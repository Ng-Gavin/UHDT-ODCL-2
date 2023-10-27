from PIL import Image
from pathlib import Path
from AlphaNumbericFucntionV2 import image2textConf
import pytesseract
import cv2

#get the path/directory; replace name in quotes with file/directory name
folder_dir = 'sans_export'

alphnums = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#This creates array to hold images. replace .jpg with whatever format neccesary (will need to find way to address all types of images)
images = [str(x) for x in Path(folder_dir).glob('*.png')]
numimages = len(images)
#variable to keep track of loop
timeslooped = 1
#create dictionary to hold the incorrect and correct outputs (equivalent of hashmap?)
CorOutputFreq= {}
IncOutputFreq = {}
#work in progress
letterFreq = {}

for file in images:
    #cut off the folder path with [12:]; the number (i.e. 12) depends on file names
    img = (str(file))
    #see if the labeled image is actually a test image (in this case the test images were all labeled for this algorithm)
    if (img[12] in alphnums):
        print(image2textConf(img),img[12:],timeslooped)
        #add the count of correct readings to each alphanumeric to a frequency map
        if image2textConf(img)[0] == img[12]:
            #if it already exists in the dictionary, add one
            if image2textConf(img)[0] in CorOutputFreq:
                CorOutputFreq[image2textConf(img)[0]] += 1
            #if it doesn't exist, add it to the dictionary and set it to 1
            else:
                CorOutputFreq[image2textConf(img)[0]] = 1
        #add the incorrect outputs (wrong char, number of times)
        else:
            #if incorrect value is already in there, add 1
            if image2textConf(img)[0] in IncOutputFreq:
                IncOutputFreq[image2textConf(img)[0]][1] += 1
            #if it doesn't exist in dictionary yet, add it there
            else:
                IncOutputFreq[image2textConf(img)[0]] = [img[12],1]
    #for testing purposes, in case you just need to see if a part of the code works without having to loop 12k times
    if timeslooped == 500:
        break

    timeslooped+=1
print(CorOutputFreq)
print(IncOutputFreq)
#to get overall accuracy:
numcorrect = [int(CorOutputFreq[num]) for num in CorOutputFreq]
totalnumcorrect = sum(numcorrect)
print(f'Overall Accuracy: {sum(numcorrect)/len(images)*100:.2f}%')
#to get individual accuracy (need to change code for 361. It wont always be 361)
for char in CorOutputFreq:
    print(f'Accuracy for "{char}" is {(CorOutputFreq[char]/361)*100:.2f}%')
    
