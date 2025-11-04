import os
import logging

logging.basicConfig(level=logging.INFO)

path = os.path.join(os.path.dirname(__file__), "stats.log")

def write_to_log(entry: str):
    with open(path, "a") as f:
        f.write(entry + "\n")

def log_slack(slug: str, random: bool = False, destination: str | None = None): # destination is SLUG
    if random and not destination:
        logging.error("Destination must be present for random logs.")
        return
    if random:
        write_to_log(f"SLACK,RANDOM,{destination}")
        return
    write_to_log(f"SLACK,{slug}")

def log_web(url: str, identifier: str, direction: str, destination: str):
    if not destination:
        logging.error("Destination must be present.")
        return
    if direction == "random":
        write_to_log(f"WEB,{url},{destination}")
        return
    write_to_log(f"WEB,{url},{identifier},{direction}")

