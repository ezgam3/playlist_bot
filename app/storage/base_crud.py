import json
from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.storage.base import BaseClass

ModelType = TypeVar("ModelType", bound=BaseClass)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD base with default methods (C)reate, (R)ead, (U)pdate, (D)elete
        Args:
            model: SQLAlhemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Get a model instance from by ID
        Args:
            db: Database connection
            id: unique id in the database
        Returns:
            Model instance
        """
        return await db.get(self.model, id)

    async def get_multi(
        self, db: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """
        Get multiple model instances from database, may use for pagination
        Args:
            db: Database connection
            offset: database query offset
            limit: database query limit
        Returns:
            List of model instances
        """
        query = select(self.model).offset(offset).limit(limit)
        result = await db.scalars(query)
        return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new model instance in database
        Args:
            db: Database connection
            obj_in: CreateSchema instance
        Returns:
            Model instance
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update a model instance in database
        Args:
            db: Database connection
            db_obj: Database object
            obj_in: UpdateSchema instance
        Returns:
            Model instance
        """
        obj_data = json.dump(obj_in)
        update_data = obj_in.dict()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Remove a model instance in database
        Args:
            id: ID of the model instance to remove
        Returns:
            Model instance
        """
        obj = await db.get(self.model, id)
        await db.delete(obj)
        await db.commit()
        return obj

    def _map_result_foo(self, row) -> list[ModelType]:
        """
        Map result to model instances
        Args:
            result: List of model instances
        Returns:
            List of model instances
        """
        return self.model(**row)
