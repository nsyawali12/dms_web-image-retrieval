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

import ocr_image_model
from ocr_image_model import read_Image_preprocessing, ocr_json_image_process

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])

ocr_img_json_service = Blueprint('ocr_image_service', __name__)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ocr_img_json(filename_for_img):
	get_pre_img = read_Image_preprocessing(filename_for_img)
	get_Img_json = ocr_json_image_process(get_pre_img)

	return get_Img_json

@ocr_img_json_service.route('/ocr_img_index/', methods=['GET'])
def ocr_img_index():
	return render_template('ocr_img_json.html')

@ocr_img_json_service.route('/api/ocr_img_json', methods=['POST'])
def upload_file():
		print("proses sedang di upload")
		# check if the post request has the file part
		try:
			print(request.files)
			print("request satu lancar")
		except Exception as e:
			print(e)
		
		if 'ocr_file_img' not in request.files:
			return "Request 2 No File Part"
		
		file = request.files['ocr_file_img']

		if file.filename == '':
			return "Filename salah"
		
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			
			file_path = os.path.join(UPLOAD_FOLDER, filename)
			file.save(file_path)

			do_ocr_img_json = get_ocr_img_json(file_path)

			respon_json = str(do_ocr_img_json)
			res_json = Response(respon_json, mimetype='application/json')
			res_json.headers['Content-Disposition'] = "attachment;filename=result_ocr_img.json"

			print("Request ocr json aman")

			return res_json
		
		return "Request ocr image launched"