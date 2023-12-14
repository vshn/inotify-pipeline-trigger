# inotify-pipeline-trigger

A small script that can be run in a sidecar container to trigger a GitLab pipeline when new files appear in a configured location.

It uses the Linux kernel's inotify facilities so it should be really lightweight.


## Installation

If you want to run the script itself directly (not as a container), you'll need to install requirements:

`python -m pip install -r requirements.txt`

Then you can run the script with:

`./trigger-pipeline.py`

Just make sure to set the env vars (see below) before running.


## Usage

Set the following environment variables:

|Env var|Description|Example|
|---|---|---|
|`PIPELINE_URL`|The URL pointing to a project's pipeline to trigger|https://gitlab.example.org/api/v4/projects/102/trigger/pipeline|
|`PIPELINE_TOKEN`|A GitLab pipeline trigger token ("glptt") that allows the pipeline to be triggered|`glptt-42df22923d789fa9f13fb00483d40b4ae0526959`|
|`WATCH_DIR`|The directory to watch|`/tmp/triggerfiles`|

## Caveats and warnings

This is certainly very primitive and non-Pythonic code. There is no input sanitization on things passed via the env vars. The error handling is at its most basic.

