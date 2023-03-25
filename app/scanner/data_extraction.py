import PyPDF2
import docx2txt
import pandas as pd


class DataExtract:
    # Extracts the data from the Word document
    @staticmethod
    def word_data_extract(directory):
        try:
            data = docx2txt.process(directory)
            return data
        except Exception:
            pass

    # Extracts the data from the CSV file
    @staticmethod
    def csv_data_extract(directory):
        try:
            data = str(pd.read_csv(directory, encoding="latin1"))
            return data
        except Exception:
            pass

    # Extracts the data from the Excel file
    @staticmethod
    def excel_data_extract(directory):
        try:
            spreadsheet = pd.ExcelFile(directory, engine="openpyxl")
            data_list = []
            for sheet in spreadsheet.sheet_names:
                data = str(spreadsheet.parse(sheet))
                data_list.append(data)
            return data_list
        except Exception:
            pass

    # Extracts the data from the Text file
    @staticmethod
    def text_data_extract(directory):
        try:
            data_list = []
            with open(directory, mode='r', encoding="latin-1") as f:
                for line in f:
                    data_list.append(line)
                return data_list
        except Exception:
            pass

    # Extracts the data from the PDF document
    @staticmethod
    def pdf_data_extract(directory):
        try:
            with open(directory, mode='rb') as file:
                reader = PyPDF2.PdfFileReader(file)
                data_list = []
                for page in reader.pages:
                    pdf_text = page.extractText()
                    pdf_text = pdf_text.replace('\n', '')
                    data_list.append(pdf_text)
                return data_list
        except Exception:
            pass