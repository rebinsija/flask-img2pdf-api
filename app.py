from flask import Flask, request, url_for, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json, os
from PIL import Image

UPLOAD_FOLDER = 'folder_file'
HOSTNAME = 'http://localhost:2390/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

CORS(app)

identitas = {}

class ContohResource(Resource):
	def get(self):
		response = {"msg": "Hello World, this is my first RESTful"}
		return response

	def post(self):
		file = request.files['file']

		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

		image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		i = image.convert('RGB')
		i.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)+'.pdf')

		return json.dumps({'ok': HOSTNAME+'files/'+filename+'.pdf'})

api.add_resource(ContohResource,"/api",methods=["GET","POST"])

@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
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