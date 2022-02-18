import os
import requests
import json
import sys
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


### importing another page python flask services

sys.path.insert(1, './pdf_to_ocr_json/ocr_pdf')
# from pdf_to_ocr_json.ocr_image_processing_json.ocr_image_json_service import ocr_imageprocess_json_service
import ocr_pdf_service
from ocr_pdf_service import ocr_pdf_json_service

sys.path.insert(1, './searchable')
import searchable_service
from searchable_service import searchable_pdf_service
# from searchable.searchable_service import searchable_pdf_service

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

app.register_blueprint(ocr_pdf_json_service, url_prefix='/ocr_pdf_service')
app.register_blueprint(searchable_pdf_service, url_prefix='/searchable_service')

@app.route('/ocr_pdf_service/ocr_pdf_index/')
def nav_ocr():
    return render_template('ocr_img_process_json.html')

@app.route('/searchable_service/searchable_index/')
def nav_searchable():
    return render_template('searchable.html')


# @app.route('/search_merge')
# def searchable_merge():
#     return render_template('search_merge.html')

if __name__== '__main__':
    app.run(port=8000, debug=True)