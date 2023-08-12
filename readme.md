pyinstaller --hiddenimport cv2 main.py -n myApp --onefile --add-data="./haarcascade_frontalface_default.xml;." --onefile


test