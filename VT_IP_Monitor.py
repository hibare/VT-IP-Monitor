import requests
import json
from decouple import config
import sys


def VT_IP_Monitor():
	try:	
		message_body = None
		API_KEY = config('VT_API_KEY')
		IP_TO_Monitor = config('IP_TO_MONITOR')
		VT_endpoint = config('VT_ENDPOINT')
		VT_LOCAL_SETTINGS_FILE = config('VT_LOCAL_SETTINGS_FILE')

		# Load local settings file
		with open(VT_LOCAL_SETTINGS_FILE, 'r') as file_handler:
			settings_data = json.loads(file_handler.read())
		
		params = {'apikey':API_KEY, 'ip':IP_TO_Monitor}

		response = requests.get(VT_endpoint, params=params)
		if response.status_code == 200:
			result = json.loads(response.text)

			# Check for URL detection by VT
			if len(result.get('detected_urls')) > 0:
				message_body = "VT URLs detections:\n\n"
				detected_urls = result.get('detected_urls')
				for url in detected_urls:
					message_body += "{}\n".format(url)

			# Check for new domain resolutions
			if len(result.get('resolutions')) > settings_data.get('CURRENT_RESOLUTIONS'):
				resolutions = result.get('resolutions')
				message_body += "\n\nResolutions:\n"
				for resolution in resolutions:
					message_body +="{} - {}".format(resolution.get('hostname'), resolution.get('last_resolved'))
		else:
			message_body = "Request code not 200"
	except Exception as e:
		message_body = "Exception - {}".format(e)

	if message_body is not None:
		print(message_body)

if __name__ == '__main__':
	VT_IP_Monitor()

