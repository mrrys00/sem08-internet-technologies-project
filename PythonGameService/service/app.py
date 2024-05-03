from datetime import datetime
from logging import basicConfig, getLogger, INFO
from flask import Flask, request
from os import getenv
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from random import randint
from asyncio import sleep


MIN_SLEEP = 1
MAX_SLEEP = 3
PLAYERS_NUMBER = 5
GET_PATH = f'/positions'
POST_PATH = f'/positions/<player_id>'
END = '\033[0m'
RED = '\033[91m'
GREEN = '\033[32m'
BLUE = '\033[34m'


def print_colored(text, color):
    print(f'{color}{text}{END}')


player_positions = {i: {"x": 0, "y": 0} for i in range(0, PLAYERS_NUMBER)}

app = Flask(__name__)

basicConfig(level=INFO)
logger = getLogger(__name__)

resource = Resource(attributes={
    SERVICE_NAME: 'PythonGameService'
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer('PythonGameService.tracer')

span_processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=getenv('OTEL_EXPORTER_OTLP_ENDPOINT'), insecure=True))
trace.get_tracer_provider().add_span_processor(span_processor)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=getenv('OTEL_EXPORTER_OTLP_ENDPOINT')))

meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)


@app.route(GET_PATH)
async def get_positions():
    print_colored('RECEIVED REQUEST.', GREEN)
    await sleep(randint(MIN_SLEEP, MAX_SLEEP))
    print_colored('SENDING RESPONSE...', GREEN)

    result = {'PLAYERS POSITIONS': player_positions}
    print_colored(result, GREEN)
    log_request(result)

    return result


@app.route(POST_PATH, methods=['POST'])
async def change_position(player_id):
    player = int(player_id)
    body = request.json

    print_colored('ID: ' + player_id + ' OLD POSITION: ' + str(player_positions[player]), BLUE)
    player_positions[player]['x'] += body['x']
    player_positions[player]['y'] += body['y']
    print_colored('ID: ' + player_id + ' NEW POSITION: ' + str(player_positions[player]), BLUE)

    result = {'POSITION': player_positions[player]}
    log_request(result)

    return result


def log_request(result):
    logger.log(msg={
        'time': datetime.now(),
        'result': result
    }, level=INFO)
