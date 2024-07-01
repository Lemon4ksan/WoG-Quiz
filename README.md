# WoG-Quiz
Python script that allows to automatically complete World of Gun quizes.

## Requirements
- Tesseract
- Git
- Python (3.12)
- pip

## Installation

First, you need to install Tessercat-OCR (text recognition tool). Select 64 or 32 bit version, depending on your system.
You may leave checkboxes as they are.
```
https://github.com/UB-Mannheim/tesseract/wiki
```
Then clone this repository
```commandline
git clone https://github.com/Lemon4ksan/WoG-Quiz.git
```
Insert path to ```tesseract.exe``` in path.txt.
Example: ```C:\Program Files\Tesseract-OCR\tesseract.exe```

Install requirements
```commandline
pip install -r requirements.txt
```
Run the script by running the main.py file
```commandline
python main.py
```

## How to use it
- Run the script
- Open the game
- Change language to English
- Start the quiz
- Press Q and watch the show


## Updates
When game releases new weapon you should run download_weapons.py script to download new entries. 
(You'll probably have to wait for the guide's author to update it first.)

## Mentions
Thanks to this guide for providing the weapon images.: https://steamcommunity.com/sharedfiles/filedetails/?id=2589399401
Make sure to give it a like. 

## Contribution
Since text recognition isn't perfect, there may be incorrect results. I can't test all the weapons myself, 
so if you encounter this situation, add possible solution for the typo in main.py after the first ```except IOError:``` 
occurrence and create a pull request. It will help a lot (You should save the photo of the problematic quiz and test
your solution before submitting).

## Support
If you find this script helpful, you can send a small reward on my Steam account:
https://steamcommunity.com/profiles/76561199101344085/