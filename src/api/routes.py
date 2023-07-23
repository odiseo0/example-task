from fastapi import APIRouter

from ..core import GetDatabase
from .schemas import MetricCreate, MetricResponse
from .use_cases import create_metric, get_metrics


api = APIRouter(tags=["Metrics"])


@api.get("/", responses={200: {"model": list[MetricResponse]}})
async def read_metrics(db: GetDatabase):
    results = await get_metrics(db)
    return [MetricResponse(path=result[0], average=result[1], min=result[2], max=result[3]).model_dump(mode="json") for result in results]


@api.post("/", status_code=201)
async def add_metrics(db: GetDatabase, obj: MetricCreate):
    return await create_metric(db, obj)
