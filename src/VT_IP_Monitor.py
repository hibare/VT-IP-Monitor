import requests
import json
from decouple import config
import sys
import traceback
import logging

# Configure and create a logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def send_notification(text):
    logger.info("Sending slack notification, data=%s", text)
    slack_endpoint = config('SLACK_ENDPOINT')
    headers = {
        'Content-type': 'application/json',
    }
    data = dict(
        text=text,
    )
    data = json.dumps(data)
    response = requests.post(slack_endpoint, headers=headers, data=data)
    return response.status_code


def VT_IP_Monitor():
    try:
        message_body = str()
        API_KEY = config('VT_API_KEY')
        IP_TO_Monitor = config('IP_TO_MONITOR')
        VT_ENDPOINT = config('VT_ENDPOINT')
        logger.info("Initiating check for IP=%s", IP_TO_Monitor)

        params = {'apikey': API_KEY, 'ip': IP_TO_Monitor}

        response = requests.get(VT_ENDPOINT, params=params)
        logger.info("Received response from VT API, status_code=%s, response=%s",
                    response.status_code, response.content)

        if response.status_code == 200:
            result = json.loads(response.text)

            # Check for URL detection by VT
            if len(result.get('detected_urls')) > 0:
                logger.info("Detected malicious URLs, %s",
                            result.get('detected_urls'))

                message_body = "VT URLs detections:\n\n"
                detected_urls = result.get('detected_urls')

                for url in detected_urls:
                    message_body += "%s\n" % (url)

            # Check for new domain resolutions
            if len(result.get('resolutions')) > config('PRESENT_RESOLUTIONS', cast=int):
                logger.info("No. of resolutions is different, %s",
                            result.get('resolutions'))
                resolutions = result.get('resolutions')
                message_body += "\n\nResolutions:\n"

                for resolution in resolutions:
                    message_body += "%s - %s\n" % (resolution.get(
                        'hostname'), resolution.get('last_resolved'))
        else:
            message_body = "Request code not 200"
    except:
        logger.error("Exception: %s", traceback.format_exc())
        message_body = "Exception - %s" % (traceback.format_exc())

    if message_body is not None:
        logger.info("Final message=%s", message_body)
        response_code = send_notification(message_body)
        logger.info("Received notification respose=%s", response_code)

    else:
        logger.info("All clean :)")


if __name__ == '__main__':
    VT_IP_Monitor()
