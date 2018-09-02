#! python3
# this program searches all the files in a specified directory and picks out the specified pattern
# Usage: RegSearch <absolute directory path> <Pattern>

import os, sys, pyperclip, re, PyPDF2, docx2txt
from unipath import Path
from docx import Document

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


def getText(fname):
    doc = Document(fname)
    fullText= []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


if(len(sys.argv) < 3):
    print("Enter in the pattern you want to search for(Not Working Yet):")
    CusPattern = input()
    Search = re.compile(CusPattern)
elif(sys.argv[2] == 'email'):
    Search = regexEmail
elif(sys.argv[2] == 'phone'):
    Search = regexPhone



# creates the file inside the directory to be walked

f=open(newpath+"\\results.txt", "w")

#walks through the given directory
for(dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if filename.endswith('.txt'): # looks for txt files
            file = open(os.path.join(path,dirpath,filename), 'r').read()
            pyperclip.copy(file)
            # scans text files for the regex search
            for groups in Search.findall(pyperclip.paste()):
                phoneNum = '-'.join([groups[1],groups[3],groups[5]])
                matches.append(phoneNum)
            for groups in Search.findall(pyperclip.paste()):
                matches.append(groups[0])
        if filename.endswith('.pdf') and  filename.isEncryptec() == False: # looks for pdf files
            print("Hello")

        if filename.endswith('.docx'): # looks for docx files
            text = docx2txt.process(os.path.join(path,dirpath,filename))
            pyperclip.copy(text)
                #scans text for regex search
            for groups in Search.findall(pyperclip.paste()):
                phoneNum = '-'.join([groups[1], groups[3], groups[5]])
                matches.append(phoneNum)
            for groups in Search.findall(pyperclip.paste()):
                matches.append(groups[0])

# copy results to the clipboard and writes to the result.txt file

if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('copied to clipboard and written to file:' + newpath +"\\results.txt: ")
    print('\n'.join(matches))
    f.write(pyperclip.paste())
else:
    print('No phone numbers or email addresses found')

f.close()
