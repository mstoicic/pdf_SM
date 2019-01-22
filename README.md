# PDFSM - Pdf Split & Merge

Simple command line tool to split and merge multiple pdf files

## Install


Python 3.6+ required.  
Clone or download git repository.  
Use
```
pipenv install
```
in program folder to install required dependencies (PyPDF2) and create virtual environment.  

## Usage

Write a .txt config file with desired PDF location and desired page numbers or page ranges.

```
Full PDF file location and name.pdf    pagenumber, pagenumber
Full PDF file location and name.pdf    pagenumber-pagenumber
```

Example(`config.txt`):

```
C:/Users/UserName/Downloads/py_regex.pdf 1-10,16,22
C:/Users/UserName/Desktop/py_regex.pdf 1-40
D:/Folder/random_file.pdf 6,8,9-20

```

Program will process the files sequentially from top to bottom and include only the defined
pages in the final PDF document.  
  
Use command:

```
python pdf_SM.py -i config.txt -o split_and_merge.pdf
```

You can also choose to use different file encoding:

```
python pdf_SM.py -i config.txt -o split_and_merge.pdf -e utf8
```