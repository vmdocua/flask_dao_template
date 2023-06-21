import logging
import logging.config
import datetime
import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from sqlalchemy import MetaData, Table, Column, Integer, Numeric, String, DateTime, \
    ForeignKey, Float, Boolean
from sqlalchemy.orm import as_declarative

logger = logging.getLogger(__name__)


############################################
# Model/DTO

# base class for all DTOs
class BaseDTO:
    def __init__(self):
        pass


# base class for all entity ORM based DTOs
# the same as EntityDTO = declarative_base(cls=BaseDTO)
@as_declarative()
class EntityDTO(BaseDTO):
    def __init__(self):
        pass

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


@dataclass_json
@dataclass
class AnimalInfoDTO(BaseDTO):
    id: int = 0
    kind: str = None
    nickname: str = None
    is_hungry: str = 'N'
    last_feed_on: datetime.datetime = None


class AnimalDTO(EntityDTO):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True)
    kind = Column(String)
    nickname = Column(String)
    color = Column(String)
    weight_kg = Column(Float)
    is_hungry = Column(String)
    last_feed_on = Column(DateTime())
    created_on = Column(DateTime())
    updated_on = Column(DateTime())

    def __repr__(self):
        return "AnimalDTO(id={self.id}, " \
               "kind='{self.kind}', " \
               "nickname='{self.nickname}', " \
               "color={self.color}, " \
               "weight_kg={self.weight_kg}, " \
               "is_hungry={self.is_hungry}, " \
               "last_feed_on={self.last_feed_on}, "\
               "created_on={self.created_on}, " \
               "updated_on={self.updated_on}')".format(self=self)
