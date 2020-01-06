# IP Monitor

A Python 3 script to monitor your IP for malicious domains/URL.

Script uses VT API to do the IP lookups and PDNS

## Dependencies

Scripts require following modules to function.

1. requests
2. python-decouple

## Execution

There are three ways to run this script.

1. Run directly on host
2. Run in a docker container
3. Run using tasker

### Run directly on host

Install all dependencies using following command.

```python
python3 pip install -r requirements.txt
```

Rename file `.env.example` to `.env` (under `src`).

Populate enviroment variables memntioned in `.env`

Navigate to `src` and execute the script as follow.

```python
python3 VT_IP_Monitor.py
```

#### OR

Schedule the script execution using cron. Edit crontab file using command `crontab -e` and add following line at the end of the file.

```
0 */12 * * * python3 <path_to_src>/src/VT_IP_Monitor.py
```

This runs the script every 1 hour.

To periodically check for popular downloads, schedule the script using cron.

### Run in docker container

Pull the latest docker image from Docker Hub using following command.

```shell
docker pull hibare/vt_ip_monitor
```

Alternatively, you can build the docker image using following command.

```shell
docker build --rm -t vt_ip_monitor . --no-cache
```

Create following file.

1. env

Populate the first file (`env`) with following values.

```
VT_API_KEY=<YOUR_VALUE>
IP_TO_MONITOR=<YOUR_VALUE>
VT_ENDPOINT=<YOUR_VALUE>
VT_LOCAL_SETTINGS_FILE=<YOUR_VALUE>
SLACK_ENDPOINT=<YOUR_VALUE>
PRESENT_RESOLUTIONS=<YOUR_VALUE>
```

Run the container using following command.

```shell
docker run -d -v $PWD/.env:/app/.env hibare/vt_ip_monitor:latest
```

### Run using tasker

tasker is a docker image to schedule the execution of the containers. Its kind of cron for docker container execution.

Rename file `.env.example` to `.env` (under `src`).

Populate enviroment variables memntioned in `.env`

Replace `<absolute path to src>` with absolute path to the `src` directory in file `docker-compose.yml`.

Start stack using following command.

```shell
docker-compose up
```

:exclamation: All cron jobs are scheduled to run every 1 hour.
