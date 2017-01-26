from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
import urllib2, urllib
import urllib
import json
import html2text
import requests
import sys
import os
import zipfile
from io import open
SD_CARD_PATH=u"/run/media/konrad/GoPro"
print u"GoPro Firmware Downloader"
print u"Choose your camera: "
raw_json=urllib2.urlopen(u"https://firmware-api.gopro.com/v2/firmware/catalog").read()
json_data=json.loads(raw_json)
for cam in json_data[u'cameras']:
	target_cam = cam[u'model_string']
	target_cam_name = cam[u'name']
	print target_cam + u" - " + target_cam_name
camera_choice=raw_input(u"Camera: ")
for cam in json_data[u'cameras']:
	if cam[u'model_string'] == camera_choice:
		fw_version=cam[u'version']
		fw_releasedate=cam[u'release_date']
		fw_release_notes=cam[u'release_html']
		fw_dl_url=cam[u'url']
		fw_filename=cam[u'model_string'] + u"_" + fw_version + u"_" + fw_releasedate + u".zip"
		print u"FW Version: " + fw_version + u" FW Release Date: " + fw_releasedate
		print html2text.html2text(fw_release_notes)
		choice_dl=raw_input(u"Do you want to download the firmware to the current working directory? [Y/N]: ")
		if choice_dl.upper() == u"Y":
			print u"Downloading..."
			with open(fw_filename, u"wb") as f:
					print u"Downloading %s" % fw_filename
					response = requests.get(fw_dl_url, stream=True)
					total_length = response.headers.get(u'content-length')

					if total_length is None: # no content length header
						f.write(response.content)
					else:
						dl = 0
						total_length = int(total_length)
						for data in response.iter_content(chunk_size=4096):
						    dl += len(data)
						    f.write(data)
						    done = int(50 * dl / total_length)
						    sys.stdout.write(u"\r[%s%s]" % (u'=' * done, u' ' * (50-done)) )    
						    sys.stdout.flush()
			print u"\nFirmware downloaded!"
			if os.path.isdir(SD_CARD_PATH):
				print u"Unzipping..."
				fh = open(fw_filename, u'rb')
				z = zipfile.ZipFile(fh)
				for name in z.namelist():
					outpath = unicode(SD_CARD_PATH + u"/UPDATE/")
					z.extract(name, outpath)
				fh.close()
				print u"Firmware extracted to SD card!"
				print u"Now eject the SD card and insert it into your camera"
				print u"then turn your camera on and wait for it to update"
			else:
				print u"SD card not recognized, insert your SD card or change the SD_CARD_PATH value"
				print u"Now create a folder called UPDATE inside the camera's SD Card"
				print u"and extract the zip file in the UPDATE folder"
				print u"then insert the SD card back into the camera and turn it on"
