from ultralytics import YOLO
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
    model_path='weight/nanoshape1.pt',
    confidence_threshold=0.4,
    device='cuda:0'
)

def ObjectDetection(image):
    image = Image.open(image)
    result = get_sliced_prediction(
        image,
        detection_model,
        slice_height=640,
        slice_width=640,
        overlap_height_ratio=0.11,
        overlap_width_ratio=0.11
    )

    return result