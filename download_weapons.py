import os
import requests
from PIL import Image
from alive_progress import alive_bar
from time import sleep
from random import uniform
from bs4 import BeautifulSoup

headers = {  # to look less like a bot
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
        html = req.text, "lxml"

    return BeautifulSoup(html, "lxml")


def main(html) -> None:
    subsections = html.find_all("div", class_="subSection detailBox")
    for subsection in subsections:
        subsection_title: str = subsection.find("div", class_="subSectionTitle").text.strip()

        link_objects = subsection.find_all("a", class_="modalContentLink")
        name_objects = subsection.find_all("b")
        links: list[str] = [obj.get("href") for obj in link_objects]
        names: list[str] = [obj.text for obj in name_objects if obj.text != ""]

        with alive_bar(len(links),
                       elapsed=False, stats=False, length=10, max_cols=120,
                       title=f"Downloading {subsection_title}",
                       monitor="{count}/{total}",
                       force_tty=True) as bar:
            for link, name in zip(links, names):
                if "/" in name:  # On Windows / is an illegal character, but it must be saved
                    match name:
                        case "Stryk B / Type B":  # Random typo...
                            name = "Stryk B"
                        case _:
                            name = name.replace("/", "[S]")
                if not f"{name}.png" in os.listdir(".\\weapons"):
                    img_data = requests.get(link, headers=headers).content
                    sleep(round(uniform(0.5, 1), 2))  # Don't spam Steam too much
                    with open(f".\\weapons\\{name}.png", "wb") as handler:
                        handler.write(img_data)
                    # Images are cropped to be simmilar with screenshots
                    new_image = Image.open(f".\\weapons\\{name}.png")
                    new_image = new_image.crop((0, 0, 256, 185))
                    new_image.save(f".\\weapons\\{name}.png")
                bar()
    print(f"All {len(html.find_all("a", class_="modalContentLink"))} weapons downloaded")

def run_downloading() -> None:
    page = page_request("https://steamcommunity.com/sharedfiles/filedetails/?id=2589399401")
    main(page)

if __name__ == '__main__':
    run_downloading()
