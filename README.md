# WoG-Quiz
Python script that allows to automatically complete World of Guns quizes.

## Demonstration
![](https://i.giphy.com/lhJjtCm0GcNwNtPGaA.webp)

## Requirements
- Tesseract
- Python (3.12)
- pip

## Installation

Download the latest release

Install Tessercat-OCR (text recognition tool). Select 64 or 32 bit version, depending on your system.
You may leave checkboxes as they are.

```
https://github.com/UB-Mannheim/tesseract/wiki
```

Insert path to ```tesseract.exe``` in path.txt.
Example: ```C:\Program Files\Tesseract-OCR\tesseract.exe```

Install requirements
```commandline
pip install -r requirements.txt
```
Start the script by running the main.py file
```commandline
python main.py
```

## How to use it
- Run the script
- Open the game
- Change language to English
- Start the quiz
- Press Q and watch the show

In addition, you can copy/paste images from ```missing_weapons``` folder in your ```weapons``` folder.

## Updates
When game releases new weapon you should run ```download_weapons.py``` script to download new entries. 
(You'll probably have to wait for the Steam guide's author to update it first.)

## Mentions
Thanks to this guide for providing the weapon images: https://steamcommunity.com/sharedfiles/filedetails/?id=2589399401
Make sure to give it a like. 
