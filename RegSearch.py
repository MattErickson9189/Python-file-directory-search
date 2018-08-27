#! python3
# this program searches all the files in a specified directory and picks out the specified pattern
# Usage: RegSearch <absolute directory path> <Pattern> (Custom pattern not implemented yet, only phone numbers)
#WIP

import os, sys, pyperclip, re

#path = sys.argv[1]

#if not(os.path.exists(path)):
 #   print("Error path does not exist!")
  #  sys.exit(1)


regexPhone = re.compile(r'''((\d{3} | \(\d{3}\))?  #area code (optional)
(\s|-|\.)?                                    #space divider (optional)
(\d{3})                                       #middle 3 numbers
(\s|-|\.)?                                    #space divider (optional)
(\d{4})                                       #last 4 numbers
)''', re.VERBOSE)

regexEmail = re.compile(r'''(
    [a-zA-Z0-9._%+-]+
    @
    [a-zA-Z0-9.-]+
    (\.[a-zA-Z]{2,4})
    )''', re.VERBOSE)

#find matches in clipboard text
text = str(pyperclip.paste())

matches = []

f=open("matched.txt", "w");

for groups in regexPhone.findall(text):
    phoneNum = '-'.join([groups[1],groups[3],groups[5]])
    if groups[5] != '':
        phoneNum += ' x' + groups[5]
    matches.append(phoneNum)
for groups in regexEmail.findall(text):
    matches.append(groups[0])

#copy results to the clipboard

if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('copied to clipboard:')
    print('\n'.join(matches))
    f.write(pyperclip.paste())
else:
    print('No phone numbers or email addresses foind')

f.close()
