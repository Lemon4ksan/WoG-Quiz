import pyautogui as pygui

name = "WEAPON_NAME"
print(pygui.locate(r'.\screenshots\weapon_image.png',
                   f'.\\weapons\\{name.replace('/', '[S]')}.png',
                   confidence=0.955, region=(0, 0, 256, 185), grayscale=True))
