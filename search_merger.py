# import os
# import requests
# import json
# from re import search
# from PyPDF2 import merger
# from cv2 import merge
# from flask import Flask, request, flash, redirect, url_for, jsonify, render_template, Response, Blueprint
# from flask.helpers import make_response
# from werkzeug.utils import  secure_filename, send_from_directory
# from werkzeug.wrappers import response

from flask import Blueprint

searchable_pdf_merge = Blueprint('search_merger', __name__)

@searchable_pdf_merge.route('/search_hello/')
def search_index():
    return "This is PDF convert into a searchable PDF"
    # return render_template('doc_json.html')