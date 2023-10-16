import cv2
import re
import pytesseract
from pytesseract import Output
from PIL import Image


custom_config = ("-c tessedit"
                  "_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                  " --psm 13"
                  " -l UHDT4"
                  " ")


#this function just returns the letter/characters that the model thinks it is
def image2text(img):
    letter=pytesseract.image_to_string(img, config=custom_config)
    return letter

#this fucntion returns an array with the the letter as the first value and the confidence value as the 2nd value
def image2textConf(img):
    text = []
    results=pytesseract.image_to_data(img, config=custom_config, output_type=Output.DICT)
    text.append(results["text"][len(results["text"])-1])
    text.append(results["conf"][len(results["text"])-1])
    return text

#this function zooms in to the iamge to get a better result from the alphanumeric
#for the small targets, i liked a zoom of 2, 
#for the large targets i like 1.5, you can play around with the zoom value
def zoom_at(img, zoom=1, angle=0, coord=None):
    
    cy, cx = [ i/2 for i in img.shape[:-1] ] if coord is None else coord[::-1]
    
    rot_mat = cv2.getRotationMatrix2D((cx,cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    
    return result




