import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(image_path)

        # Convert image to RGB mode
        image = image.convert('RGB')

        image_flip = image.transpose(Image.FLIP_LEFT_RIGHT)

        flipped_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'flip.jpg')
        image_flip.save(flipped_image_path)

        return render_template('upload.html', filename='flip.jpg')

    else:
        flash('Invalid file format. Please upload a valid image file.')
        return redirect(request.url)



@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='81')
