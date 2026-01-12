from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
import logging
from ..database import get_db_session
from ..middleware.auth import get_current_user
from ..models.user import User
from ..models.task import TaskCreate, TaskUpdate
from ..schemas.task import TaskResponse
from ..services.task_service import TaskService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Get all tasks for the current user"""
    try:
        logger.info(f"Retrieving tasks for user ID: {current_user.id}")
        tasks = TaskService.get_tasks_by_user(db_session, current_user.id)
        logger.info(f"Retrieved {len(tasks)} tasks for user: {current_user.id}")
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tasks"
        )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Create a new task for the current user"""
    try:
        logger.info(f"Creating new task for user ID: {current_user.id}")

        # Validate title length
        if len(task_create.title) < 1 or len(task_create.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be 1-200 characters"
            )

        # Validate description length if provided
        if task_create.description and len(task_create.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be 1000 characters or less"
            )

        task = TaskService.create_task(db_session, task_create, current_user.id)
        logger.info(f"Successfully created task ID: {task.id} for user: {current_user.id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task"
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Get a specific task by ID"""
    try:
        logger.info(f"Retrieving task ID: {task_id} for user ID: {current_user.id}")
        task = TaskService.get_task_by_id(db_session, task_id, current_user.id)

        if not task:
            logger.warning(f"Task not found - ID: {task_id} for user: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully retrieved task: {task.id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the task"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Update a task"""
    try:
        logger.info(f"Updating task ID: {task_id} for user ID: {current_user.id}")

        # Validate title length if provided
        if task_update.title is not None:
            if len(task_update.title) < 1 or len(task_update.title) > 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title must be 1-200 characters"
                )

        # Validate description length if provided
        if task_update.description is not None and len(task_update.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be 1000 characters or less"
            )

        task = TaskService.update_task(db_session, task_id, task_update, current_user.id)

        if not task:
            logger.warning(f"Update failed - Task not found: {task_id} for user: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully updated task: {task.id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task"
        )


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Toggle the completion status of a task"""
    try:
        logger.info(f"Toggling completion for task ID: {task_id} for user ID: {current_user.id}")
        task = TaskService.toggle_task_completion(db_session, task_id, current_user.id)

        if not task:
            logger.warning(f"Toggle failed - Task not found: {task_id} for user: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully toggled task {task.id} completion status")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error toggling task {task_id} completion for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while toggling the task completion status"
        )


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Delete a task"""
    try:
        logger.info(f"Deleting task ID: {task_id} for user ID: {current_user.id}")
        success = TaskService.delete_task(db_session, task_id, current_user.id)

        if not success:
            logger.warning(f"Delete failed - Task not found: {task_id} for user: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully deleted task: {task_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the task"
        )