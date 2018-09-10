# _*_ coding:utf-8 _*_
__author__ = 'jiangchao'
__date__ = '2018/8/13 0013 下午 2:07'
import os.path as ops
import turicreate as tc

from robo_dl_api.settings import BASE_DIR


class TurApi(object):

    def __init__(self):
        self.tc = tc
        self.tc.config.set_num_gpus(0)
        self.model = self.loads()
        self._predict = None

    @staticmethod
    def loads():
        model_path = ops.join(ops.join(BASE_DIR, 'core/turi_models'), 'welding')
        return tc.load_model(model_path)

    def predict(self, file_path):
        data = self.tc.image_analysis.load_images(file_path, with_path=True)
        self._predict = self.model.predict(data)
        print(self._predict)
        return self.transfer_pos()

    def transfer_pos(self):
        """转换坐标"""
        data = []
        if len(self._predict) <= 0:
            print(self._predict)
            return []
        for _predict in self._predict[0]:
            print(_predict)
            y = float(_predict['coordinates']['y'])
            x = float(_predict['coordinates']['x'])
            w = float(_predict['coordinates']['width'])
            h = float(_predict['coordinates']['height'])
            xmin = int((2 * x - w) / 2)
            ymin = int((2 * y - h) / 2)
            xmax = int((2 * x + w) / 2)
            ymax = int((2 * y + h) / 2)
            data.append({
                "coordinates": {
                    "xmin": xmin,
                    "ymin": ymin,
                    "xmax": xmax,
                    "ymax": ymax,
                },
                "label": _predict["label"],
                "type": "rectangle"
            })
        return data
