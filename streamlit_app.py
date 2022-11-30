import streamlit as st
from numpy import load
from numpy import expand_dims
from matplotlib import pyplot
from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf
from tensorflow import keras
import datetime
import cv2
import numpy as np
import os
import pandas as pd

df=pd.read_csv('small_df.csv')
df['Time'] = pd.to_datetime(df['Time'])
st.write(df['Time'][0])

st.header('GRIP Team')
st.header("Stage predictor using images")
st.write("Upload image to get its corresponding stage")

uploaded_file = st.file_uploader("Choose an image...")

def verify_class(image,model=keras.models.load_model('Classifier')):   
	img_width, img_height = 150, 150
	img = keras.preprocessing.image.load_img(image)
	img = tf.image.central_crop(img, central_fraction=0.5)
	img = tf.image.resize(img,[img_width, img_height])
	img = keras.utils.img_to_array(img)
	img = np.expand_dims(img, axis = 0)
	res=model.predict(img)
	
	return res


def load_image(filename, size=(512,512)):
	# load image with the preferred size
	pixels = load_img(filename, target_size=size)
	# convert to numpy array
	pixels = img_to_array(pixels)
	# scale from [0,255] to [-1,1]
	pixels = (pixels - 127.5) / 127.5
	# reshape to 1 sample
	pixels = expand_dims(pixels, 0)
	return pixels



if uploaded_file is not None:
	#src_image = load_image(uploaded_file)
	upimage = Image.open(uploaded_file)	

	st.image(uploaded_file, caption='Input Image', use_column_width=True)

	pred_class=verify_class(uploaded_file)


	if int(pred_class[0][0].round()==0):
		st.write('Image loaded is not suitable for the prediction model')
		d = st.date_input("Please select the date of the Stage to load",
		datetime.date(2012, 6, 9),
		min_value=datetime.date(2012, 6, 9),
		max_value=datetime.date(2019, 10, 11))
		t = st.time_input('Select the time for that date',datetime.time(0, 0))
		#st.write('The closest Stage to your date is:', d,t)
		
		date=datetime.datetime.combine(d,t)
		st.write(str(date))
		df.index.searchsorted(date)
		
		s = df.loc[df.index.unique()[df.index.unique().get_loc(datetime.timestamp(date), method='nearest')]]
		st.write('The closest Stage to your date is: ',s['Stage'])
	elif int(pred_class[0][0].round()==1):
		st.write('Predicted Stage:')
		st.write('Our model:',0)
		st.write('VGG:',0)
