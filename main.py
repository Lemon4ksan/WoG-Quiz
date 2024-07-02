import logging
import os
import pytesseract
import pyautogui as pygui
import keyboard
import mouse
from download_weapons import run_downloading
from fixes import fix_it
from time import sleep

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
    """
    mouse.move(*location, duration=0.05)
    mouse.press()
    sleep(0.01)
    mouse.release()
    sleep(0.01)

def main() -> None:
    try:
        start_x, start_y = locate_quiz()
    except pygui.ImageNotFoundException:
        print("Couldn't find quiz window")
        return

    while not pygui.pixelMatchesColor(start_x + 83, start_y + 266, (255, 0, 0)):
        pygui.screenshot(r'.\screenshots\weapon_image.png',
                         region=(start_x + 80, start_y + 30, 256, 185))

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
                             confidence=0.95, region=(0, 0, 256, 185), grayscale=True)
            except pygui.ImageNotFoundException:
                continue
            except IOError:
                logging.debug(f"Name {name} caused the issue")
                name = fix_it(name)  # fixes.py
                if name is None:
                    logging.debug(f"Weapon skipped")
                    continue
                try:
                    pygui.locate(r'.\screenshots\weapon_image.png',
                                 f'.\\weapons\\{name.replace('/', '[S]')}.png',
                                 confidence=0.95, region=(0, 0, 256, 185), grayscale=True)
                    logging.debug(f"Name {name} issue was resolved")
                except pygui.ImageNotFoundException:
                    continue
                except IOError:
                    logging.debug(f"Name {name} issue wasn't resolved")
                    print(f'NameError: weapon name {name} was incorrect. Please add a solution for this typo.')
                    return
            break

        click(pygui.locateCenterOnScreen(r'.\screenshots\button.png'))  # click on the correct button
        mouse.move(150, 100, False, 0.05)  # Move cursor away from the text
        sleep(0.05)

if __name__ == '__main__':
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
    keyboard.add_hotkey('q', main)
    keyboard.wait()
