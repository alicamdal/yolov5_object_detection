import cv2
import torch
import torch.backends.cudnn as cudnn
from utils.augmentations import letterbox
from models.common import DetectMultiBackend
from utils.general import (non_max_suppression, scale_coords, xyxy2xywh)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
import numpy as np


class object_detect:
    def __init__(self):
        self.weights = "yolov5s6_r2.pt" # Model Weight Path
        self.device = select_device('0') # Select CUDA Device
        self.model = DetectMultiBackend(self.weights, device=self.device, dnn=False) # Read Model Properties
        self.stride, self.names, self.pt, self.jit, self.onnx, self.engine = self.model.stride, self.model.names, self.model.pt, self.model.jit, self.model.onnx, self.model.engine

        self.half = False # Half Precision Flag
        self.half &= (self.pt or self.jit or self.engine) and self.device.type != 'cpu' # Half Precision can be performed only on CUDA
        if self.pt or self.jit:
            self.model.model.half() if self.half else self.model.model.float()
        cudnn.benchmark = True
        self.model.warmup(imgsz=(16, 3, 640,640), half=self.half) # Model Warm up

    @torch.no_grad()
    def detect(self, frame):
        # frame preprocessing
        self.frame = cv2.resize(frame,(384,480))
        self.img0 = self.frame.copy()
        self.img = [letterbox(self.img0, (384, 480), self.stride, True)[0]]
        self.img = np.stack(self.img,0)
        self.img = self.img[..., ::-1].transpose((0, 3, 1, 2))
        self.img = np.ascontiguousarray(self.img)
        # pushing data to selected device
        self.img = torch.from_numpy(self.img).to(self.device)
        self.img = self.img.half() if self.half else self.img.float()
        self.img /= 255
        if len(self.img.shape) == 3:
            self.img = self.img[None]
        # perform prediction on frame
        self.pred = self.model(self.img, augment=False, visualize=False)
        self.pred = non_max_suppression(self.pred, 0.25, 0.25, 0, False, max_det=10)
        for i, det in enumerate(self.pred):                    
            self.annotator = Annotator(self.img0, line_width=2, example=str(self.names))
            if len(det):
                det[:, :4] = scale_coords(self.img.shape[2:], det[:, :4], self.img0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    names = ["trash"] # class names
                    label = None if False else (names[c] if False else f'{names[c]} {conf:.2f}')
                    self.annotator.box_label(xyxy, label, color=colors(c, True))
            self.img0 = self.annotator.result()
        return self.img0
