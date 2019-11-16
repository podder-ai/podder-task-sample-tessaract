from pathlib import Path
from typing import Any

from podder_task_foundation import Context, Task as BaseTask

from .ocr import TextReader


class Task(BaseTask):
    """
    Concrete task class.
    """

    def initialize(self, context: Context) -> None:
        context.logger.debug("Start Initializing...")
        self._reader = TextReader(context.config)

    def execute_file(self, file_path: str, context: Context) -> Any:
        """
        Concrete execute method.
        Notes
        -----
        1. Logging:
            You can output logs with `self.logger`.
            (e.g.) self.context.logger.debug("logging output")
        2. File Path:
            You can get absolute path to `data` directory by `self.context.file.get_data_path`.
            Please put your data or saved_models under `data` directory.
            Also your can use `self.context.file.get_tmp_path` to get absolute path to `tmp` directory.
            (e.g.) self.context.file.get_tmp_path('sample.csv')
        """
        context.logger.debug("Start executing...")
        context.logger.debug("inputs: {}".format(file_path))

        # Add your code here
        print("Process file:" + file_path)

        texts = self._reader.get_text(file_path)
        output_file_path = Path(file_path).name + '.txt'
        context.file.write_text_to_output_file(output_file_path, "\n".join(texts))

        outputs = output_file_path
        context.logger.debug("outputs: {}".format(outputs))
        context.logger.debug("Complete executing.")
        return outputs
