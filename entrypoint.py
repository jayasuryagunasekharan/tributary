# import dependencies
import json
import redis as redis
from flask import Flask, request, jsonify
from loguru import logger

# define constants
HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

# create a Flask server, and allow us to interact with it using the app variable
app = Flask(__name__)


# define an endpoint which accepts POST requests, and is reachable from the /record endpoint
@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    if engine_temperature_values:
        current_engine_temperature = float(engine_temperature_values[0])
        average_engine_temperature = sum(map(float, engine_temperature_values)) / len(engine_temperature_values)
    else:
        current_engine_temperature = None
        average_engine_temperature = None

    logger.info(f"record request successful")
    return jsonify({
        "current_engine_temperature": current_engine_temperature,
        "average_engine_temperature": average_engine_temperature
    })


# define an endpoint which accepts POST requests, and is reachable from the /collect endpoint
@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)

    if engine_temperature_values:
        current_engine_temperature = float(engine_temperature_values[0])
        average_engine_temperature = sum(map(float, engine_temperature_values)) / len(engine_temperature_values)
    else:
        current_engine_temperature = None
        average_engine_temperature = None

    return jsonify({
        "current_engine_temperature": current_engine_temperature,
        "average_engine_temperature": average_engine_temperature
    })


# start the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
