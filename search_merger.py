
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
import searchable
from searchable import searchable_preprocess, result_search
import PyPDF2
from PyPDF2 import PdfFileMerger

from flask import Blueprint

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF', 'jpg', 'png'])

path_to_img_pdf = "output_path_searchable/"
path_result = "./merge_result/"

searchable_pdf_merge = Blueprint('search_merger', __name__)

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_to_searchable(filename_for_searchable):
    get_pdf_img = searchable_preprocess(filename_for_searchable)
    get_result_search = result_search(get_pdf_img)

    path_to_img_pdf = "output_path_searchable/"
    # merge_each_img = merging_pdf_to_file(path_to_img_pdf)
    
    # return merge_each_img
    return get_result_search

@searchable_pdf_merge.route('/search_index/', methods=['GET'])
def search_index():
    # return "This is PDF convert into a searchable PDF"
    return render_template('search_merge.html')

@searchable_pdf_merge.route('/api/mergepdf', methods=['POST'])
def upload_file():
        print("proses sedang di upload")

        #check if the post request has file part
        try:
            print(request.files)
            print("request satu lancar")
        except Exception as e:
            print(e)
    
        if 'merge_file' not in request.files:
            # flash('No file part')
            return "request 2 No file part"
            # print("sampai if 1 aman")
        file = request.files['merge_file']

        if file.filename == '':
            return "Filename salah"
    
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            do_pdf_to_searchable = pdf_to_searchable(file_path)
            print(do_pdf_to_searchable)

            print("request ke 3 aman")

            print('Goes Merging')

            # Tagged

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
            
            # result_merger = 'search_result.pdf'

            # response = make_response(merger.write(result_merger))
            # response.headers["Content-Disposition"] = "attachment;filename=search_result.pdf"
            # response.headers.set('Content-Type', 'application/pdf')
            
            # filePath = os.path.join(path_result, os.path.basename('searchable_result.pdf'))
            # with open('./merge_result/searchable_result.pdf', 'wb') as f:
            # f.write(datatowrite.encode(encoding='UTF-8'))
                
            merger.write('merge_result/searchable_result.pdf')
            merger.close()
            respon_result = open('merge_result/searchable_result.pdf', 'rb')
            
            response = Response(respon_result, content_type='application/pdf')
            response.headers["Content-Disposition"] = "attachment;filename=searchable_pdf.pdf"
            
            # merger.write(response)

            print("Request PDF Searchable aman")

            return response
        
        return "Request ocr lancar"