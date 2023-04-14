import fnmatch
import glob
import requests
import math
import os
import httpx
import asyncio

from app.scanner.data_extraction import DataExtract
from app.scanner.pii_search import PiiSearch


class Scanner:
    def __init__(self, config):
        self.config = config
        self.custom_search = self.config['custom_search']
        self.scan_path = self.config['scan_path']
        self.id = 0
        self.filename = ""
        self.total_files = 0
        self.total_files_scanned = 0

    @staticmethod
    async def post_async(url, json):
        async with httpx.AsyncClient() as client:
            await client.post(url, json=json, timeout=3600)

    async def count_total_files_and_post(self, file_extensions):
        count = 0
        for root, _, filenames in os.walk(self.scan_path):
            for ext in file_extensions:
                count += sum(fnmatch.fnmatch(file, f'*.{ext}') for file in filenames)
        self.total_files = count
        await self.post_async('http://localhost:5001/dashboard/total-files', self.total_files)

    async def scan_files(self, file_extensions):
        for ext in file_extensions:
            for filepath in glob.iglob(f'{self.scan_path}/**/*.{ext}', recursive=True):
                self.filename = filepath
                await self.scan_file_type(ext)
        await self.post_async('http://localhost:5001/dashboard/total-files-scanned', self.total_files_scanned)

    async def run(self):
        file_extensions = self.get_file_extensions()

        # Run the count_total_files_and_post and scan_files methods concurrently
        await asyncio.gather(
            self.count_total_files_and_post(file_extensions),
            self.scan_files(file_extensions)
        )

    def get_file_extensions(self):
        file_types_extensions = {
            'pdf': 'pdf',
            'excel': 'xlsx',
            'text': 'txt',
            'word': 'docx',
            'csv': 'csv',
        }

        return [ext for ft, ext in file_types_extensions.items() if self.config[ft]]

    async def scan_file_type(self, file_extension):
        data_extract = DataExtract()
        extract_func_map = {
            'pdf': data_extract.from_pdf,
            'xlsx': data_extract.from_excel,
            'txt': data_extract.from_txt,
            'docx': data_extract.from_word,
            'csv': data_extract.from_csv,
        }
        extracted_data = await extract_func_map[file_extension](self.filename)
        await self.search_pii(str(extracted_data))

    async def search_pii(self, data):
        self.total_files_scanned += 1
        five_percent = math.ceil(self.total_files / 20)
        if self.total_files_scanned % five_percent == 0 or self.total_files_scanned == self.total_files:
            await self.post_async('http://localhost:5001/dashboard/total-files-scanned', self.total_files_scanned)
        if data is None:
            return
        for pii_type in ['ssn', 'ccn', 'custom']:
            if self.config['ssn'] or self.config['ccn'] or pii_type == 'custom':
                await self.search_pii_type(data, pii_type)

    async def search_pii_type(self, data, pii_type):
        # Assuming you have implemented functions like `find_censored_ssn`, `find_censored_ccn`, etc.
        pii_search = PiiSearch(self.custom_search)
        search_func_map = {
            'ssn': pii_search.us_ssn,
            'ccn': pii_search.us_ccn,
            'custom': pii_search.search_custom,
        }
        censored_pii = await search_func_map[pii_type](str(data))
        if censored_pii:
            self.id += 1
            pii = {
                "id": self.id,
                "pii_type": pii_type,
                "file_path": self.filename,
                "pii": censored_pii[0],

            }
            await self.post_async('http://localhost:5001/dashboard/table-results', pii)
