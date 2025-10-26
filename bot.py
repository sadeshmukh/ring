import os
import yaml
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

import dotenv
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN) 

handler = SocketModeHandler(app, SLACK_APP_TOKEN)

def check_channel(slug, cid):
    """Checks whether link exists in channel description"""
    next_link = f"{os.getenv('BASE_URL')}/next/{slug}"
    prev_link = f"{os.getenv('BASE_URL')}/prev/{slug}"
    try:
        response = client.conversations_info(channel=cid)
        channel_data = response.get("channel", {})
        purpose = channel_data.get("purpose", {})
        description = purpose.get("value", "") if purpose else ""
        return next_link in description and prev_link in description
    except Exception as e:
        logging.error(f"Error checking channel {cid}: {e}")
        return False

@app.command("ring-validate")
def ring_validate(ack, body):
    """Checks if the current channel is recognized in the ring and has both ring links in its description."""
    ack()
    user_id = body["user_id"]
    channel_id = body["channel_id"]

    with open("channels.yml", "r") as file:
        channels_data = yaml.safe_load(file).get("channels", [])
    
    channels_map = {channel["channel_id"]: channel for channel in channels_data}

    if channel_id not in channels_map:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="This channel is not part of the ring."
        )
        return

    slug = channels_map[channel_id]["slug"]
    if check_channel(slug, channel_id):
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="All good!"
        )
    else:
        next_link = f"{os.getenv('BASE_URL')}/next/{slug}"
        prev_link = f"{os.getenv('BASE_URL')}/prev/{slug}"
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=f"One or both ring links are missing in the channel description: {next_link}, {prev_link}"
        )

def start_slack_bot():
    logging.info("Starting Slack bot...")
    handler.start()

if __name__ == "__main__":
    start_slack_bot()