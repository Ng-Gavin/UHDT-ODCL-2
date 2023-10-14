from PIL import Image
from pathlib import Path
import pytesseract
import cv2

#get the path/directory
folder_dir = 'test_pngs'
#from website https://www.geeksforgeeks.org/how-to-iterate-through-images-in-a-folder-python/
#consider https://www.geeksforgeeks.org/python-ocr-on-all-the-images-present-in-a-folder-simultaneously/

#find way to replace this array with an actual way to iterate through files.
#temp_array = ['a_test_3_blur_20_r12.jpg','a_Test.png','a_Test_2.png','a_test_3.jpg','Upper_Ariel_Q.jpg','B_test_1.png','R_real_test_1.png','4_test_2.png']

images = Path(folder_dir).glob('*.png')
#function to read words off image (we need to try and get individual letters)
for file in images:
    img = str(file)
    def read_img(img):
        #custom_config = r' --oem 10, --psm 6'
        custom_config = r'--psm 10 --oem 3'
        print(pytesseract.image_to_string(Image.open(img),config=custom_config))
        #loop through a bunch of images (preferably font images)
    read_img(img)

#img= 'a_test_3.jpg'


    

#create way to compare output with actual expected letter.