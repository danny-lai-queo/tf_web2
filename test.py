import requests
import time

'''
your localhost url. If running on port 5000
'''
url = "http://localhost:5000/process"
# Path to image file
#filess = {"img": open("PATH_TO_INPUT_IMAGE", "rb")}
files = {"fileToUpload": open("img.jpg", "rb")}
starttime = time.time()
results = requests.post(url, files=files)
print("time taken:", time.time() - starttime)
print(results.text)
