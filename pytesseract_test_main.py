from PIL import Image
from pathlib import Path
from AlphaNumbericFucntionV2 import image2textConf
from time import sleep
import pytesseract
import cv2

#get the path/directory; replace name in quotes with file/directory name
folder_dir = 'sans_export'
#from website https://www.geeksforgeeks.org/how-to-iterate-through-images-in-a-folder-python/
#consider https://www.geeksforgeeks.org/python-ocr-on-all-the-images-present-in-a-folder-simultaneously/

alphnums = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#This creates array to hold images. replace .jpg with whatever format neccesary (will need to find way to address all types of images)
images = [str(x) for x in Path(folder_dir).glob('*.png')]
totalpics = len(images)
tallycorrect = 0
timeslooped = 0

for file in images:
    #cut off the folder path with [12:]; have to change the number depending on file names
    img = (str(file))
    if (img[12] in alphnums):
        print(image2textConf(img),img[12:],timeslooped)
        if image2textConf(img)[0] == img[12]:
            #print("FINALLY")
            tallycorrect+=1
    timeslooped+=1
    #sleep(0.5)
print(f"The amount correct: {tallycorrect}, out of {totalpics}. An accuracy of {(tallycorrect/totalpics)*100:.2f}%")
