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

import ocr_image_process_model
from ocr_image_process_model import read_preprocessing, ocr_json_after_image_process
# from pdf_to_ocr_json.ocr_image_processing_json import ocr_image_process_model
# from ocr_image_process_model import read_preprocessing, ocr_json_phase

# from flask import Blueprint, render_template


UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])


ocr_imageprocess_json_service = Blueprint('ocr_image_json_service', __name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_for_img_pdf_json(filename_for_pdf):
    get_pre_img = read_preprocessing(filename_for_pdf)
    get_OCR_json = ocr_json_after_image_process(get_pre_img)

    # dict_sampe = {
    #   "file_output": filename_for_pdf,
    # }
  
    return get_OCR_json

@ocr_imageprocess_json_service.route('/ocr_img_index/', methods=['GET'])
def ocr_img_index():
    # return "This is PDF to JSON page using OCR"
    return render_template('ocr_img_process_json.html')

@ocr_imageprocess_json_service.route('/api/ocr_image_json', methods=['POST'])
def upload_file():
      print("proses sedang di upload")
      # check if the post request has the file part
      try:
        print(request.files)
        print("request satu lancar")
      except Exception as e:
        print(e)
      
      if 'ocr_file_image_process' not in request.files:
          # flash('No file part')
          return "request 2 No file part"
          
      file = request.files['ocr_file_image_process']

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
        
          do_ocr_json = ocr_for_img_pdf_json(file_path)
          
          respon_json = str(do_ocr_json)
          res_json = Response(respon_json, mimetype='application/json')
          res_json.headers["Content-Disposition"] = "attachment;filename=result_ocr_pdf2img.json"

          print("request ocr json aman ")

          return res_json

      return "Request ocr lancar"

