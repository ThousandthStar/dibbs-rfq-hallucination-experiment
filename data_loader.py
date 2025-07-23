
import requests
import os
import glob
from bs4 import BeautifulSoup

def load_data(file_path: str, folder_name: str) -> list[str]:
    
    try:
        os.mkdir(folder_name)
        print(f"Created folder {folder_name}")
    except FileExistsError:
        print(f"Folder {folder_name} already exists, clearing folder...")
        files = glob.glob(f"{folder_name}/*")
        for file in files:
            os.remove(file)

    paths: list[str] = []

    with open(file_path, "r") as file:
        for line in file:
            raw = line.strip()
            name = raw.split("/")[-1]
            path = f"{folder_name}/{name}";
            warning_url = raw.replace("https://dibbs2.bsm.dla.mil", "https://dibbs2.bsm.dla.mil/dodwarning.aspx?goto=")

            session = requests.Session()
            r = session.get(warning_url)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")
            data = {
                "__VIEWSTATE":            soup.find(id="__VIEWSTATE")["value"],
                "__VIEWSTATEGENERATOR":   soup.find(id="__VIEWSTATEGENERATOR")["value"],
                "__EVENTVALIDATION":      soup.find(id="__EVENTVALIDATION")["value"],
                "butAgree":               "OK",
            }

            post = session.post(warning_url, data=data)
            post.raise_for_status()

            pdf = session.get(raw)
            pdf.raise_for_status()

            with open(path, "wb") as to_write:
                to_write.write(pdf.content)

