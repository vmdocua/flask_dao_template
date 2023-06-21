import logging
import logging.config
from pathlib import Path
from flask import Flask, request, render_template, make_response, jsonify


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

    app1 = Flask(__name__, template_folder='app/web/templates', static_folder='app/web/static')
    flask_app = app1


    @app1.route('/')
    def home():
        logger.debug("home")
        return render_template('home.j2')

    return app1


def main():
    app = create_flask_app()
    logger.debug("Running server ...")
    app.run(use_reloader=False, port=9090)


if __name__ == "__main__":
    main()
