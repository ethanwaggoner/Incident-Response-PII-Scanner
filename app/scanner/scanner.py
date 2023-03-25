import glob
import requests
import math
import os

from app.scanner.data_extraction import DataExtract
from app.scanner.pii_search import PiiSearch


class Scanner:
    def __init__(self, config):
        self.config = config
        self.scan_path = self.config['scan_path']
        self.id = 0
        self.filename = ""
        self.total_files = 0
        self.total_files_scanned = 0

    def run(self):
        file_extensions = self.get_file_extensions()

        self.total_files = sum(
            1 for _, _, filenames in os.walk(self.scan_path)
            for file in filenames
            if any(file.endswith(ext) for ext in file_extensions)
        )

        requests.post('http://localhost:5001/dashboard/total-files', json=self.total_files)

        for ext in file_extensions:
            for filepath in glob.iglob(f'{self.scan_path}/**/*.{ext}', recursive=True):
                self.filename = filepath
                self.scan_file_type(ext)

        requests.post('http://localhost:5001/dashboard/total-files-scanned',
                      json=self.total_files)

    def get_file_extensions(self):
        file_types_extensions = {
            'pdf': 'pdf',
            'excel': 'xlsx',
            'text': 'txt',
            'word': 'docx',
        }

        return [ext for ft, ext in file_types_extensions.items() if self.config[ft]]

    def scan_file_type(self, file_extension):
        # Assuming you have implemented functions like `extract_pdf_data`, `extract_excel_data`, etc.
        data_extract = DataExtract()
        extract_func_map = {
            'pdf': data_extract.pdf_data_extract,
            'xlsx': data_extract.excel_data_extract,
            'txt': data_extract.text_data_extract,
            'docx': data_extract.word_data_extract,
        }
        extracted_data = extract_func_map[file_extension](self.filename)
        self.search_pii(str(extracted_data))

    def search_pii(self, data):
        five_percent = math.ceil(self.total_files / 20)

        self.total_files_scanned += 1

        if self.total_files_scanned % five_percent == 0:
            requests.post('http://localhost:5001/dashboard/total-files-scanned',
                          json=self.total_files_scanned)

        if data is None:
            return
        for pii_type in ['ssn', 'ccn']:
            if self.config[pii_type]:
                self.search_pii_type(data, pii_type)

    def search_pii_type(self, data, pii_type):
        # Assuming you have implemented functions like `find_censored_ssn`, `find_censored_ccn`, etc.
        pii_search = PiiSearch()
        search_func_map = {
            'ssn': pii_search.us_ssn,
            'ccn': pii_search.us_ccn,
        }
        censored_pii = search_func_map[pii_type](str(data))
        if censored_pii:
            self.id += 1
            pii = {
                "id": self.id,
                "pii_type": pii_type,
                "file_path": self.filename,
                "pii": censored_pii[0],

            }
            requests.post('http://localhost:5001/dashboard/table-results', json=pii)

