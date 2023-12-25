from flask import Flask, jsonify
from loguru import logger
from serviceworker import ServiceWorker
import os


app = Flask(__name__)


@app.route('/execute', methods=['POST'])
def execute_service_worker():
    try:
        logger.info("Executing service worker")
        service_worker = ServiceWorker(int(os.environ["APP_TX_SIZE"]),
                                       "postgresql+psycopg2",
                                       os.environ["POSTGRES_USER"],
                                       os.environ["POSTGRES_PASSWORD"],
                                       os.environ["POSTGRES_HOST"],
                                       int(os.environ["POSTGRES_PORT"]),
                                       os.environ["POSTGRES_DB"])

        service_worker.execute()

        return jsonify({
            "message": "Executed service worker successfully"
        }), 201
    except Exception as e:
        logger.error(f"Exception while executing service worker: {e}")
        return jsonify({
            "message": f"Exception while executing service worker: {e}"
        }), 500


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
