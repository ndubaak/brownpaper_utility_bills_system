from pypdf import PdfReader
import re
from cerberus import Validator


reader = PdfReader("1802859732-29-05-2019.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
n = 1

v = Validator({'text': {'type': 'string'}})
print(v.validate({'text': n}))

# names = re.findall(r'\b[A-Z][a-z]*\.\s[A-Z][a-z]*\.\s[A-Z][a-zA-Z]+\b', text)

# print(text)


# emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

# # Print the emails
# for email in emails:
#     print(email)

