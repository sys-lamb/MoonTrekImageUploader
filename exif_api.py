#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS
import requests
from io import BytesIO
import pandas as pd
import json

from flask import Flask, request, jsonify, abort

app = Flask(__name__)
app.config["DEBUG"] = True

def extract_exif(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # extract EXIF data
    exifdata = img.getexif()
    
    exif_data = dict()
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        exif_data[str(tag)] = str(data)
    return exif_data   
    
def save_to_file(exif_dict):   
    json = json.dumps(exif_dict)
    f = open("dict.json","w")
    f.write(json)
    f.close()    
    return

@app.route('/', methods=['GET', 'POST'])
def process_file():
    req_param = request.json
    url = req_param['image_url']
    exif_data = extract_exif(url)
    return jsonify(exif_data)

print('api ready')
if __name__ == '__main__':

    app.run(debug=False, host='127.0.0.1', port = 8055)










