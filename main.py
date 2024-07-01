import os
import pytesseract
import pyautogui as pygui
import keyboard
from download_weapons import run_downloading

def locate_quiz() -> tuple[int, int] | None:
    """
    Defines start position of the quiz window
    """
    game_location = pygui.locateOnScreen(r'.\screenshots\locate.png', confidence=0.8)
    x, y = game_location[:2]
    return int(x), int(y)

def main() -> None:
    """
    TODO: Fix some issues. Make application choose correct buttons by itself
    """
    try:
        start_x, start_y = locate_quiz()
    except pygui.ImageNotFoundException:
        print("Couldn't find quiz window")
        return
    names: list[str] = []

    for i in range(3):
        pygui.screenshot(r'.\screenshots\button.png',
                         region=(start_x, start_y + 295 + 30 * i, 200, 30))
        names.append(pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip())

    for i in range(3):
        pygui.screenshot(r'.\screenshots\button.png',
                         region=(start_x + 200, start_y + 295 + 30 * i, 200, 30))
        names.append(pytesseract.image_to_string(r'.\screenshots\button.png', lang='eng').strip())

    # Button size 200x30
    # Button menu size 0x300
    # Guide images offest 80 30 256 185

    pygui.screenshot(r'.\screenshots\weapon_image.png',
                     region=(start_x + 80, start_y + 30, 256, 185))
    for name in names:
        try:
            pygui.locate(r'.\screenshots\weapon_image.png',
                         f'.\\weapons\\{name.replace('/', '[S]')}.png',
                         confidence=0.8, region=(0, 0, 256, 185))
        except pygui.ImageNotFoundException:
            continue
        except IOError:
            name = name.replace(" ", "-")  # Attempt to fix wrong text recognition
            try:
                pygui.locate(r'.\screenshots\weapon_image.png',
                             f'.\\weapons\\{name.replace('/', '[S]')}.png',
                             confidence=0.8, region=(0, 0, 256, 185))
            except pygui.ImageNotFoundException:
                continue
            except IOError:
                print(f'NameError: weapon name {name} was incorrect. Try to increase game resolution and retry')
                break

        print(name)

if __name__ == '__main__':
    if not os.access(r'.\weapons', os.F_OK):
        print('Downloading missing weapons...')
        os.mkdir(r'.\weapons')
        run_downloading()
    print("Press Q to get the current quiz answer")
    keyboard.add_hotkey('q', main)
    keyboard.wait()
