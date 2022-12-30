import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from model.model import Task
import model.task_handler as task_handler


app = FastAPI()


@app.get('/api/tasks')
async def get_tasks():
    return await task_handler.get_tasks()


@app.get('/api/tasks/{id}')
async def get_task(id: int):
    return await task_handler.get_tasks(id)


@app.post('/api/task/create')
async def create_task(new_task: Task):
    id = await task_handler.create_task(new_task)
    return await task_handler.get_tasks(id)


@app.put('/api/tasks/{id}/update')
async def update_task(id: int, task: Task):
    await task_handler.update_task(id, task)
    return await task_handler.get_tasks(id)


@app.delete('/api/tasks/{id}/delete')
async def dalete_task(id: int, task: Task):
    deleted_id = await task_handler.delete_task(id)
    response = {deleted_id: 'Task successfully deleted'}
    return jsonable_encoder(response)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
