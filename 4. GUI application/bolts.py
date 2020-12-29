from detectron2.data.datasets import register_coco_instances

from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.engine import DefaultPredictor
import cv2
import matplotlib.pyplot as plt
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
import os

register_coco_instances(f"HackRZHD", {}, f"kyrill\\RZHD_data\\annotations.json", f"kyrill\\RZHD_data\\")


cfg = get_cfg()
# cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("HackRZHD",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
# cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025
cfg.SOLVER.MAX_ITER = 1000
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4

# os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)


cfg.MODEL.WEIGHTS = os.path.join(f"kyrill\\output\\", "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
# cfg.DATASETS.TEST = ("microcontroller_test", )
predictor = DefaultPredictor(cfg)


# dataset_dicts = get_microcontroller_dicts('Microcontroller Segmentation/test')
# for d in random.sample(dataset_dicts, 3):

im = cv2.imread("data2\\86.jpg")
outputs = predictor(im)
v = Visualizer(im[:, :, ::-1],
#                metadata=HackRZHD_metadata,
               scale=0.8,
               instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
)
v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
plt.figure(figsize = (14, 10))
plt.imshow(cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
plt.show()






