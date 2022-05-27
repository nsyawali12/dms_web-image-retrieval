import os
import requests
import json
from re import search
from PyPDF2 import merger
from cv2 import merge
from flask import Flask, request, flash, redirect, url_for, jsonify, render_template, Response, Blueprint
from flask.helpers import make_response
from werkzeug.utils import  secure_filename, send_from_directory
from werkzeug.wrappers import response

import ocr_pdf_model
from ocr_pdf_model import read_PDF_preprocessing, ocr_json_pdf_process
# from pdf_to_ocr_json.ocr_image_processing_json import ocr_image_process_model
# from ocr_image_process_model import read_preprocessing, ocr_json_phase

# from flask import Blueprint, render_template


UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])


ocr_pdf_json_service = Blueprint('ocr_pdf_service', __name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ocr_pdf_json(filename_for_pdf):
    get_pre_pdf = read_PDF_preprocessing(filename_for_pdf)
    get_OCR_json = ocr_json_pdf_process(get_pre_pdf)

    # dict_sampe = {
    #   "file_output": filename_for_pdf,
    # }
  
    return get_OCR_json

@ocr_pdf_json_service.route('/ocr_pdf_index/', methods=['GET'])
def ocr_pdf_index():
    # return "This is PDF to JSON page using OCR"
    return render_template('ocr_pdf_json.html')

@ocr_pdf_json_service.route('/api/ocr_pdf_json', methods=['POST'])
def upload_file():
      print("proses sedang di upload")
      # check if the post request has the file part
      try:
        print(request.files)
        print("request satu lancar")
      except Exception as e:
        print(e)
      
      if 'ocr_file_pdf' not in request.files:
          # flash('No file part')
          return "request 2 No file part"
          
      file = request.files['ocr_file_pdf']

      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          return "Filename salah" 
          
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
        #   file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          file_path = os.path.join(UPLOAD_FOLDER, filename)
          file.save(file_path)

          res_ocr = []
        
          do_ocr_json = get_ocr_pdf_json(file_path)
          
          respon_json = str(do_ocr_json)
          res_json = Response(respon_json, mimetype='application/json')
          res_json.headers["Content-Disposition"] = "attachment;filename=result_ocr_pdf.json"

          print("request ocr json aman ")

          return res_json

      return "Request ocr done"

