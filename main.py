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
    Defines start position of the quiz window.

    :returns: Coordinates to the top-right corner of the quiz window.
    """
    game_location = pygui.locateOnScreen(r'.\screenshots\locate.png', confidence=0.8)
    x, y = game_location[:2]
    return int(x), int(y)

def click(location: tuple[int, int] | pygui.Point) -> None:
    """
    Clicks on given coordinates. Uses animated mouse movement to be consistent (Don't use pygui click function).
    Sometimes click won't count. We can't do anything about it.

    :param location: Coordinates to click on.
    """
    mouse.move(*location, duration=0.05)
    mouse.press()
    sleep(0.03)
    mouse.release()
    sleep(0.03)

def find_matching_name() -> bool:
    """
    Checks if correct button was found for the screenshotted weapon (.\\screenshots\\weapon_image.png).

    :returns: True if the correct button was found, False otherwise (Error in the script).
    """
    for button_index in range(6):
        weapon_name: str = screenshot_button(button_index)
        if correct_weapon(weapon_name):
            return True
        if button_index == 5:  # All buttons are incorrect
            return False

def screenshot_button(button_index: int) -> str:
    """
    Screenshots button at given index and returns its text (.\\screenshots\\button.png).

    :param button_index: Index of the current button.
    :returns: String representing weapon name.
    """
    if button_index < 3:
        pygui.screenshot(r'.\screenshots\button.png',
                         region=(start_x, start_y + 295 + 30 * button_index, 200, 30))
    else:
        pygui.screenshot(r'.\screenshots\button.png',
                         region=(start_x + 200, start_y + 295 + (30 * button_index - 90), 200, 30))

    name: str = pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip()

    return name

def correct_weapon(weapon_name: str) -> bool:
    """
    Checks if given weapon name corresponds to the weapon on screen.

    :param weapon_name: String representing weapon name.
    :returns: True if the weapon name corresponds to the weapon on screen, False otherwise.
    :raises NameError: Weapon name doesn't exist.
    """
    try:
        pygui.locate(r'.\screenshots\weapon_image.png',
                     fr'.\weapons\{weapon_name.replace('/', '[S]')}.png',
                     confidence=0.955, region=(0, 0, 256, 185), grayscale=True)
    except pygui.ImageNotFoundException:
        return False
    except IOError:
        logging.debug(f"Name {weapon_name} caused the issue")
        weapon_name = fix_it(weapon_name)  # fixes.py
        if weapon_name is None:
            logging.debug(f"Name was skipped")
            return False
        try:
            pygui.locate(r'.\screenshots\weapon_image.png',
                         fr'.\weapons\{weapon_name.replace('/', '[S]')}.png',
                         confidence=0.955, region=(0, 0, 256, 185), grayscale=True)
            logging.debug(f"Name {weapon_name} issue was resolved")
        except pygui.ImageNotFoundException:
            logging.debug(f"Name {weapon_name} issue was resolved")
            return False
        except IOError:
            logging.debug(f"Name {weapon_name} issue wasn't resolved")
            raise NameError(f'NameError: weapon name {weapon_name} was incorrect. Please add a solution for this typo.')

    return True

def main() -> None:
    """
    :Note: Multiprocessing module slows everything down sadly. locate() is faster than locateOnScreen()
    """
    global start_x, start_y

    try:
        start_x, start_y = locate_quiz()
    except pygui.ImageNotFoundException:
        print("Couldn't find quiz window")
        return

    start_time = time()
    while round(time() - start_time) < 45:
        pygui.screenshot(r'.\screenshots\weapon_image.png',
                         region=(start_x + 80, start_y + 29, 256, 185))

        if not find_matching_name():
            print("No matches found. Quiz is finished")
            return

        try:
            click(pygui.locateCenterOnScreen(r'.\screenshots\button.png'))  # click on the correct button
            mouse.move(0, 100, False, 0.05)
        except pygui.ImageNotFoundException:
            print("Quiz is finished")
            return

    print("Quiz is finished")

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
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        exit()
