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

