from ultralytics import YOLO
import supervision as sv
import os
import time
import numpy as np
import cv2
from sahi.utils.yolov8 import download_yolov8s_model
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from pathlib import Path
from PIL import Image


detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path='weight/nanotarget1.pt',
    confidence_threshold=0.3,
    device='cuda:0'
)

dir = "FlightTests/Positive"
start_time = time.time()
for files in os.listdir(dir):
    image = Image.open(f"{dir}/{files}")
    result = get_sliced_prediction(
        image,
        detection_model,
        slice_height=640,
        slice_width=640,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0.2
    )

    #Crops target from image
    for i in range(len(result.object_prediction_list)):
        BB = result.object_prediction_list[0].bbox.to_voc_bbox()
        print(BB)
        name, fext = os.path.splitext(f"{files}")
        cropped = image.crop((BB[0], BB[1], BB[2], BB[3]))
        cropped.save(f"results/{name}cropped.jpg")
            
    #result.export_visuals(export_dir="results/", file_name=f"{name}") #Saves whole image with bounding box labeled
end_time = time.time()
print(f"Runtime:",end_time - start_time)
