import json
from pydantic import parse_file_as
from typing import List, Optional

from model.model import Task, TaskList


filepath = 'data/tasks.json'


async def data_to_json(data: List):
    data = json.dumps(data)
    with open(filepath, 'w') as file:
        file.write(data)


async def get_tasks(id: Optional[int]):
    tasks = parse_file_as(List[TaskList], filepath)
    data = {task.id: task.sict() for task in tasks}
    response = data if id == 0 else data[id]
    return response


async def create_task(new_task: Task):
    tasks = parse_file_as(List[TaskList], filepath)
    new_id = max([task.id for task in tasks]) + 1
    tasks.append(TaskList(id=new_id, task=new_task))
    data = [task.dict() for task in tasks]
    await data_to_json(data)
    return new_id


async def delete_task(id: int):
    tasks = parse_file_as(List[TaskList], filepath)
    tasks = [task for task in tasks if task.id != id]
    data = [task.dict() for task in tasks]
    await data_to_json(data)
    return id


async def update_task(id: int, new_task: Task):
    tasks = parse_file_as(List[TaskList], filepath)
    data = [task.dict() for task in tasks]
    for task in data:
        if task.id == id:
            task.task = new_task.dict()
    await data_to_json(data)
    return id
