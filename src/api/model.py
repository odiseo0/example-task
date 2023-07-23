from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    service_name = Column(String)
    path = Column(String)
    response_time = Column(BIGINT)
    date_added = Column(DateTime, nullable=False, default=datetime.now)
