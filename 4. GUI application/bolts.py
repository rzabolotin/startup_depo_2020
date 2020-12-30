import cv2
from detectron2 import model_zoo
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

import config


cfg = get_cfg()

cfg.MODEL.DEVICE='cpu'

cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = config.PATH_TO_MODEL
cfg.MODEL.ROI_HEADS.NUM_CLASSES = config.NUM_CLASSES

predictor = DefaultPredictor(cfg)


def visualize_dl_predictios(inp_image):

    outputs = predictor(inp_image)
    v = Visualizer(inp_image[:, :, ::-1],
                scale=0.8,
                instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
    )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    return cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB)





