"""
File Name     :: pdf_SM.py
Description   :: Split and merge PDF files
License       :: MIT
Contributor   :: Marijan Stoicic [GH: mstoicic]
Dependencies  :: PyPDF2 module
"""


import PyPDF2
import argparse
import re
from collections import OrderedDict
from typing import List


def interpret_config_file(file_path: str, file_encoding: str = None):
    """Interpretes configuration file / returns ordered dictionary with filepath:page numbers pairs"""
    
    with open(file_path, "r", encoding=file_encoding) as f:
        lines = f.readlines()

    d = OrderedDict()

    for i, line in enumerate(lines):
        l = line.split(".pdf")

        if len(l) != 2:
            raise ValueError(f"Something is wrong with the config file at line: {i + 1} -> {line}")

        pdf_file_path = l[0] + ".pdf"
        page_numbers = interpret_page_numbers(l[1])

        d[i] = {pdf_file_path: page_numbers}

    return d


def interpret_page_numbers(page_numbers: str):
    """Interpretes page numbers / returns list with page numbers"""

    numbers = []
    
    page_numbers_list = page_numbers.replace(" ", "").split(",")

    if len(page_numbers_list) == 0:
        raise ValueError("There are no page numbers determined")

    for p in page_numbers_list:
        if len(re.findall(r"-", p)) == 1:
            start_n, end_n = p.split("-")
            start_n = int(start_n)
            end_n = int(end_n)
            numbers.extend(list(range(start_n, end_n + 1)))
        else:
            numbers.append(int(p))

    return sorted(list(set(numbers)))


def extract_interesting_pdf_pages(pdf_dict: dict):
    """Extracts pdf pages / returns list of pdf pages"""
    
    pages = []

    for pdf_file_number, details_dict in pdf_dict.items():
        pdf_file_path = list(details_dict.keys())[0]
        page_numbers = list(details_dict.values())[0]
        pdf = PyPDF2.PdfFileReader(pdf_file_path)

        for i in page_numbers:
            p = i - 1
            try:
                pages.append(pdf.getPage(p))
            except:
                print(f"There is no page: {p} in pdf file: {pdf_file_path}, so it's getting ignored.")
    
    return pages


def merge_pdf_pages(pdf_pages: list):
    """Merges pdf pages / returns merged pdf"""

    pdf = PyPDF2.PdfFileWriter()
    for p in pdf_pages:
        pdf.addPage(p)
    return pdf


def split_and_merge():
    """Main function"""
    
    #Command line argument perser
    parser = argparse.ArgumentParser(description='Split then merge .pdf files')
    parser.add_argument('-i', '--input', required=True, type=str)
    parser.add_argument('-o', '--output', required=True, type=str)
    parser.add_argument('-e', '--encoding', default=None, type=str)

    args = vars(parser.parse_args())

    input_config_file_path = args["input"]
    file_encoding = args["encoding"]
    output_pdf_file_path = args["output"]

    pdf_dict = interpret_config_file(input_config_file_path, file_encoding)
    interesting_pdf_pages = extract_interesting_pdf_pages(pdf_dict)
    pdf = merge_pdf_pages(interesting_pdf_pages)

    with open(output_pdf_file_path, "wb") as f:
        pdf.write(f)

    print(f"***** Final number of pages in the new document: {pdf.getNumPages()}")
    print(f"***** Split and Merge is done! File is written to path: {output_pdf_file_path}")


#Run the program
if __name__ == "__main__":
    split_and_merge()