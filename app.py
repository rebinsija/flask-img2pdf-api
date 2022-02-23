from flask import Flask, request, url_for, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import json, os

UPLOAD_FOLDER = 'folder_file'
HOSTNAME = 'http://localhost:2390/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
CORS(app)

identitas = {}

class ContohResource(Resource):
	def post(self):
		file = request.files['file']

		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

		image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		i = image.convert('RGB')
		i.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)+'.pdf')

		return json.dumps({'ok': HOSTNAME+'files/'+filename+'.pdf'})

api.add_resource(ContohResource,"/api",methods=["POST"])

@app.route("/files")
def list_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/files/<path:path>")
def get_file(path):
	return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)



if __name__ == "__main__":
	app.run(debug=True,port=2390)