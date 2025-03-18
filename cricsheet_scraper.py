import os
import requests
import zipfile
from bs4 import BeautifulSoup

# Given URL of Cricsheet downloads page

match_types = {
    "Test matches": "https://cricsheet.org/downloads/tests_json.zip",
    "One-day internationals": "https://cricsheet.org/downloads/odis_json.zip",
    "T20 internationals": "https://cricsheet.org/downloads/t20s_json.zip"

}

# Folders for zip and json files.
zip_folder = "cricsheet_zips"
json_folder = "cricsheet_json"

downloaded_files = []

# Download the files
for match_type in match_types:
    match_URL =match_types.get(match_type)
    print(match_URL)
    filename = os.path.basename(match_URL)
    file_path = os.path.join(zip_folder, filename)
    print(f"file_path***{file_path}")
    zip_response = requests.get(match_URL)
    if zip_response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(zip_response.content)
        downloaded_files.append(file_path)
    else:
        print(f"Failed to download: {match_URL}")

# Unzipping downloaded files
print(downloaded_files)

for zip_file in downloaded_files:
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(json_folder)
    except Exception as e:
        print(f"Error extracting {zip_file}: {e}")

