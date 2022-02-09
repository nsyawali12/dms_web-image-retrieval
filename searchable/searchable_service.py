
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
import searchable_model
from searchable_model import searchable_preprocess, searchable_result_pdf
import PyPDF2
from PyPDF2 import PdfFileMerger

from flask import Blueprint

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])

path_result = "./searchable/merge_result_searchable/"

searchable_pdf_service = Blueprint('searchable_service', __name__)

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_to_searchable(filename_for_searchable):
    get_pdf_img = searchable_preprocess(filename_for_searchable)
    get_result_search = searchable_result_pdf(get_pdf_img)

    path_to_img_pdf = "./searchable/output_path_searchable/"
    # merge_each_img = merging_pdf_to_file(path_to_img_pdf)
    
    # return merge_each_img
    return get_result_search

@searchable_pdf_service.route('/searchable_index/', methods=['GET'])
def search_index():
    # return "This is PDF convert into a searchable PDF"
    return render_template('searchable.html')

@searchable_pdf_service.route('/api/searchable_pdf', methods=['POST'])
def upload_file():
        print("proses sedang di upload")

        #check if the post request has file part
        try:
            print(request.files)
            print("request satu lancar")
        except Exception as e:
            print(e)
    
        if 'searchable_file' not in request.files:
            # flash('No file part')
            return "request 2 No file part"
            # print("sampai if 1 aman")
        file = request.files['searchable_file']

        if file.filename == '':
            return "Filename salah"
    
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            do_pdf_to_searchable = pdf_to_searchable(file_path)
            print(do_pdf_to_searchable)

            print('Goes Merging all the PDF')

            # Tagged
            path_to_img_pdf = "./searchable/output_path_searchable/"

            num_dir = os.listdir(path_to_img_pdf)
            num_files = len(num_dir)

            # pdf_file = path_to_img_pdf + "homeland_searchablePDF_%d.pdf"
            # print(pdf_file)

            merger = PdfFileMerger()

            for item in range(0, len(num_dir)):
                pdf_file = path_to_img_pdf + "homeland_searchablePDF_%d.pdf"
                items_pdf = pdf_file %item
                if items_pdf.endswith('.pdf'):
                    # merger.append(fileobj=open(items_pdf))
                    merger.append(items_pdf)
                
            merger.write('./searchable/merge_result_searchable/searchable_result.pdf')
            merger.close()
            merge_pdf_result = open('./searchable/merge_result_searchable/searchable_result.pdf', 'rb')
            
            response = Response(merge_pdf_result, content_type='application/pdf')
            response.headers["Content-Disposition"] = "attachment;filename=searchable_pdf.pdf"
            
            # merger.write(response)

            print("Request PDF Searchable aman")

            return response
        
        return "Request ocr lancar"