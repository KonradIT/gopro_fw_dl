import urllib.request
import urllib
import json
import html2text
import requests
import sys
import os
import zipfile
SD_CARD_PATH="/run/media/konrad/GoPro"
print("GoPro Firmware Downloader")
print("Choose your camera: ")
raw_json=urllib.request.urlopen("https://firmware-api.gopro.com/v2/firmware/catalog").read()
json_data=json.loads(raw_json)
for cam in json_data['cameras']:
	target_cam = cam['model_string']
	target_cam_name = cam['name']
	print(target_cam + " - " + target_cam_name)
camera_choice=input("Camera: ")
for cam in json_data['cameras']:
	if cam['model_string'] == camera_choice:
		fw_version=cam['version']
		fw_releasedate=cam['release_date']
		fw_release_notes=cam['release_html']
		fw_dl_url=cam['url']
		fw_filename=cam['model_string'] + "_" + fw_version + "_" + fw_releasedate + ".zip"
		print("FW Version: " + fw_version + " FW Release Date: " + fw_releasedate)
		print(html2text.html2text(fw_release_notes))
		choice_dl=input("Do you want to download the firmware to the current working directory? [Y/N]: ")
		if choice_dl.upper() == "Y":
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
			print("\nFirmware downloaded!")
			if os.path.isdir(SD_CARD_PATH):
				print("Unzipping...")
				fh = open(fw_filename, 'rb')
				z = zipfile.ZipFile(fh)
				for name in z.namelist():
					outpath = str(SD_CARD_PATH + "/UPDATE/")
					z.extract(name, outpath)
				fh.close()
				print("Firmware extracted to SD card!")
				print("Now eject the SD card and insert it into your camera")
				print("then turn your camera on and wait for it to update")
			else:
				print("SD card not recognized, insert your SD card or change the SD_CARD_PATH value")
				print("Now create a folder called UPDATE inside the camera's SD Card")
				print("and extract the zip file in the UPDATE folder")
				print("then insert the SD card back into the camera and turn it on")
