import numpy as np
import colorsys
import os
from nets import ssd
import tensorflow as tf
#from tensorflow.keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import preprocess_input

from utils.utils import BBoxUtility, letterbox_image, ssd_correct_boxes
from PIL import Image, ImageFont, ImageDraw


# --------------------------------------------#
#   使用自己训练好的模型预测需要修改2个参数
#   model_path和classes_path都需要修改！
# --------------------------------------------#
class SSD(object):
    _defaults = {

        "model_path": r'C:\\Users\\cuime\\Desktop\\yolov5_7_eye\\yolov5-7.0\\model_data\\eye_model.h5',
        # "model_path": 'model_data/ep441-loss2.244-val_loss1.994.h5',
        "classes_path": r'C:\\Users\\cuime\Desktop\\yolov5_7_eye\\yolov5-7.0\\model_data\\voc_classes.txt',
        "model_image_size": (512, 512, 3),
        "confidence": 0.4,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    # ---------------------------------------------------#
    #   初始化ssd
    # ---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        self.class_names = self._get_class()
        self.generate()
        self.bbox_util = BBoxUtility(self.num_classes)

    # ---------------------------------------------------#
    #   获得所有的分类
    # ---------------------------------------------------#
    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    # ---------------------------------------------------#
    #   获得所有的分类
    # ---------------------------------------------------#
    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # 计算总的种类
        self.num_classes = len(self.class_names) + 1

        # 载入模型
        input_shape = (512, 512, 3)
        tf.compat.v1.disable_eager_execution()
        self.ssd_model = ssd.SSD300(input_shape, self.num_classes)
        self.ssd_model.load_weights(self.model_path, by_name=True)

        self.ssd_model.summary()
        # self.ssd_model.run_eagerly = True
        print('{} model, anchors, and classes loaded.'.format(model_path))

        # 画框设置不同的颜色
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

    # ---------------------------------------------------#
    #   检测图片
    # ---------------------------------------------------#
    def detect_image(self, image):
        image_shape = np.array(np.shape(image)[0:2])
        crop_img, x_offset, y_offset = letterbox_image(image, (self.model_image_size[0], self.model_image_size[1]))
        photo = np.array(crop_img, dtype=np.float64)

        # 图片预处理，归一化
        photo = preprocess_input(np.reshape(photo, [1, self.model_image_size[0], self.model_image_size[1], 3]))
        preds = self.ssd_model.predict(photo)

        # 将预测结果进行解码
        results = self.bbox_util.detection_out(preds, confidence_threshold=self.confidence)

        if len(results[0]) <= 0:
            return image

        # 筛选出其中得分高于confidence的框
        det_label = results[0][:, 0]
        det_conf = results[0][:, 1]
        det_xmin, det_ymin, det_xmax, det_ymax = results[0][:, 2], results[0][:, 3], results[0][:, 4], results[0][:, 5]

        # 仅保留置信度最高的检测结果
        max_index = np.argmax(det_conf)
        max_conf = det_conf[max_index]
        max_label = det_label[max_index]
        max_xmin, max_ymin, max_xmax, max_ymax = det_xmin[max_index], det_ymin[max_index], det_xmax[max_index], \
                                                 det_ymax[max_index]

        # 去掉灰条
        # 去掉灰条
        boxes = ssd_correct_boxes(
            np.array([max_ymin])[:, np.newaxis],
            np.array([max_xmin])[:, np.newaxis],
            np.array([max_ymax])[:, np.newaxis],
            np.array([max_xmax])[:, np.newaxis],
            np.array([self.model_image_size[0], self.model_image_size[1]]),
            image_shape
        )
        font = ImageFont.truetype(font='model_data/simhei.ttf',
                                  size=np.floor(3e-2 * np.shape(image)[1] + 0.5).astype('int32'))

        thickness = (np.shape(image)[0] + np.shape(image)[1]) // self.model_image_size[0]

        predicted_class = self.class_names[int(max_label) - 1]
        score = max_conf

        top, left, bottom, right = boxes[0]
        top = top - 5
        left = left - 5
        bottom = bottom + 5
        right = right + 5

        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(np.shape(image)[0], np.floor(bottom + 0.5).astype('int32'))
        right = min(np.shape(image)[1], np.floor(right + 0.5).astype('int32'))

        # 画框框
        label = '{} {:.2f}'.format(predicted_class, score)
        draw = ImageDraw.Draw(image)
        label_size = draw.textsize(label, font)
        label = label.encode('utf-8')
        print(label)

        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[int(max_label) - 1])
        draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=self.colors[int(max_label) - 1])
        draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
        del draw
        return image

    def close_session(self):
        self.sess.close()
