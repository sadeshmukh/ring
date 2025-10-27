import os
import yaml
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

import dotenv
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)

from channels import CHANNELS_MAP, CHANNEL_IDS, CHANNELS_DATA

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

@app.command("/ring-validate")
def ring_validate(ack, body):
    """Checks if the current channel is recognized in the ring and has both ring links in its description."""
    ack()
    user_id = body["user_id"]
    channel_id = body["channel_id"]

    if channel_id not in CHANNELS_MAP:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="This channel is not part of the ring, but it could be! Join <#C09NLGSU5U3> and take a look at <https://hackclub.slack.com/docs/T0266FRGM/F09NCDL31AT|this canvas> to get your channel added."
        )
        return

    slug = CHANNELS_MAP[channel_id]["slug"]
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

@app.command("/ring-validate-all")
def ring_validate_all(ack, body):
    """Checks which channels aren't recognized in the ring or aren't currently valid."""
    ack()
    user_id = body["user_id"]
    invalid_channels = [] # list: <#channel_id> managed by <@user_id>

    
    for channel in CHANNELS_DATA:
        slug = channel["slug"]
        cid = channel["channel_id"]
        if not check_channel(slug, cid):
            invalid_channels.append(f"<#{cid}> managed by <@{channel['user_id']}>")

    if not invalid_channels:
        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=user_id,
            text="All channels are properly configured!"
        )
    else:
        invalid_list = "\n".join(invalid_channels)
        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=user_id,
            text=f"The following channels are missing ring links in their descriptions:\n{invalid_list}"
        )

@app.command("/ring-links")
def ring_links(ack, body):
    """Provides the next and previous channel links in the ring."""
    ack()
    user_id = body["user_id"]
    channel_id = body["channel_id"]

    if channel_id not in CHANNELS_MAP:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="This channel is not part of the ring, but it could be! Join <#C09NLGSU5U3> and take a look at <https://hackclub.slack.com/docs/T0266FRGM/F09NCDL31AT|this canvas> to get your channel added."
        )
        return

    slug = CHANNELS_MAP[channel_id]["slug"]
    id = [i for i in CHANNEL_IDS if CHANNELS_MAP[i]["slug"] == slug][0]
    i = CHANNEL_IDS.index(id)
    next_channel = CHANNEL_IDS[(i + 1) % len(CHANNEL_IDS)]
    next_slack_url = f"<#{next_channel}>"
    prev_channel = CHANNEL_IDS[(i - 1) % len(CHANNEL_IDS)]
    prev_slack_url = f"<#{prev_channel}>"

    client.chat_postEphemeral(
        channel=channel_id,
        user=user_id,
        text=f"{prev_slack_url} <|> {next_slack_url}"
    )

def start_slack_bot():
    logging.info("Starting Slack bot...")
    handler.start()

if __name__ == "__main__":
    start_slack_bot()