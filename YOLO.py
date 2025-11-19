from maix import nn,image
import os
from UART import UART
class YOLO:
    def __init__(self):
        self.model_path = "model_243032.mud"
        if not os.path.exists(self.model_path):
            self.model_path = "/root/models/maixhub/243032/model_243032.mud"

        self.detector = nn.YOLOv5(model=self.model_path)
        self.Num = 0
    def detect_figure(self,img):
        # self.Num = 0
        # 数字识别
        model_img = img.copy()  # 复制原始图像
        model_img.resize(self.detector.input_width(), self.detector.input_height())  # 缩放到模型尺寸
        objs = self.detector.detect(model_img, conf_th=0.5, iou_th=0.45)

        for obj in objs:
            # x, y, w, h = scale_coords(obj.x, obj.y, obj.w, obj.h)
            x, y, w, h = obj.x, obj.y, obj.w, obj.h
            img.draw_rect(x, y, w, h, color=image.COLOR_RED)
            msg = f'{self.detector.labels[obj.class_id]}: {obj.score:.2f}'
            img.draw_string(x, y, msg, color=image.COLOR_RED)
            label = self.detector.labels[obj.class_id]
            # labels = 3, 4
            if label:  # 确保标签非空
                self.Num = label[0]  # 取标签的第一个字符 8
                if label[0] == ' ':
                    self.Num = label[1]
                # if(self.Num == '4'):print(self.Num)