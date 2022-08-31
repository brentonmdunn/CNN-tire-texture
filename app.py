from flask import Flask, render_template, redirect, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import os

from machinelearning.inference import prediction

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']

def file_name(file):
    return file

@app.route('/')
def index():

    # type = prediction()
  
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    images = []

    # last_file = ""
    last_file = []

    for file in files:
        # last_file[0] = file
        if os.path.splitext(file)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            images.append(file)

    # ----

    # full_filename = os.path.join(app.config['UPLOAD_DIRECTORY'], images)

    # return render_template('index.html', user_image=full_filename, type=type)

    # return render_template('index.html', images=images[-1], type=type)

    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():

    route = ""

    try:
        file = request.files['file']

        if file:
            extension = os.path.splitext(file.filename)[1].lower()

            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'File is not an image.'
        
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            ))

            print("\n\n****\n\n", file_name(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            )), "\n\n****\n\n")

            route = os.path.join(
                'prediction',
                secure_filename(file.filename)
            )
  
    except RequestEntityTooLarge:
        return 'File is larger than the 16MB limit.'


    return redirect(route)

@app.route('/prediction/<file>')
def output(file):
    ouput = prediction(file)
    return render_template('output.html', type=ouput)

@app.route('/serve-image/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = { 'jpg', 'jpeg' , 'png' }


# app = Flask(__name__)


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





# @app.route("/")
# def home():
#     type = prediction()
#     return render_template('/home.html', type=type)


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''


