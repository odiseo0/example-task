from contextlib import contextmanager
from typing import Any

from sqlalchemy import Executable
from sqlalchemy import func as sql_func
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Metric
from .schemas import MetricCreate


@contextmanager
def catch_sqlalchemy_exception() -> Any:
    """Catch `SQLAlchemyError` to handle it."""
    try:
        yield
    except (IntegrityError, SQLAlchemyError) as e:
        raise Exception() from e
    

async def execute(db: AsyncSession, stmt: Executable):
    with catch_sqlalchemy_exception():
        return await db.execute(stmt)


async def get_metrics(db: AsyncSession) -> dict[str, Any]:
    """Read all the metrics grouped by path"""
    stmt = select(
        Metric.path, 
        sql_func.avg(Metric.response_time).label("avg"), 
        sql_func.min(Metric.response_time).label("min"), 
        sql_func.max(Metric.response_time).label("max")
    ).group_by(Metric.path)

    results = await execute(db, stmt)

    return results.unique().all()


async def create_metric(db: AsyncSession, obj: MetricCreate) -> Metric:
    obj_dict = obj.model_dump(mode="json", by_alias=False)
    db_obj = Metric(**obj_dict)

    db.add(db_obj)
    
    await db.commit()
    await db.refresh(db_obj)

    return db_obj
