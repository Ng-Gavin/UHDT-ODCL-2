from PIL import Image
from pathlib import Path
from AlphaNumbericFucntionV2 import image2textConf
from time import sleep
import pytesseract
import cv2

#get the path/directory; replace name in quotes with file/directory name
folder_dir = 'UHDTr1-ground-truth'
#from website https://www.geeksforgeeks.org/how-to-iterate-through-images-in-a-folder-python/
#consider https://www.geeksforgeeks.org/python-ocr-on-all-the-images-present-in-a-folder-simultaneously/

alphnums = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#This creates array to hold images. replace .jpg with whatever format neccesary (will need to find way to address all types of images)
images = [str(x) for x in Path(folder_dir).glob('*.png')]
totalpics = len(images)

tallycorrect = 0
for file in images:
    #cut off the folder path with [20:]
    img = (str(file))
    if (img[20] in alphnums):
        print(image2textConf(img),img[20])
        if image2textConf(img)[0] == img[20]:
            #print("FINALLY")
            tallycorrect+=1
    sleep(0.5)
#general accuracy of entire set of images
print(f"The amount correct: {tallycorrect}, out of {totalpics}. An accuracy of {(tallycorrect/totalpics)*100:.2f}%")
    
