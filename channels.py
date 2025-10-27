import yaml

with open("channels.yml", "r") as file:
    channels_data = yaml.safe_load(file).get("channels", [])

CHANNELS_DATA = channels_data
CHANNELS_MAP = {channel["channel_id"]: channel for channel in channels_data}
CHANNEL_IDS = sorted(CHANNELS_MAP.keys())