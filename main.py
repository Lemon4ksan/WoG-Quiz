import cv2
import logging
import os
import pytesseract
import pyautogui as pygui
import keyboard
import mouse
from download_weapons import run_downloading
from fixes import fix_it
from time import time, sleep

def locate_quiz() -> tuple[int, int]:
    """
    Defines start position of the quiz window
    """
    game_location = pygui.locateOnScreen(r'.\screenshots\locate.png', confidence=0.8)
    x, y = game_location[:2]
    return int(x), int(y)

def click(location: tuple[int, int] | pygui.Point) -> None:
    """
    Clicks on given coordinates. Uses animated mouse movement to be consistent (Don't use pygui click functions)
    Sometimes click won't count. We can't do anything about this (Even win32_api lib can fail)
    """
    mouse.move(*location, duration=0.05)
    mouse.press()
    sleep(0.03)
    mouse.release()
    sleep(0.03)

def main() -> None:
    """
    :Note: Multiprocessing module slows everything down sadly. locate() is faster than locateOnScreen()
    """
    try:
        start_x, start_y = locate_quiz()
    except pygui.ImageNotFoundException:
        print("Couldn't find quiz window")
        return
    start_time = time()
    while round(time() - start_time) < 45:
        pygui.screenshot(r'.\screenshots\weapon_image.png',
                         region=(start_x + 80, start_y + 29, 256, 185))
        for i in range(6):
            if i < 3:
                pygui.screenshot(r'.\screenshots\button.png',
                                 region=(start_x, start_y + 295 + 30 * i, 200, 30))
                name: str = pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip()
            else:
                pygui.screenshot(r'.\screenshots\button.png',
                                 region=(start_x + 200, start_y + 295 + (30 * i - 90), 200, 30))
                name: str = pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip()
            try:
                pygui.locate(r'.\screenshots\weapon_image.png',
                             f'.\\weapons\\{name.replace('/', '[S]')}.png',
                             confidence=0.955, region=(0, 0, 256, 185), grayscale=True)
            except pygui.ImageNotFoundException:
                if i == 5:
                    print("No matches found")
                    return
                continue
            except IOError:
                logging.debug(f"Name {name} caused the issue")
                name = fix_it(name)  # fixes.py
                if name is None:
                    logging.debug(f"Weapon {name} was skipped")
                    continue
                try:
                    pygui.locate(r'.\screenshots\weapon_image.png',
                                 f'.\\weapons\\{name.replace('/', '[S]')}.png',
                                 confidence=0.955, region=(0, 0, 256, 185), grayscale=True)
                    logging.debug(f"Name {name} issue was resolved")
                except pygui.ImageNotFoundException:
                    logging.debug(f"Name {name} issue was resolved")
                    if i == 5:
                        print("No matches found. Quiz is finished")
                        return
                    continue
                except IOError:
                    logging.debug(f"Name {name} issue wasn't resolved")
                    print(f'NameError: weapon name {name} was incorrect. Please add a solution for this typo.')
                    return
            break

        try:
            click(pygui.locateCenterOnScreen(r'.\screenshots\button.png'))  # click on the correct button
            mouse.move(0, 100, False, 0.05)  # Move cursor away from the text
        except pygui.ImageNotFoundException:
            print("Quiz is finished")
            return

if __name__ == '__main__':
    cv2.setLogLevel(-1)
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="logs.log", level=logging.DEBUG, filemode="w")

    with open("path.txt", "r") as file:
        path = file.read()

    if path:
        pytesseract.pytesseract.tesseract_cmd = fr'{path}'
        try:
            pytesseract.image_to_string(r'.\screenshots\locate.png')
        except (PermissionError, pytesseract.pytesseract.TesseractNotFoundError):
            print('TesseractNotFoundError: Invalid path to Tesseract')
            exit(0)

    if not os.access(r'.\weapons', os.F_OK):
        print('Downloading missing weapons...')
        os.mkdir(r'.\weapons')
        run_downloading()
    print("Press Q to start for 1 iteration")
    # I could make it fully automatic, but there are still too many issues
    # User interaction is required
    keyboard.add_hotkey('q', main)
    keyboard.wait()
