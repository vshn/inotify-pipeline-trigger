#!/usr/bin/env python3
import inotify.adapters
import requests
import os
import datetime


print("Starting up.")

config = {
        "url": os.environ.get("PIPELINE_URL", "http://example.org"),
        "token": os.environ.get("PIPELINE_TOKEN", "glptt-foobar"),
        "directory": os.environ.get("WATCH_DIR", "/sedex-interface/inbox")
        }

def _main():
    validate_config(config)
    i = inotify.adapters.Inotify()
    i.add_watch(config["directory"])
    print(f"Watching directory {config['directory']} and will trigger {config['url']} when new files arrive.")

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        # We want to wait for the file to finish being written before we trigger the pipeline
        if 'IN_CLOSE_WRITE' in type_names:
            trigger_pipeline(filename)

def trigger_pipeline(filename = ''):
    print(f"{datetime.datetime.now()} New file {filename} detected in inbox, triggering pipeline at {config['url']}")
    data = {
            "token": config["token"],
            "ref": "main"
            }
    try:
        response = requests.post(config["url"], data=data)
        print(f"{datetime.datetime.now()} Response code: {response.status_code}")
    except Exception as e:
        print(f"{datetime.datetime.now()} ERROR: Exception while sending POST request to {config['url']}")
        print(f"Exception is: {e}")
        print(f"Response code: {response.status_code}")
        print(f"Response: {response.content.decode()}")

# Only validates the watch dir, but feel free to add more
def validate_config(config):
    directory = config["directory"]
    if not (os.path.exists(directory) and os.path.isdir(directory)):
        exit(f"{directory} does not exist or isn't a directory")

if __name__ == '__main__':
    _main()
