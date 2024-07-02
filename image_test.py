import pyautogui as pygui

name = "WEAPON_NAME"
print(pygui.locate(r'.\screenshots\weapon_image.png',  # Compare last saved gun image with other guns images
                   f'.\\weapons\\{name.replace('/', '[S]')}.png',
                   confidence=0.95, region=(0, 0, 256, 185), grayscale=True))
