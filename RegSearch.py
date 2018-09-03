#! python3
# this program searches all the files in a specified directory and picks out the specified pattern
# Usage: RegSearch <absolute directory path> <Pattern>

import os, sys, pyperclip, re, docx2txt
from unipath import Path
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


matches = []
path = sys.argv[1]
savepath = Path(path)
newpath = savepath.parent
# checks if the path is valid
if not(os.path.exists(path)):
    print("Error path does not exist!")
    sys.exit(1)

# regex for phone
regexPhone = re.compile(r'''((\d{3} | \(\d{3}\))?  #area code (optional)
(\s|-|\.)?                                    #space divider (optional)
(\d{3})                                       #middle 3 numbers
(\s|-|\.)?                                    #space divider (optional)
(\d{4})                                       #last 4 numbers
)''', re.VERBOSE)

#regex for email
regexEmail = re.compile(r'''(
    [a-zA-Z0-9._%+-]+
    @
    [a-zA-Z0-9.-]+
    (\.[a-zA-Z]{2,4})
    )''', re.VERBOSE)

if(len(sys.argv) < 3):
    print("Enter in the pattern you want to search for(Not Working Yet):")
    CusPattern = input()
    Search = re.compile(CusPattern)
elif(sys.argv[2] == 'email'):
    Search = regexEmail
elif(sys.argv[2] == 'phone'):
    Search = regexPhone

#function to convert pdf to text
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    pyperclip.copy(text)

#function to scan text against regSearches
def regSearch(text):
    for groups in Search.findall(text):
        phoneNum = '-'.join([groups[1], groups[3], groups[5]])
        matches.append(phoneNum)
    for groups in Search.findall(text):
        matches.append(groups[0])

# creates the file inside the directory to be walked

f=open(newpath+"\\results.txt", "w")

#walks through the given directory
for(dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if filename.endswith('.txt'): # looks for txt files
            file = open(os.path.join(path,dirpath,filename), 'r').read()
            pyperclip.copy(file)
            # scans text files for the regex search
            regSearch(pyperclip.paste())

        if filename.endswith('.pdf'): # looks for pdf files
            convert_pdf_to_txt(os.path.join(path,dirpath,filename))
            # scans text for regex search
            regSearch(pyperclip.paste())

        if filename.endswith('.docx'): # looks for docx files
            text = docx2txt.process(os.path.join(path,dirpath,filename))
            pyperclip.copy(text)
                #scans text for regex search
            regSearch(pyperclip.paste())

# copy results to the clipboard and writes to the result.txt file

if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('copied to clipboard and written to file:' + newpath +"\\results.txt: ")
    print('\n'.join(matches))
    f.write(pyperclip.paste())
else:
    print('No phone numbers or email addresses found')

f.close()
