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

import gc_homeland_v11
from gc_homeland_v11 import read_preprocessing, ocr_json_phase

# from flask import Blueprint, render_template


UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])


ocr_page = Blueprint('ocr_json', __name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_for_pdf_json(filename_for_pdf):
    get_pre_img = read_preprocessing(filename_for_pdf)
    get_OCR_json = ocr_json_phase(get_pre_img)

    # dict_sampe = {
    #   "file_output": filename_for_pdf,
    # }
  
    return get_OCR_json

@ocr_page.route('/ocr_index/', methods=['GET'])
def ocr_index():
    # return "This is PDF to JSON page using OCR"
    return render_template('doc_json.html')

@ocr_page.route('/api/filepdf', methods=['POST'])
def upload_file():
      print("proses sedang di upload")
      # check if the post request has the file part
      try:
        print(request.files)
        print("request satu lancar")
      except Exception as e:
        print(e)

      # return "Gagal"
      
      if 'pdf_ocr' not in request.files:
          # flash('No file part')
          return "request 2 No file part"
          # print("sampai if 1 aman")
      file = request.files['pdf_ocr']

      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          return "Filename salah" 
          # print('sampai sini aman')
          # print("sampai if 2 aman")
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
        #   file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          file_path = os.path.join(UPLOAD_FOLDER, filename)
          file.save(file_path)

          res_ocr = []
        
          do_ocr_json = ocr_for_pdf_json(file_path)
          # do_ocr_tuple = ocr_for_pdf_tuple(file_path)

          print("Request ke 3 aman")
          
          respon_json = str(do_ocr_json)
          res_json = Response(respon_json, mimetype='application/json')
          res_json.headers["Content-Disposition"] = "attachment;filename=ocr_json.json"

          # res_ocr.append(res_json)

          print("request ocr json aman ")

          # respon = str(do_ocr_tuple)
          # res = Response(respon, mimetype='application/json')
          # res.headers["Content-Disposition"] = "attachment;filename=ocr_tuple.json"

          # print("request ocr tuple aman ")

          return res_json

      return "Request ocr lancar"

