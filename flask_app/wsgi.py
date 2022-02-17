from flask_app_batch import app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk import capture_message

import logging.config
import logging
from os import path, environ

SENTRY_DSN = environ.get('SENTRY_DSN', "https://f165e333e7de4173a6781281ce74f807@o611000.ingest.sentry.io/6215417")

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100% of transactions
    traces_sample_rate=1.0,
)
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.INFO,  # Send Info as events
)


if __name__ == '__main__':
    capture_message("Starting the flask app")

    # app.run(debug=environ.get('DEBUG',False),
    #             port=int(environ.get('PORT',5000)),
    #             host=environ.get('HOST','0.0.0.0')
    #     )
    app.run(debug=False)
