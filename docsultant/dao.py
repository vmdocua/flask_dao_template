import logging
from typing import List
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from docsultant.model import AnimalDTO, AnimalInfoDTO

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


############################################
# DAO

class BaseDAO:
    default_session = None

    def __init__(self):
        pass

    def session(self):
        # logger.debug("session() "+str(self)+" = "+str(BaseDAO.default_session))
        return BaseDAO.default_session

    def to_dataclass(self, proxy, cls):
        if proxy:
            if isinstance(proxy, list):
                return [cls(**r._mapping) for r in proxy]
            return cls(**proxy._mapping)
        return None



# animal DAO
class AnimalDAO(BaseDAO):
    def __init__(self):
        pass

    # use ORM to get List
    def get_animals(self) -> List[AnimalDTO]:
        return self.session().query(AnimalDTO).all()

    # use ORM to get single entity
    def get_animal_by_id(self, id: int) -> AnimalDTO:
        return self.session().get(AnimalDTO, id)

    # use ORM to get animal by nickname filter
    def get_role_by_nickname(self, nickname: str) -> AnimalDTO:
        return self.session(). \
            query(AnimalDTO).filter(AnimalDTO.nickname == nickname).first()

    # use raw SQL to get List of animal info dataclass
    def get_animal_infos(self) -> List[AnimalInfoDTO]:
        res = self.session().execute(
            text("""
                select
                    id, 
                    kind, 
                    nickname,
                    is_hungry,
                    last_feed_on
                from 
                    animal    
            """
                 )
        ).all()
        return self.to_dataclass(res, AnimalInfoDTO)

    # use raw SQL to get List of animal info dataclass
    def get_animal_info_by_nickname(self, nickname: str) -> AnimalInfoDTO:
        res = self.session().execute(
            text("""
                select
                    id,
                    kind,
                    nickname,
                    is_hungry,
                    last_feed_on
                from
                    animal a
                where
                    a.nickname = :nickname
            """
                 ), {'nickname': nickname}
        ).first()
        return self.to_dataclass(res, AnimalInfoDTO)


# DAO factory
class DAO:
    def __init__(self):
        self.animal_dao = AnimalDAO()









