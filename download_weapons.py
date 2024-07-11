import os
import io
import requests
from PIL import Image
from alive_progress import alive_bar
from time import sleep
from random import uniform
from bs4 import BeautifulSoup

headers = {
    "Access-Control-Allow-Origin": "*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 "
                  "Safari/537.36"
}

def page_request(url: str, *, use_index: bool = False) -> BeautifulSoup:
    """
    :param url: URL of the page
    :param use_index: Should program create index.html file. Defaults to False. If such file exists it will use it

    :returns: BeautifulSoup object
    """
    if use_index and not os.access("index.html", os.F_OK):
        req = requests.get(url, headers=headers)
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(req.text)
    if os.access("index.html", os.F_OK):
        with open("index.html", "r", encoding="utf-8") as file:
            html = file.read()
    else:
        req = requests.get(url, headers=headers)
        html = req.text

    return BeautifulSoup(html, "lxml")

def bar_progress(link: str, name: str) -> None:
    """
    Single bar progress

    :param link: String representing link to the file to download
    :param name: String representing name of the weapon
    """
    if "/" in name:
        if name == "Stryk B / Type B":
            name = "Stryk B"
        else:
            name = name.replace("/", "[S]")

    if not f"{name}.png" in os.listdir(".\\weapons"):
        img_data = requests.get(link, headers=headers).content
        sleep(round(uniform(0.5, 1), 2))
        new_image = Image.open(io.BytesIO(img_data))
        new_image = new_image.crop((0, 0, 256, 185))
        new_image.save(fr'.\weapons\{name}.png')

def download_subsection(links: list[str], names: list[str], subsection_title: str) -> None:
    """
    Single subsection downloading

    :param links: List of strings representing link to the file to download
    :param names: List of strings representing name of the weapon
    :param subsection_title: String representing name of the subsection
    """
    with alive_bar(len(links),
                   elapsed=False, stats=False, length=10, max_cols=120,
                   title=f"Downloading {subsection_title}",
                   monitor="{count}/{total}",
                   force_tty=True) as bar:
        for link, name in zip(links, names):
            bar_progress(link, name)
            bar()

def main(html: BeautifulSoup) -> None:
    subsections = html.find_all("div", class_="subSection detailBox")
    for subsection in subsections:
        subsection_title: str = subsection.find("div", class_="subSectionTitle").text.strip()

        link_objects = subsection.find_all("a", class_="modalContentLink")
        name_objects = subsection.find_all("b")
        links: list[str] = [obj.get("href") for obj in link_objects]
        names: list[str] = [obj.text for obj in name_objects if obj.text != ""]

        download_subsection(links, names, subsection_title)

    print(f"All {len(html.find_all("a", class_="modalContentLink"))} weapons downloaded")

def run_downloading() -> None:
    """Start downloading process"""
    page = page_request("https://steamcommunity.com/sharedfiles/filedetails/?id=2589399401")
    main(page)

if __name__ == '__main__':
    run_downloading()
