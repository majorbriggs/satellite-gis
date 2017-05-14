from flask import Flask, jsonify, request
from flask import make_response
from background import check_file_exists
from multiprocessing import Process
from background import add_new_rgb
from geoserver_utils import download_from_s3_and_add_layer

app = Flask(__name__)



@app.route('/add_layer', methods=['GET'])
def get_rgb():
    image_key = request.args.get('imageKey')
    if not image_key:
        return make_response('Bad request. Provide a non empty imageKey parameter', 400)
    if check_file_exists(filepath=image_key):
        result = download_from_s3_and_add_layer(image_key=image_key)
        if result:
            return make_response(jsonify({"path":image_key, "status":"DONE"}), 200)
        else:
            return make_response(jsonify({"path":image_key, "status":"SERVER_ERROR"}), 500)
    else:
        return make_response(jsonify({"path":image_key, "status":"FAILED. S3 resource doesn't exist"}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')