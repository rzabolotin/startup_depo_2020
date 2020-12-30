import os

import pytesseract

PROGRAM_NAME = "Defect detector"
DATA_FOLDER = r"4. GUI application\data"
IMAGES_FOLDER = os.path.join(DATA_FOLDER, "images")
IMAGES_NN_FOLDER = os.path.join(DATA_FOLDER, "images_nn")

PATH_TO_MODEL = "data/model_final.pth"
NUM_CLASSES = 4

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(IMAGES_NN_FOLDER, exist_ok=True)