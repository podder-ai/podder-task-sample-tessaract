from logging import getLogger

from ....app.task import Task
from podder_task_foundation import Context

logger = getLogger()


class TestTask:
    DAG_ID = "dag_id"
    JOB_ID = "job_id"
    INPUTS = [
        {
            "job_id": JOB_ID,
            "job_data": {
                "resources": ["input/data/sample1-page-1.pdf"],
                "params": {
                    "name": "John Doe",
                    "address": "Tokyo",
                    "text": "some text"
                }
            }
        }
    ]

    def test_if_execute_method_exist(self):
        context = Context(self.DAG_ID)
        task = Task(context)
        task.execute([])

    def test_outputs_outputs_length_over_one(self):
        context = Context(self.DAG_ID)
        task = Task(context)
        outputs = task.execute(self.INPUTS)
        assert isinstance(outputs, list)
        assert len(outputs) >= 1

    def test_outputs_contain_job_id(self):
        context = Context(self.DAG_ID)
        task = Task(context)
        outputs = task.execute(self.INPUTS)
        assert outputs[0]["job_id"] == self.JOB_ID

    def test_outputs_contain_job_data(self):
        context = Context(self.DAG_ID)
        task = Task(context)
        outputs = task.execute(self.INPUTS)
        assert outputs[0]["job_data"]
        assert isinstance(outputs[0]["job_data"], dict)

    def test_outputs_contain_params(self):
        context = Context(self.DAG_ID)
        task = Task(context)
        outputs = task.execute(self.INPUTS)
        assert outputs[0]["job_data"]["params"]

    def test_outputs_contain_resources(self):
        context = Context(self.DAG_ID)
        task = Task(context)
        outputs = task.execute(self.INPUTS)
        assert isinstance(outputs[0]["job_data"]["resources"], list)
