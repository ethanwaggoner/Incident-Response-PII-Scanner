import mimetypes

import PyPDF2
import docx
from PyPDF2.errors import PdfReadError, FileNotDecryptedError
from docx.opc.exceptions import PackageNotFoundError
import pandas as pd


class DataExtract:
    @staticmethod
    def from_pdf(file_path):
        try:
            pdf_file = open(file_path, 'rb')
        except FileNotFoundError:
            return "Error: File not found."
        except IOError:
            return "Error: Unable to open the file."

        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text
        except FileNotDecryptedError:
            return ""
        except PdfReadError:
            return ""
        except Exception:
            return ""

    @staticmethod
    def from_csv(file_path):
        try:
            data = pd.read_csv(file_path)
        except FileNotFoundError:
            return "Error: File not found."
        except pd.errors.ParserError:
            return "Error: Failed to parse the CSV file."
        except Exception:
            return "Error"
        return data.to_string()

    @staticmethod
    def from_excel(file_path):
        try:
            data = pd.read_excel(file_path)
        except FileNotFoundError:
            return "Error: File not found."
        except Exception:
            return "Error: Failed to read the Excel file."
        return data.to_string()

    @staticmethod
    def from_txt(file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
        except FileNotFoundError:
            return ""
        except Exception:
            return ""
        return text

    @staticmethod
    def from_word(file_path):
        try:
            doc = docx.Document(file_path)
        except FileNotFoundError:
            return "Error: File not found."
        except PackageNotFoundError:
            return "Error: Failed to read the Word document."
        except Exception:
            return "Error: Failed to read the Word document."

        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text

    @staticmethod
    def from_file(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            return "Error: Unable to determine the file type."

        if mime_type == "application/pdf":
            return DataExtract.from_pdf(file_path)
        elif mime_type == "text/csv":
            return DataExtract.from_csv(file_path)
        elif mime_type in ["application/vnd.ms-excel",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            return DataExtract.from_excel(file_path)
        elif mime_type == "text/plain":
            return DataExtract.from_txt(file_path)
        elif mime_type in ["application/msword",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return DataExtract.from_word(file_path)
        else:
            return f"Error: Unsupported file type '{mime_type}'."
