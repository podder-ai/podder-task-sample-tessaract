from pathlib import Path

import pytesseract
from PIL import ImageEnhance
from podder_task_foundation.config import Config
from podder_task_foundation.exceptions import PodderTaskException

from .image_converter import ImageConverter


class TextReader(object):
    def __init__(self, config: Config):
        self._config = config

    def get_text(self, image_file: str):
        texts = []
        source_file = Path(image_file)
        images = ImageConverter(source_file).convert()

        if len(images) > 0:
            language = self._config.get('ocr.language', 'eng')
            print("Language: " + language)

            for image in images:
                con12_image = image
                if image.mode != 'P':
                    con12 = ImageEnhance.Sharpness(image)
                    con12_image = con12.enhance(1.5)

                raw_text = pytesseract.image_to_string(
                    con12_image,
                    lang=language,
                    config='--psm ' + str(self._config.get('ocr.psm', 6)))
                texts.extend(raw_text.split("\n"))
        else:
            raise PodderTaskException(
                "Unsupported File Type", "This task can accept PDF, TIFF, JPEG, PNG only",
                "Check your input file and convert it into the supported file types.")

        return texts
