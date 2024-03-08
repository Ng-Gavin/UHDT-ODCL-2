from ultralytics import YOLO
import os, sys, glob, cv2
import numpy as np
model_path = sys.argv[1]
test_folder_path = sys.argv[2]
print(test_folder_path)
test_images = glob.glob(os.path.join(".", test_folder_path, "*.jpg"))
print(test_images)
test_images_cv = []
model = YOLO(model_path)
i = 0
while i < 100:
    test_image = test_images[i]
    tested_image = cv2.imread(test_image)
    tested_image = cv2.cvtColor(tested_image, cv2.COLOR_BGR2GRAY)
    tested_image = cv2.cvtColor(tested_image, cv2.COLOR_GRAY2BGR)
    #cv2.imshow('test', tested_image)
    #v2.waitKey(0)
    #cv2.destroyAllWindows()
    i += 1
    test_images_cv.append(tested_image)
results = model.predict(test_images_cv, stream=False, save=True, imgsz=320)#visualize=True)

#result = results[0]
#masks = result.masks
#print(len(masks))
#mask1 = masks[0]
#mask = mask1.data[0].numpy()
#boxes = result.boxes.data
#clss = boxes[]


"""
for result in results:
    #masks = result.masks
    print("start")
    #print(masks)
    #print(result.names)
    #print(result.boxes)
    #print(result.probs)
    print("end")
    #result.show()
"""

