from pathlib import Path

import pytesseract
from podder_task_foundation.config import Config
from podder_task_foundation.exceptions import PodderTaskException

from .image_converter import ImageConverter
from .preprocessor import Preprocessor


class TextReader(object):
    def __init__(self, config: Config):
        self._config = config
        self._preprocessor = Preprocessor(config)

    def get_text(self, image_file: str) -> [str]:
        texts = []
        source_file = Path(image_file)
        images = ImageConverter(source_file).convert()

        if len(images) > 0:
            language = self._config.get('ocr.language', 'eng')
            print("Language: " + language)

            for image in images:

                image = self._preprocessor.preprocess(image)
                raw_text = pytesseract.image_to_string(
                    image, lang=language, config='--psm ' + str(self._config.get('ocr.psm', 6)))
                texts.extend(raw_text.split("\n"))
        else:
            raise PodderTaskException(
                "Unsupported File Type", "This task can accept PDF, TIFF, JPEG, PNG only",
                "Check your input file and convert it into the supported file types.")

        return texts
