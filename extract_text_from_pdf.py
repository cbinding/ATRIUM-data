# see https://www.geeksforgeeks.org/extract-text-from-pdf-file-using-python/

# importing required modules 
from pypdf import PdfReader 
  
# creating a pdf reader object 
reader = PdfReader('./001_142_151.pdf') 
  
# printing number of pages in pdf file 
print(len(reader.pages)) 
  
# getting a specific page from the pdf file 
page1 = reader.pages[0] 
page2 = reader.pages[1]
  
# extracting text from page 
text1 = page1.extract_text() 
text2 = page2.extract_text() 
text3 = " ".join([text1, text2])
cleaned = " ".join(text3.split()).replace("- ", "")

print(cleaned)