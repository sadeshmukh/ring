import os
import yaml
import logging
import argparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
import threading

from bot import start_slack_bot, check_channel

logging.basicConfig(level=logging.INFO)

with open("channels.yml", "r") as file:
    channels_data = yaml.safe_load(file).get("channels", [])
    
channels_map = {channel["channel_id"]: channel for channel in channels_data}
channel_ids = sorted(channels_map.keys())

import subprocess
commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")

app = FastAPI(title="Ring")

@app.get("/")
async def root():
    return {"message": "the all new Slack Ring"}

@app.get("/next/{slug}")
async def next_ring(slug: str):
    if not any(channels_map[i]["slug"] == slug for i in channel_ids):
        raise HTTPException(status_code=404, detail="Channel slug not found")
    id = [i for i in channel_ids if channels_map[i]["slug"] == slug][0]
    i = channel_ids.index(id) + 1
    next_channel = channel_ids[i % len(channel_ids)]
    slack_url = f"https://hackclub.slack.com/archives/{next_channel}"

    return RedirectResponse(url=slack_url, status_code=302)

@app.get("/prev/{slug}")
async def prev_ring(slug: str):

    if not any(channels_map[i]["slug"] == slug for i in channel_ids):
        raise HTTPException(status_code=404, detail="Channel slug not found")
    id = [i for i in channel_ids if channels_map[i]["slug"] == slug][0]
    i = channel_ids.index(id) - 1
    prev_channel = channel_ids[i % len(channel_ids)] # works, because negative indices
    slack_url = f"https://hackclub.slack.com/archives/{prev_channel}"
    return RedirectResponse(url=slack_url, status_code=302)

@app.get("/version")
async def version():
    # the repo hash is good enough
    return {"commit_hash": commit_hash}

def run_web_server(socket_path=None, host="0.0.0.0", port=None):
    if socket_path:
        if os.path.exists(socket_path):
            os.unlink(socket_path)
        uvicorn.run(app, uds=socket_path)
    else:
        port = port or int(os.getenv("PORT", 8000))
        uvicorn.run(app, host=host, port=port)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", type=str, help="Unix socket path to bind to (e.g., /tmp/ring.sock)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, help="Port to bind to (default: from PORT env var or 8000)")
    
    args = parser.parse_args()
    
    logging.info("Starting Ring...")
    
    slack_thread = threading.Thread(target=start_slack_bot, daemon=True)
    slack_thread.start()
    
    run_web_server(socket_path=args.socket, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
