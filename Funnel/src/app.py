from flask import Flask, jsonify
from dbconn import DbConnection
from funnel import ZNOFunnel
from loguru import logger
import os


app = Flask(__name__)


@app.route("/execute", methods=["POST"])
def execute_funnel():
    try:
        DbConnection.initialize(host=os.environ["POSTGRES_HOST"],
                                port=int(os.environ["POSTGRES_PORT"]),
                                dbname=os.environ["POSTGRES_DB"],
                                user=os.environ["POSTGRES_USER"],
                                password=os.environ["POSTGRES_PASSWORD"],
                                dberror_sleep_time=int(os.environ["APP_DBERR_SLEEP"]))

        zno_funnel = ZNOFunnel(DbConnection.get_instance(),
                               os.environ["APP_INPUT_DIR"],
                               int(os.environ["APP_TX_SIZE"]))

        zno_funnel.execute()

        DbConnection.get_instance().close_connection()

        return jsonify({
            "message": "Executed funnel successfully"
        }), 201
    except Exception as e:
        logger.error(f"Exception while executing funnel: {e}")
        return jsonify({
            "message": f"Exception while executing funnel: {e}"
        }), 500


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
