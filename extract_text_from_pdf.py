# see https://www.geeksforgeeks.org/extract-text-from-pdf-file-using-python/
import requests, os
# importing required modules 
from pypdf import PdfReader 

def main():
    # creating a pdf reader object 
    reader = PdfReader('./data/078_047_054.pdf') 
    
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

def get_file_from_url(source_url: str="", target_folder: str=""):
    target = os.path.join(target_folder, "tmp1.pdf")
    response = requests.get(source_url, timeout=30)
    with open(target, "wb") as file:
        file.write(response.content)
    

    

if __name__ == "__main__":
    main()
    