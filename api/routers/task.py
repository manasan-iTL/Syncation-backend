from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.task as task_schema
import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
  return await task_crud.get_tasks_with_done(db)

@router.post("/{user_id}/tasks", response_model=task_schema.TaskCreateResponse)
async def create_tasks(
  user_id: str ,task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
  return await task_crud.create_task(user_id, db, task_body)

@router.put("/{user_id}/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    user_id: str, task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, user_id=user_id, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_crud.update_task(db, task_body, original=task)

@router.delete("/{user_id}/tasks/{task_id}", response_model=None)
async def delete_task(user_id: str, task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, user_id=user_id, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)