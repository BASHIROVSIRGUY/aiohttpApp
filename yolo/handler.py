import torch
from PIL import Image
from io import BytesIO


class ObjectDetecter:
    def __init__(self, yolo_version='m'):
        self.model = torch.hub.load('ultralytics/yolov5', f'yolov5{yolo_version}')

    def detect(self, img_byte, type='jpeg'):
        img = self._bin_decode(img_byte)
        results = self.model(img)
        results_array = results.render()
        result_img = Image.fromarray(results_array[0])
        result_img_byte = self._bin_encode(result_img, type)
        return result_img_byte

    def _bin_encode(self, img, type):
        img_byte = BytesIO()
        img.save(img_byte, format=type)
        return img_byte.getvalue()

    def _bin_decode(self, img_byte):
        img = Image.open(BytesIO(img_byte))
        return img
