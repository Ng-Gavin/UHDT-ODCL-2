import sys
import os

import cv2

#usage: use python3 labelingtool.py FILE_DIRECTORY
#or python labelingtoo.py FILE_DIRECTORY
#depending on your installation 
#where FILE_DIRECTORY is the location of where the files you want to generate the ground truth text file is located
#uses the first character of the image in order to write to the ground truth file what the file contains
def isImage(filepath) -> bool:
    '''
    checks if file is an image
    '''

    lowercasePath = filepath.lower()

    # you can add more formats here
    cases = [
        lowercasePath.endswith('jpg'),
        lowercasePath.endswith('png'),
        lowercasePath.endswith('jpeg'),
    ]

    return any(cases)



def getPaths(imgdir, condition=lambda x: True):
    '''
    given path to image folder will return you a list of full paths
    to files which this folder contain

    :param condition: is a function that will filter only those files
    that satisfy condition
    '''

    files = map(lambda x: os.path.join(imgdir, x).strip(),
        os.listdir(imgdir))

    filtered = filter(condition, files)

    return list(filtered)



def labelingProcess(imgdir):
    print("Welcome to the labeling tool")
    print("if you want to stop labeling just close the program or press ctrl+C")

    WIDTH = 600
    HEIGHT = 600


    pathsToImages = getPaths(imgdir, isImage)

    if not len(pathsToImages):
        print("couldn't find any images")
        return

    for pathtoimage in pathsToImages:
        imageName = os.path.basename(pathtoimage)

        # label img has the same name as image only ends with .txt
        labelName = ''.join(imageName.split('.')[:-1]) + '.gt.txt'
        labelPath = os.path.join(imgdir, labelName)

        # skip labeled images
        if os.path.exists(labelPath):
            continue

        # read image
        image = cv2.imread(pathtoimage)
        if image is None:
            print("couldn't open the image")
            continue

        h, w = image.shape[:2]

        label = imageName[0]

        if not len(label):
            continue


        with open(labelPath, 'w') as labelfile:
            labelfile.write(label)


if __name__ == '__main__':
    imgdir = sys.argv[1]
    labelingProcess(imgdir)