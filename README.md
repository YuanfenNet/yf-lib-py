# Yuanfen Python Library

## build && upload

```bash
$ hatch build
$ python3 -m twine upload dist/*
```

## Config

Support .json, .yaml, .ini files.
Support auto reloading while config file changes.

```python
config_json = Config(os.path.abspath("config.json"))
config_yaml = Config(os.path.abspath("config.yaml"))
config_ini = Config(os.path.abspath("config.ini"))

print(config_ini["app"]["config_a"])
print(config_yaml["movie"]["name"])
```

## Logger

Stream and TimedRotatingFile handlers for logging.

```python
logger = Logger(name="my-logger", level=logging.INFO)

logger.debug("debug log")
logger.info("info log")
logger.warn("warn log")
logger.error("error log")
```

## BaseResponse, SuccessResponse, ErrorResponse

Response models for fastapi.

```python
import uvicorn
from fastapi import FastAPI
from yuanfen import SuccessResponse

app = FastAPI()


@app.get("/health-check")
def health_check():
    return SuccessResponse(data="OK")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

## time

```python
from yuanfen import time

time.format(dt=datetime.now(), format="%Y-%m-%dT%H:%M:%S")
time.parse(dt_string="2023-11-25T10:51:19", format="%Y-%m-%dT%H:%M:%S")
time.format_duration(90)
```

## GroupRobot

Webhook group robot

```python
robot = GroupRobot(webhook="your robot's webhook path")
robot.send(data)
```
