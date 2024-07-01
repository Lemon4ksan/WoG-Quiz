import os
import pytesseract
import pyautogui as pygui
import keyboard
import mouse
from download_weapons import run_downloading
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

    pygui.screenshot(r'.\screenshots\weapon_image.png',
                     region=(start_x + 80, start_y + 30, 256, 185))

    for i in range(6):
        if i < 3:
            pygui.screenshot(r'.\screenshots\button.png',
                             region=(start_x, start_y + 295 + 30 * i, 200, 30))
            name: str = pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip()
        else:
            pygui.screenshot(r'.\screenshots\button.png',  # This is awful, but it works. !Rewrite!
                             region=(start_x + 200, start_y + 295 + 30 * (5 - i), 200, 30))
            name: str = pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip()
        try:
            pygui.locate(r'.\screenshots\weapon_image.png',
                         f'.\\weapons\\{name.replace('/', '[S]')}.png',
                         confidence=0.9, region=(0, 0, 256, 185))  # TODO: Adjust pixels to get clean white space
        except pygui.ImageNotFoundException:
            continue
        except IOError:
            # Attempts to fix wrong text recognition. There will be more fixes later on
            match name:
                case "Bren":
                    name.replace("l", "I")
            try:
                pygui.locate(r'.\screenshots\weapon_image.png',
                             f'.\\weapons\\{name.replace('/', '[S]')}.png',
                             confidence=0.9, region=(0, 0, 256, 185))  # TODO: same here
            except pygui.ImageNotFoundException:
                continue
            except IOError:
                print(f'NameError: weapon name {name} was incorrect. Please add a solution for this typo.')
                break
        break

    click(pygui.locateCenterOnScreen(r'.\screenshots\button.png'))  # click on the correct button
    mouse.move(150, 0, False, 0.05)  # Move cursor away from the text

if __name__ == '__main__':
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
    print("Press Q to answer the current quiz")   # TODO: Make it loop until game over
    keyboard.add_hotkey('q', main)
    keyboard.wait()
