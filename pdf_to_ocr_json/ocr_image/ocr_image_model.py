from csv import reader
from unittest import result
import numpy as np
import pdf2image
from pdf2image import convert_from_path
import easyocr
import PIL
from PIL import ImageDraw, Image, ImageFont
import spacy

from IPython.display import display, Image

import os
import tempfile
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

import json

def plot_img(images, titles):
  fig, axs = plt.subplots(nrows = 1, ncols = len(images), figsize = (15, 15))
  for i, p in enumerate(images):
    axs[i].imshow(p, 'gray')
    axs[i].set_title(titles[i])
    #axs[i].axis('off')
  plt.show()

def draw_boxes(image, bounds, color='yellow', width=2):
  draw = ImageDraw.Draw(image)
  for bound in bounds:
    p0, p1, p2, p3 = bound[0]
    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    try:
      draw.text(p0, bound[1], font=font, fill='red')
    except:
      print(bound[1])
  return image

def read_Image_preprocessing(filename_img):
	file_img = filename_img
	
	img = cv2.imread(file_img) # problem possibility

	## Input Threshold Preprocess
	img = cv2.medianBlur(img, 5)

	ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	## Plotting images
	result_img = [img, th1]

	return th1

def ocr_json_image_process(pre_img):
	reader = easyocr.Reader(['id'])
	font = ImageFont.load_default()

	bounds = reader.readtext(np.array(pre_img), min_size=0, slope_ths=0.2,
													ycenter_ths=0.7, height_ths=0.6, width_ths=0.8,
													decoder='beamsearch', beamWidth=10)
	
	pre_copy = PIL.Image.fromarray(pre_img)

	draw_boxes(pre_copy, bounds, color='red')

	text= ''
	result_text = []

	for i in range(len(bounds)):
		text = bounds[i][1]
		result_text.append(text)

	result_json = {
		"semua_text_ocr": result_text
	}

	return result_json

