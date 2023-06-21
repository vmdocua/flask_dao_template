import logging
from typing import Optional, Callable, Any
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from docsultant.dao import BaseDAO

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


############################################
# DB engine

def db_init(session_scopefunc: Optional[Callable[[], Any]] = None):
    logger.debug("dao_init()")
    engine = create_engine(f'sqlite:///{str(Path(__file__).parent.parent)}/db/db.sqlite3', echo=True)
    logger.debug("created DB engine=" + str(engine))

    BaseDAO.default_session = scoped_session(sessionmaker(bind=engine), scopefunc=session_scopefunc)
    logger.debug("done")


def db_session_done():
    logger.debug("dao_session_done()")
    BaseDAO.default_session.remove()
