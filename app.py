from flask import Flask, jsonify, request, render_template,send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from flask import send_file
from gtts import gTTS
import pyttsx3
import tempfile
import os
import wave
import shutil
from flask import Response

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'khushimgajjar@9279123'
jwt = JWTManager(app)

users = {
    'broaderai': 'broaderai',
    'admin': 'admin123',
}

# Serve the login form using a GET request to '/login'
@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def get_login():
    return render_template('index.html')

# Handle the login form submission via a POST request to '/login'
@app.route('/login', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']

    if username not in users or users[username] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    # return jsonify(access_token=access_token), 200
    return render_template('upload.html',access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/text-to-speech')
def index():
    return render_template('upload.html')

# Define a route to handle the text-to-speech conversion
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        # Get the 'gender' and 'rate' parameters from the request
        gender = request.form.get('gender')
        rate = int(request.form.get('rate'))

        # Get the uploaded text file
        text_file = request.files['text_file']

        if text_file and gender and rate:
            # Read the text from the uploaded file
            text = text_file.read().decode('utf-8')
             # Get the name of the uploaded text file (without the file extension)
            text_file_name = os.path.splitext(text_file.filename)[0]

            outpath = "/var/www/texttoaudioapi/output/"

            if gender == 'female':
                # Use gTTS (Google Text-to-Speech) for female voice
                tts = gTTS(text)
                output_file = f'{text_file_name}-female.mp3'
                tts.save(outpath + output_file)
                return send_file(outpath + output_file, as_attachment=True)
            elif gender == 'male':
                # Use pyttsx3 with the default voice and adjusted rate
                engine = pyttsx3.init()
                engine.setProperty('rate', rate)  # Set the rate here
                output_file = f'{text_file_name}-male.mp3'
                engine.save_to_file(text, outpath + output_file)
                engine.runAndWait()
                return send_file(outpath + output_file, as_attachment=True)
            else:
                return jsonify({'error': 'Invalid gender specified.'}), 400
        else:
            return jsonify({'error': 'Missing parameters or text file.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

    





