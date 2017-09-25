import os
from flask import Flask, render_template, request
from PIL import Image
import sys
import pyocr
import pyocr.builders
import re
import json
import base64


__author__ = 'K_K_N'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def ocr(image_data):
    #imgdata = base64.b64decode(image_data)
    #img_result = open('temp.jpg','w+')
    #img_result.write(imgdata)
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[1]
    print("Will use lang '%s'" % (lang))
    txt = tool.image_to_string(
        Image.open(image_data),
        lang='OCR',
        builder=pyocr.builders.TextBuilder()
    )

    #img_result.close()
    ektp_no = re.search( r'[?:nik\s*:\s*](\d{8,20})\s*', txt, re.I)
    #print ektp_no
    if ektp_no:
        print "ektp_no.group() : ", ektp_no.group()
    data = {}
    data['ektp'] = ektp_no.group().strip()
    return json.dumps(data)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        return ocr(file)
    else: 
        data = {}
        data['error'] = 'File not found.'
        return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=True)
