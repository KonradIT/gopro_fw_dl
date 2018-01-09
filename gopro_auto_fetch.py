## GoPro Firmware Backup Utility ##

import urllib.request
import urllib
import json
import html2text
import requests
import sys
import os
import zipfile

raw_json=urllib.request.urlopen("https://firmware-api.gopro.com/v2/firmware/catalog").read()
json_data=json.loads(raw_json)
for cam in json_data['cameras']:
	logfile = open(cam['model_string'] + '.txt', 'a')
	fw_version=cam['version']
	logfile.write(fw_version)
	fw_releasedate=cam['release_date']
	logfile.write(fw_releasedate)
	fw_release_notes=cam['release_html']
	logfile.write(html2text.html2text(fw_release_notes))
	fw_dl_url=cam['url']
	fw_filename=cam['model_string'] + "_" + fw_version + "_" + fw_releasedate + ".zip"
	print("FW Version: " + fw_version + " FW Release Date: " + fw_releasedate)
	print(html2text.html2text(fw_release_notes))
	print("Downloading...")
	with open(fw_filename, "wb") as f:
			print("Downloading %s" % fw_filename)
			response = requests.get(fw_dl_url, stream=True)
			total_length = response.headers.get('content-length')

			if total_length is None: # no content length header
				f.write(response.content)
			else:
				dl = 0
				total_length = int(total_length)
				for data in response.iter_content(chunk_size=4096):
					dl += len(data)
					f.write(data)
					done = int(50 * dl / total_length)
					sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
					sys.stdout.flush()
