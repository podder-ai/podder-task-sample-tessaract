import cv2
import numpy as np
from PIL import Image, ImageEnhance
from podder_task_foundation.config import Config


class Preprocessor(object):
    def __init__(self, config: Config):
        self._config = config

    def preprocess(self, image):

        if image.mode != 'P':
            con12 = ImageEnhance.Sharpness(image)
            image = con12.enhance(1.5)

        cv_image = self._pil_to_cv(image)

        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        result, new_cv_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
        preprocessed_image = self._cv_to_pil(new_cv_image)

        return preprocessed_image

    # Ref: https://qiita.com/derodero24/items/f22c22b22451609908ee
    @staticmethod
    def _pil_to_cv(pil_image):
        cv_image = np.array(pil_image, dtype=np.uint8)
        if cv_image.ndim == 2:
            pass
        elif cv_image.shape[2] == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        elif cv_image.shape[2] == 4:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGBA2BGRA)

        return cv_image

    @staticmethod
    def _cv_to_pil(cv_image):
        pil_image = cv_image.copy()
        if pil_image.ndim == 2:
            pass
        elif pil_image.shape[2] == 3:
            pil_image = cv2.cvtColor(pil_image, cv2.COLOR_BGR2RGB)
        elif pil_image.shape[2] == 4:
            pil_image = cv2.cvtColor(pil_image, cv2.COLOR_BGRA2RGBA)
        pil_image = Image.fromarray(pil_image)

        return pil_image
