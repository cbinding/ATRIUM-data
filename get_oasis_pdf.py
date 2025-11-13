import requests, os, re 

# https://www.pythontutorials.net/blog/python-download-files-from-google-drive-using-url/
def download_google_drive_file(url, save_path):  
    """Download a file from Google Drive using its URL."""  
    file_id = extract_file_id(url)  
    base_url = "https://drive.google.com/uc?export=download&id="  
    download_url = f"{base_url}{file_id}"  
 
    session = requests.Session()  
    response = session.get(download_url, stream=True)  
 
    # Check if the response requires a confirmation token (large file)  
    if "Content-Disposition" not in response.headers:  
        # Look for the confirmation token in the response content  
        token_pattern = r'confirm=([^&]+)'  
        token_match = re.search(token_pattern, response.text)  
        if token_match:  
            confirm_token = token_match.group(1)  
            download_url = f"{download_url}&confirm={confirm_token}"  
            response = session.get(download_url, stream=True)  
        else:  
            raise RuntimeError("Could not bypass virus scan warning. No confirmation token found.")  
 
    # Extract filename from Content-Disposition header if available  
    filename = None  
    content_disposition = response.headers.get("Content-Disposition")  
    if content_disposition:  
        filename_pattern = r'filename="?([^"]+)"?'  
        filename_match = re.search(filename_pattern, content_disposition)  
        if filename_match:  
            filename = filename_match.group(1)  
 
    # ensure the intended output path exists 
    if not os.path.exists(save_path): os.makedirs(save_path)

    # Use provided save_path or auto-generate filename  
    if save_path.endswith('/'):  # If save_path is a directory  
        if not filename:  
            filename = f"downloaded_file_{file_id}"  
        save_path = os.path.join(save_path, filename)  
    else:  
        filename = save_path.split('/')[-1]  # Use user-provided filename  
 
    # Download the file in chunks to handle large files      
    try:  
        with open(save_path, "wb") as f:  
            for chunk in response.iter_content(chunk_size=8192):  
                if chunk:  # Filter out keep-alive chunks  
                    f.write(chunk)  
        print(f"Successfully downloaded: {filename}")  
        return save_path  
    except Exception as e:  
        raise RuntimeError(f"Failed to save file: {str(e)}") 
    

def extract_file_id(url):  
    """Extract FILE_ID from a Google Drive URL."""  
    pattern = r'(?:id=|/d/)([a-zA-Z0-9_-]+)'  
    match = re.search(pattern, url)  
    if match:  
        return match.group(1)  
    else:  
        raise ValueError("Invalid Google Drive URL. Could not extract FILE_ID.")
    

if __name__ == "__main__":
    #main()
    file_urls = [
        "https://drive.google.com/file/d/1WbM2E7hGSS4ik2LLjApnZrk-kqk5anvf/view?usp=drive_link",
        "https://drive.google.com/file/d/1oInKzYtxsOh2MQ3ZKY3ma5t--rcSlnL_/view?usp=drive_link",
    ]

    file_url = "https://drive.google.com/file/d/1WbM2E7hGSS4ik2LLjApnZrk-kqk5anvf/view?usp=drive_link"

    folder_url = "https://drive.google.com/drive/folders/1STO5OJ40SVBSo1fgPo1feXcEXbYDtz4m?usp=drive_link"

    target_folder = "data/tmp/"

    try:  
        download_google_drive_file(file_url, target_folder)  
    except Exception as e:  
        print(f"Error: {e}")  

   