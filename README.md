# Yuanfen Python Library

## Installation

```bash
pip install yuanfen
```

## Config

Supports `.json`, `.yaml` / `.yml`, and `.ini` files. Instances are singletons per file path. Auto-reloads when the config file changes (uses polling by default).

```python
from yuanfen import Config

config = Config("configs/config.yaml")

# Access via key (raises KeyError if missing)
print(config["app"]["name"])

# Access with default fallback
print(config.get("debug", False))
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | — | Path to the config file |
| `poll` | `bool` | `True` | Use polling observer (more compatible); set `False` for native FS events |
| `logger` | `Logger` | `Logger()` | Logger instance for reload messages |

## Logger

Writes to both stdout and a daily-rotated file at `logs/log` (kept for 365 days).

```python
import logging
from yuanfen import Logger

logger = Logger(name="my-service", level=logging.DEBUG)

logger.debug("debug log")
logger.info("info log")
logger.warning("warning log")
logger.error("error log")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `None` | Prefix added to every log message as `[name]` |
| `level` | `int` | `logging.INFO` | Minimum log level |
| `logger` | `logging.Logger` | root logger | Use a custom logger instance |

## Response

Pydantic response models for FastAPI.

```python
from yuanfen import BaseResponse, SuccessResponse, ErrorResponse

# Default: code=0, message="SUCCESS"
SuccessResponse(data={"id": 1})

# Default: code=1000, message="ERROR"
ErrorResponse(message="Something went wrong")

# Custom
BaseResponse(code=404, message="Not found")
```

```python
import uvicorn
from fastapi import FastAPI
from yuanfen import SuccessResponse, ErrorResponse

app = FastAPI()

@app.get("/health-check")
def health_check():
    return SuccessResponse(data="OK")

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id != 1:
        return ErrorResponse(code=404, message="Item not found")
    return SuccessResponse(data={"id": item_id})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## time

Timezone-aware time utilities (defaults to `Asia/Shanghai`).

```python
from yuanfen import time
from datetime import datetime

# Current time (no tzinfo attached)
dt = time.now()

# Current time with timezone info
dt_tz = time.now(tz="Asia/Shanghai", with_tz=True)

# Strip timezone from a tz-aware datetime
dt_naive = time.remove_tz(dt_tz)

# Format datetime to string
time.format(dt=datetime.now(), format="%Y-%m-%dT%H:%M:%S")

# Parse string to datetime
time.parse(dt_str="2023-11-25T10:51:19", format="%Y-%m-%dT%H:%M:%S")

# Format duration in seconds to HH:MM:SS or MM:SS
time.format_duration(90)   # "01:30"
time.format_duration(3661) # "01:01:01"

# Timestamps (default 16-digit microseconds)
time.current_timestamp()          # current timestamp
time.get_timestamp(dt, length=13) # milliseconds from datetime

# Passthrough to standard library
time.sleep(1.5)
time.time()
```

## GroupRobot

Send messages to a webhook-based group robot (e.g. DingTalk, Feishu).

```python
from yuanfen import GroupRobot

robot = GroupRobot(webhook="https://your-robot-webhook-url")
robot.send({"msgtype": "text", "text": {"content": "Hello!"}})
```

## Email

Send and receive emails via SMTP/IMAP.

```python
from yuanfen import Email

mail = Email(
    address="you@example.com",
    password="your-password",
    smtp_host="smtp.example.com",
    smtp_port=465,
    imap_host="imap.example.com",
    imap_port=993,
    sender_name="My App",  # optional display name
)

# Send a plain-text email
mail.send_text(to="recipient@example.com", subject="Hello", text="World")

# Search latest N email UIDs matching IMAP criteria
ids = mail.search_ids(count=5, "UNSEEN")

# Fetch a single email by UID
msg = mail.fetch(message_id="123", content_type="text/plain")
# msg keys: subject, from, to, date, charset, content

# Search + fetch in one call
messages = mail.search(count=5, content_type="text/plain", "UNSEEN")
```

## Redis

A Redis client wrapper with optional key prefix and a distributed lock helper.

```python
from yuanfen import Redis, RedisLock

redis = Redis({
    "host": "localhost",
    "port": 6379,
    "password": "secret",
    "db": 0,
    "prefix": "myapp",       # optional; keys are stored as "myapp:<key>"
    "decode_responses": True, # optional, default True
})

redis.set("foo", "bar", ex=60)  # set with 60s expiry
redis.get("foo")                 # "bar"
redis.setex("foo", 60, "bar")
redis.setnx("counter", "0")
redis.incr("counter")
redis.delete("foo")
redis.exists("foo")
redis.expire("foo", 120)
redis.ttl("foo")
redis.getset("foo", "new")
```

### RedisLock

```python
lock = RedisLock(
    redis_client=redis.redis_client,
    lock_key="my-job",
    timeout=10,          # lock expiry in seconds
    retry_interval=0.5,  # seconds between retries; None = no retry
)

if lock.acquire():
    try:
        # critical section
        pass
    finally:
        lock.release()
```

## SMS

SMS verification code service built on Alibaba Cloud SMS (async).

```python
from yuanfen import Config, Logger, SmsService, SmsSendCodeRequest, SmsVerifyCodeRequest

config = Config("config.yaml")
logger = Logger()
sms = SmsService(config=config, logger=logger)

# config.yaml must contain:
# redis: { host, port, password, db, prefix }
# aliyun: { access_key_id, access_key_secret, sms_sign_name, sms_template_code }

# Send a 6-digit code (raises on cooldown or send failure)
await sms.send_code(SmsSendCodeRequest(system="myapp", phone="13800138000", length=6))

# Verify the code (raises on wrong code / expiry / too many attempts)
await sms.verify_code(SmsVerifyCodeRequest(system="myapp", phone="13800138000", code="123456"))
```

Behavior:
- Code TTL: **300 seconds** (5 minutes)
- Resend cooldown: **60 seconds**
- Max verify attempts: **5** (code is deleted on exceeded)

## hash

```python
from yuanfen import hash

# SHA-256 (default)
digest = hash.get_file_hash("path/to/file")

# Other algorithm, truncated to 8 chars
digest = hash.get_file_hash("path/to/file", algorithm="md5", length=8)
```

## ip

```python
from yuanfen import ip

# Get public IP (tries ipify then ipip.net)
public_ip = ip.get_public_ip()

# Get IP location (sources: "baidu" or "ip-api")
location = ip.get_ip_location("8.8.8.8", source="baidu")
location = ip.get_ip_location("8.8.8.8", source="ip-api")
```

## Version

Semantic version parsing and comparison.

```python
from yuanfen import Version

v = Version(1, 2, 3)
v = Version.parse("1.2.3")

str(v)          # "1.2.3"
v.to_tuple()    # (1, 2, 3)
v.to_dict()     # {"major": 1, "minor": 2, "patch": 3}

# compare() returns -1, 0, or 1
v.compare("1.2.4")           # -1
v.compare(Version(1, 2, 3))  # 0
v.compare({"major": 1, "minor": 2, "patch": 0})  # 1
```

## APP_ENV

Reads the `APP_ENV` environment variable (defaults to `"dev"`).

```python
from yuanfen import APP_ENV

if APP_ENV == "prod":
    ...
```
