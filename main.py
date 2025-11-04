import os
import yaml
import logging
import argparse
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import uvicorn
import threading
import random

from bot import start_slack_bot, check_channel
from statslog import log_web

logging.basicConfig(level=logging.INFO)

from channels import CHANNELS_MAP, CHANNEL_IDS

# with open("channels.yml", "r") as file:
#     channels_data = yaml.safe_load(file).get("channels", [])
    
# CHANNELS_MAP = {channel["channel_id"]: channel for channel in channels_data}
# CHANNEL_IDS = sorted(CHANNELS_MAP.keys())

import subprocess
commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
last_commit_date = subprocess.check_output(["git", "log", "-1", "--format=%cd"]).strip().decode("utf-8")

logging.info(f"Loaded {len(CHANNEL_IDS)} channels into the ring.")
logging.info(f"Running on commit {commit_hash} updated at {last_commit_date}")

app = FastAPI(title="Ring")

@app.get("/")
def root():
    return {"message": "website coming soon! in the meantime, check /random to get started."}

def get_channel_by_identifier(identifier: str):
    try:  # use as int, otherwise treat as slug
        idx = int(identifier)
        if not any(CHANNELS_MAP[i]["idx"] == idx for i in CHANNEL_IDS):
            raise HTTPException(status_code=404, detail="Channel index not found")
        return [i for i in CHANNEL_IDS if CHANNELS_MAP[i]["idx"] == idx][0]
    except ValueError:
        if not any(CHANNELS_MAP[i]["slug"] == identifier for i in CHANNEL_IDS):
            raise HTTPException(status_code=404, detail="Channel slug not found")
        return [i for i in CHANNEL_IDS if CHANNELS_MAP[i]["slug"] == identifier][0]

@app.get("/next/{identifier}")
@app.get("/n/{identifier}")
def next_ring(identifier: str, request: Request):
    cid = get_channel_by_identifier(identifier)
    current_slug = CHANNELS_MAP[cid]["slug"]
    i = CHANNEL_IDS.index(cid) + 1
    next_channel = CHANNEL_IDS[i % len(CHANNEL_IDS)]
    slack_url = f"https://hackclub.slack.com/archives/{next_channel}"
    
    log_web(str(request.url), current_slug, "next", destination=CHANNELS_MAP[next_channel]["slug"])
    return RedirectResponse(url=slack_url, status_code=302)

@app.get("/prev/{identifier}")
@app.get("/p/{identifier}")
def prev_ring(identifier: str, request: Request):
    cid = get_channel_by_identifier(identifier)
    current_slug = CHANNELS_MAP[cid]["slug"]
    i = CHANNEL_IDS.index(cid) - 1
    prev_channel = CHANNEL_IDS[i % len(CHANNEL_IDS)]  # works because negative indices
    slack_url = f"https://hackclub.slack.com/archives/{prev_channel}"
    log_web(str(request.url), current_slug, "prev", destination=CHANNELS_MAP[prev_channel]["slug"])
    return RedirectResponse(url=slack_url, status_code=302)

@app.get("/random")
def random_ring(request: Request):
    random_channel = random.choice(CHANNEL_IDS)
    slack_url = f"https://hackclub.slack.com/archives/{random_channel}"
    log_web(str(request.url), "random", "random", destination=CHANNELS_MAP[random_channel]["slug"])
    return RedirectResponse(url=slack_url, status_code=302)

@app.get("/version")
def version():
    # the repo hash is good enough
    return {"commit_hash": commit_hash, "updated_at": last_commit_date}

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
