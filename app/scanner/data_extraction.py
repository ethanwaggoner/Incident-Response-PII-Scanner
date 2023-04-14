import mimetypes
import aiofiles
import asyncio
import PyPDF2
import docx
from aiofiles.os import stat as aio_stat
from PyPDF2.errors import PdfReadError, FileNotDecryptedError
from docx.opc.exceptions import PackageNotFoundError
import pandas as pd
from memory_profiler import profile


class DataExtract:

    @staticmethod
    async def from_pdf(file_path):
        try:
            async with aiofiles.open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file.name)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
                return text
        except (FileNotFoundError, FileNotDecryptedError, PdfReadError, Exception) as e:
            print(e)

    @staticmethod
    async def from_csv(file_path):
        try:
            data = pd.read_csv(file_path)
            return data.to_string()
        except (FileNotFoundError, pd.errors.ParserError, Exception):
            return "Error"

    @staticmethod
    async def from_excel(file_path):
        try:
            async with aiofiles.open(file_path, 'rb') as excel_file:
                data = pd.read_excel(excel_file.name)
                return data.to_string()
        except (FileNotFoundError, Exception) as e:
            print(e)

    @staticmethod
    async def from_txt(file_path):
        try:
            async with aiofiles.open(file_path, 'r') as file:
                text = await file.read()
            return text
        except (FileNotFoundError, Exception):
            return ""

    @staticmethod
    async def from_word(file_path):
        try:
            doc = docx.Document(file_path)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text
        except (FileNotFoundError, PackageNotFoundError, Exception):
            return "Error"

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
