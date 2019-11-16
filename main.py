import uuid

from app.task import Task
from podder_task_foundation import MODE

DAG_ID = "___dag_id___"


def main() -> None:
    task = Task(MODE.CONSOLE)
    job_id = str(uuid.uuid1())
    task.handle(job_id, DAG_ID)


if __name__ == "__main__":
    main()
