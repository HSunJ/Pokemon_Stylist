import flask
from flask import render_template, request

import base64
import numpy as np
import cv2
import openai
import urllib.request
from PIL import Image

import tensorflow as tf


# Initialize the useless part of the base64 encoded image.
init_Base64 = 21

# Our dictionary
label_dict = {0: 'charmander', 1: 'Magikarp', 2: 'pikachu', 3: 'Jigglypuff'}

# Initializing the Default Graph (prevent errors)
# graph = tf.compat.v1.get_default_graph()

# Use pickle to load in the pre-trained model.
#with open(f'DensNet121_model.h5', 'rb') as f:
#    model = pickle.load(f)
model = tf.keras.models.load_model('MobileNetV2_model.h5')


# Initializing new Flask instance. Find the html template in "templates".
app = flask.Flask(__name__)


def run_inference(prompt):
    print(prompt)
    response = openai.Image.create(prompt=prompt          # 텍스트 입력
                               , n=1                    # 생성할 이미지 개수
                               , size= "256x256"      # 이미지 크기
                               , api_key = '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') # openai API키
    url = response['data'][0]['url']
    print(url)
    urllib.request.urlretrieve(url, 'static/image_pokemon/output.jpg')
    return Image.open("static/image_pokemon/output.jpg")

# First route : Render the initial drawing template

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/draw')
def draw():
    return render_template('draw.html')


# Second route : Use our model to make prediction - render the results page.
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        final_pred = None
        # Preprocess the image : set the image to 28x28 shape
        # Access the image
        draw = request.form['url']
        # Removing the useless part of the url.
        draw = draw[init_Base64:]
        # Decoding
        draw_decoded = base64.b64decode(draw)
        image = np.asarray(bytearray(draw_decoded), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        # Resizing and reshaping to keep the ratio.
        resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        resized = cv2.Canny(resized, 120, 200)
        resized = cv2.merge([resized, resized, resized])
        resized = resized.reshape((1, 224, 224, 3))
        vect = np.asarray(resized, dtype="uint8")
        vect = vect.reshape(1, 224, 224, 3).astype('float32')
        # Launch prediction
        my_prediction = model.predict(vect)
        # Getting the index of the maximum prediction
        index = np.argmax(my_prediction[0])
        # Associating the index and its value within the dictionnary
        final_pred = label_dict[index]


    return render_template('results.html', prediction=final_pred)

@app.route('/final/')
def final():
    prompt = f'{request.args["pred"]},{request.args["output"]}'
    run_inference("pixel style, "+prompt)
    return render_template('final.html')

if __name__ == '__main__':
    app.run(debug=True)


