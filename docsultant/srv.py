import logging
import logging.config
from threading import get_ident
from pathlib import Path
from flask import Flask, request, render_template, make_response, jsonify
from docsultant.db import db_init, db_session_done
from docsultant.dao import DAO
from docsultant.model import AnimalDTO, AnimalInfoDTO


logger = logging.getLogger(__name__)
logFile = str(Path(__file__).parent.parent) + '/logging.ini'
logging.config.fileConfig(logFile, disable_existing_loggers=False)


logger.debug("name=" + __name__)

flask_app: Flask = None


def response_ok(res, mimetype):
    response = make_response(res, 200)
    response.mimetype = mimetype
    return response


def create_flask_app() -> Flask:
    logger.info("app")
    _dao:DAO = DAO()

    db_init(get_ident)
    app1 = Flask(__name__, template_folder='app/web/templates', static_folder='app/web/static')
    flask_app = app1

    # NOTE: just for quick test purposes w/o transaction manager
    @app1.teardown_appcontext
    def teardown_appcontext(resp_or_exc):
        logger.debug("teardown_appcontext(...)")
        db_session_done()


    @app1.route('/')
    def home():
        logger.debug("home")
        return render_template('home.j2')

    @app1.route('/get_animals', methods=['GET', 'POST'])
    def get_animals():
        logger.debug("get_animals()")
        return response_ok(jsonify([r.to_dict() for r in _dao.animal_dao.get_animals()]),
                           'application/json')

    @app1.route('/get_tom', methods=['GET', 'POST'])
    def get_tom():
        logger.debug("get_tom()")
        return response_ok(jsonify(_dao.animal_dao.get_animal_by_id(1).to_dict()),
                           'application/json')

    @app1.route('/get_animal_infos', methods=['GET', 'POST'])
    def get_animal_infos():
        logger.debug("get_animal_infos()")
        return response_ok(jsonify([r.to_dict() for r in _dao.animal_dao.get_animal_infos()]),
                           'application/json')

    @app1.route('/get_tom_info', methods=['GET', 'POST'])
    def get_tom_info():
        logger.debug("get_tom_info()")
        return response_ok(jsonify(_dao.animal_dao.get_animal_info_by_nickname("Tom")),
                           'application/json')

    return app1


def main():
    app = create_flask_app()
    logger.debug("Running server ...")
    app.run(use_reloader=False, port=9090)


if __name__ == "__main__":
    main()
