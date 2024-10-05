from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load your Keras model here
model2 = load_model('plant_species_recognition_model222.keras')

# Define your species names here
spiciesname = ['African Violet (Saintpaulia ionantha)',
 'Aloe Vera',
 'Anthurium (Anthurium andraeanum)',
 'Areca Palm (Dypsis lutescens)',
 'Asparagus Fern (Asparagus setaceus)',
 'Begonia (Begonia spp.)',
 'Bird of Paradise (Strelitzia reginae)',
 'Birds Nest Fern (Asplenium nidus)',
 'Boston Fern (Nephrolepis exaltata)',
 'Calathea',
 'Cast Iron Plant (Aspidistra elatior)',
 'Chinese Money Plant (Pilea peperomioides)',
 'Chinese evergreen (Aglaonema)',
 'Christmas Cactus (Schlumbergera bridgesii)',
 'Chrysanthemum',
 'Ctenanthe',
 'Daffodils (Narcissus spp.)',
 'Dracaena',
 'Dumb Cane (Dieffenbachia spp.)',
 'Elephant Ear (Alocasia spp.)',
 'English Ivy (Hedera helix)',
 'Hyacinth (Hyacinthus orientalis)',
 'Iron Cross begonia (Begonia masoniana)',
 'Jade plant (Crassula ovata)',
 'Lilium (Hemerocallis)',
 'Lily of the valley (Convallaria majalis)',
 'Money Tree (Pachira aquatica)',
 'Monstera Deliciosa (Monstera deliciosa)',
 'Orchid',
 'Parlor Palm (Chamaedorea elegans)',
 'Peace lily',
 'Poinsettia (Euphorbia pulcherrima)',
 'Polka Dot Plant (Hypoestes phyllostachya)',
 'Ponytail Palm (Beaucarnea recurvata)',
 'Pothos (Ivy arum)',
 'Prayer Plant (Maranta leuconeura)',
 'Rattlesnake Plant (Calathea lancifolia)',
 'Rubber Plant (Ficus elastica)',
 'Sago Palm (Cycas revoluta)',
 'Schefflera',
 'Snake plant (Sanseviera)',
 'Tradescantia',
 'Tulip',
 'Venus Flytrap',
 'ZZ Plant (Zamioculcas zamiifolia)']
minSize = 202  # Set this to your model's expected input size

def classify_image(image_path):
    input_img = center_crop_and_resize(image_path)
    input_img_arr = tf.keras.utils.img_to_array(input_img)
    input_img_exp_dim = tf.expand_dims(input_img_arr, 0)
    
    prediction = model2.predict(input_img_exp_dim)
    result = tf.nn.softmax(prediction[0])
    outcome = 'The Image Belongs To ' + spiciesname[np.argmax(result)] + ' with a score of ' + str(np.max(result) * 100)
    return outcome

def center_crop_and_resize(image_path, target_size=(minSize, minSize)):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    min_dim = min(width, height)
    
    x1 = (width - min_dim) // 2
    y1 = (height - min_dim) // 2
    x2 = x1 + min_dim
    y2 = y1 + min_dim
    
    cropped_image = image[y1:y2, x1:x2]
    resized_image = cv2.resize(cropped_image, target_size, interpolation=cv2.INTER_AREA)
    return resized_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.json['image']
    image_data = data.split(',')[1]  # Get the base64 part
    image_path = os.path.join('uploads', 'captured_image.png')

    # Decode the image and save it
    with open(image_path, 'wb') as fh:
        fh.write(base64.b64decode(image_data))

    # Classify the image
    outcome = classify_image(image_path)

    return jsonify({'result': outcome}), 200

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'), debug=True)
