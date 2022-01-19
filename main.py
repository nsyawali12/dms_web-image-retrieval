import os
import requests
import json
from re import search
from PyPDF2 import merger
from cv2 import merge
from flask import Flask, request, flash, redirect, url_for, jsonify, render_template, Response
from flask.helpers import make_response
from werkzeug.utils import  secure_filename, send_from_directory
from werkzeug.wrappers import response
# import searchable
# from searchable import searchable_preprocess, result_search
import PyPDF2
from PyPDF2 import PdfFileMerger


### importing another page python
from ocr_json import ocr_page
from search_merger import searchable_pdf_merge

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app = Flask(__name__)

# add pages here
@app.route('/')
def homepage():
    return render_template('index.html')
    
# @app.route('/doc_json')
# def doc_json():
#     return render_template('doc_json.html')

app.register_blueprint(ocr_page, url_prefix='/ocr_json')
app.register_blueprint(searchable_pdf_merge, url_prefix='/search_merger')

@app.route('/ocr_json/ocr_index/')
def nav_ocr():
    return render_template('doc_json.html')

@app.route('/search_merger/search_index/')
def nav_searchable():
    return render_template('doc_json.html')


# @app.route('/search_merge')
# def searchable_merge():
#     return render_template('search_merge.html')

if __name__== '__main__':
    app.run(port=8000, debug=True)