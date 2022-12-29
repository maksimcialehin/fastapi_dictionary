from fastapi import FastAPI
from datetime import datetime
from typing import Optional
from fastapi.encoders import jsonable_encoder


app = FastAPI()


@app.get('/api/tasks')
async def get_tasks():
    pass


@app.get('/api/tasks/{id}')
async def get_task(id: int):
    pass


@app.post('/api/task/create')
async def create_task(task: Task):
    pass


@app.put('/api/tasks/{id}/update')
async def update_task(id: int, task: Task):
    pass


@app.delete('/api/tasks/{id}/delete')
async def dalete_task(id: int, task: Task):
    pass
