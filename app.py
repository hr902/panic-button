import logging
import os

from dotenv import load_dotenv
from flask import Flask, Response, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk.errors import SlackApiError

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise RuntimeError(f"Missing required environment variable: {name}")


SLACK_BOT_TOKEN = require_env("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = require_env("SLACK_SIGNING_SECRET")
ALERT_CHANNEL = require_env("ALERT_CHANNEL")
PORT = int(os.getenv("PORT", "3000"))

slack_app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)
handler = SlackRequestHandler(slack_app)
web_app = Flask(__name__)


@slack_app.command("/panic")
def panic_command(ack, body, client, logger):
    user_id = body.get("user_id", "unknown-user")
    channel_id = body.get("channel_id", "unknown-channel")
    user_name = body.get("user_name", "unknown-user")
    command_text = (body.get("text") or "").strip()

    logger.info(
        "Received /panic from user=%s name=%s source_channel=%s text=%s",
        user_id,
        user_name,
        channel_id,
        command_text or "<empty>",
    )
    try:
        ack(
            response_type="ephemeral",
            text="Alerta recibida. Estamos contigo.",
        )

        alert_text = f":rotating_light: ALERTA: <@{user_id}> activo el boton de panico."
        if command_text:
            alert_text += f" Detalle: {command_text}"

        response = client.chat_postMessage(
            channel=ALERT_CHANNEL,
            text=alert_text,
        )
        logger.info(
            "Alert message sent successfully. ts=%s destination=%s",
            response.get("ts"),
            ALERT_CHANNEL,
        )
    except SlackApiError as exc:
        error_code = exc.response.get("error", "unknown_error")
        logger.exception("Slack rejected chat_postMessage with error=%s", error_code)
    except Exception:
        logger.exception("Unexpected error while processing /panic")


@slack_app.error
def handle_slack_error(error, body, logger):
    logger.exception("Unhandled Slack Bolt error. body=%s error=%s", body, error)


@web_app.get("/")
def healthcheck():
    return {"ok": True, "service": "panic-button"}, 200


@web_app.post("/slack/events")
def slack_events():
    try:
        return handler.handle(request)
    except Exception:
        logger.exception("HTTP error while handling Slack request")
        return Response("Internal error", status=500)


@web_app.get("/slack/events")
def slack_events_get():
    return Response("Slack endpoint is ready.", status=200)


if __name__ == "__main__":
    logger.info("Starting Slack app in HTTP mode on port %s", PORT)
    web_app.run(host="0.0.0.0", port=PORT)
