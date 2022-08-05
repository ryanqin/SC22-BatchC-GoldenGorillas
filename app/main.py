from flask import Flask, render_template, url_for, send_from_directory
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from url_utils import get_base_url
import os, sys
import torch
from detect import Detector

port = 8000
base_url = get_base_url(port)

if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(["png", "jpeg", "jpg", "heic"]) #allowed file types

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

# Ensure flask only uses https so cocalc doesn't get mad
class ForceHttpsRedirects:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["wsgi.url_scheme"] = "https"
        return self.app(environ, start_response)

app.wsgi_app = ForceHttpsRedirects(app.wsgi_app)

detector = Detector('aug5-v9.pt', 0.6)
detector.load_model()

# check for legit file
def allowed(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS #-1 will look at last index, in case the files named like `test.thing.png`

@app.route(f'{base_url}', methods=['GET', 'POST'])
def home():
    print(request.method + " home")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("uploaded_file")
            return redirect(url_for('uploaded_file', filename=filename, code=302))
    return render_template("index.html")

# Creates separate link/page for the about page 
@app.route(f'{base_url}/about', methods=['GET'])
def about():
    return render_template("about.html")

# Create separate link/page for the inspiration page
@app.route(f'{base_url}/inspo', methods=['GET'])
def inspo():
    return render_template("inspo.html")

# delete a generated file after viewing
@app.route(f'{base_url}/clear', methods=['GET'])
def clear():
    for file in os.listdir(UPLOAD_FOLDER):
        for ext in ALLOWED_EXTENSIONS:
            if file.endswith(ext):
                os.remove(os.path.join(UPLOAD_FOLDER, file))
    return "200";

#detect coins and total $
@app.route(f'{base_url}/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    here = os.getcwd()
    image_path = os.path.join(here, app.config['UPLOAD_FOLDER'], filename)
    save_path = os.path.join(here, app.config['UPLOAD_FOLDER'])

    print("loading")
    #run detection on image
    detector.infer(image_path, save_path)

    print("loading")
    #get total amount in each currency
    total_amounts = {'USD': 0, 'CAD': 0, 'EUR': 0, 'JPY': 0}

    for key in total_amounts:
        total_amounts[key] = detector.get_total_amount(key)

    print("loading")
    #get number of detections per class
    num_per_coin = detector.get_num_coins()

    print('total_amounts', str(total_amounts))

    out_info = {
        # 'result': "".join(image_path.split(".")[0:-1]) + "-boxed" + image_path.split(".")[-1],
        'result': os.path.join(app.config['UPLOAD_FOLDER'], "".join(filename.split(".")[0:-1]) + ".jpg"),
        'amounts': total_amounts,
        'detections': num_per_coin
    }
    print('total amounts', out_info['amounts'])
    return out_info

@app.route(f'{base_url}/uploads/<path:filename>')
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ =="__main__":
    website_url = 'cocalc20.ai-camp.dev'
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host="0.0.0.0", port=port, debug = True)