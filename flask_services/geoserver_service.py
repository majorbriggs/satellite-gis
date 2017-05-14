from flask import Flask, jsonify, request
from flask import make_response
from background import check_image_exists
from multiprocessing import Process
from background import add_new_rgb
app = Flask(__name__)



@app.route('/add_rgb', methods=['GET'])
def get_rgb():
    path = request.args.get('path')
    if not path:
        return make_response('Bad request. Provide a non empty path parameter', 400)
    if check_image_exists(image_path=path, type='rgb'):
        return make_response(jsonify({"path":path, "status":"DONE"}))
    if check_image_exists(image_path=path, type='rgb_started'):
        return make_response(jsonify({"path":path, "status":"IN_PROGRESS"}), 202)
    else:
        p = Process(target=add_new_rgb, kwargs={"image_path":path})
        p.start()
        return make_response(jsonify({"path":path,
                    "status":"STARTED"}), 202)

@app.route('/add_ndvi', methods=['GET'])
def get_ndvi():
    path = request.args.get('path')
    if not path:
        return make_response('Bad request. Provide a non empty path parameter', 400)
    # target: add to que

    return make_response(jsonify({"path":path,
                    "status":"Processing started"}), 202)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')