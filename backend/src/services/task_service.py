from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import logging
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskService:
    @staticmethod
    def create_task(db_session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
        """Create a new task for a user"""
        logger.info(f"Creating new task for user ID: {user_id}")

        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            user_id=user_id
        )

        db_session.add(db_task)
        db_session.commit()
        db_session.refresh(db_task)

        logger.info(f"Successfully created task with ID: {db_task.id} for user: {user_id}")

        return db_task

    @staticmethod
    def get_tasks_by_user(db_session: Session, user_id: UUID) -> List[Task]:
        """Get all tasks for a specific user"""
        logger.info(f"Retrieving tasks for user ID: {user_id}")

        tasks = db_session.exec(
            select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        ).all()

        logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")
        return tasks

    @staticmethod
    def get_task_by_id(db_session: Session, task_id: int, user_id: UUID) -> Optional[Task]:
        """Get a specific task by ID for a user (enforces user isolation)"""
        logger.info(f"Retrieving task ID: {task_id} for user ID: {user_id}")

        task = db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if task:
            logger.info(f"Successfully retrieved task: {task.id}")
        else:
            logger.warning(f"Task not found - ID: {task_id} for user: {user_id}")

        return task

    @staticmethod
    def update_task(db_session: Session, task_id: int, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
        """Update a task for a user"""
        logger.info(f"Updating task ID: {task_id} for user ID: {user_id}")

        task = TaskService.get_task_by_id(db_session, task_id, user_id)

        if not task:
            logger.warning(f"Update failed - Task not found: {task_id} for user: {user_id}")
            return None

        # Log the fields being updated
        update_data = task_update.model_dump(exclude_unset=True)
        logger.info(f"Updating task {task_id} with data: {update_data}")

        # Update only the fields that are provided
        for field, value in update_data.items():
            setattr(task, field, value)

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        logger.info(f"Successfully updated task: {task.id}")
        return task

    @staticmethod
    def toggle_task_completion(db_session: Session, task_id: int, user_id: UUID) -> Optional[Task]:
        """Toggle the completion status of a task"""
        logger.info(f"Toggling completion for task ID: {task_id} for user ID: {user_id}")

        task = TaskService.get_task_by_id(db_session, task_id, user_id)

        if not task:
            logger.warning(f"Toggle completion failed - Task not found: {task_id} for user: {user_id}")
            return None

        old_status = task.completed
        task.completed = not task.completed

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        logger.info(f"Successfully toggled task {task.id} completion from {old_status} to {task.completed}")
        return task

    @staticmethod
    def delete_task(db_session: Session, task_id: int, user_id: UUID) -> bool:
        """Delete a task for a user"""
        logger.info(f"Deleting task ID: {task_id} for user ID: {user_id}")

        task = TaskService.get_task_by_id(db_session, task_id, user_id)

        if not task:
            logger.warning(f"Delete failed - Task not found: {task_id} for user: {user_id}")
            return False

        db_session.delete(task)
        db_session.commit()

        logger.info(f"Successfully deleted task: {task_id}")
        return True