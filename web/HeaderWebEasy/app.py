from flask import Flask, send_file, request, jsonify

app = Flask(__name__)

IMAGE_PATH = 'image.jpg'

FLAG = "magpie{Ht+p_H3ad!!}"

@app.route('/', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def handle_requests():
    if request.method == 'GET':
        return send_file(IMAGE_PATH, mimetype='image/png')
    
    elif request.method == 'HEAD':
        return '', 200, {'FLAG': FLAG}

    elif request.method == 'POST':
        return jsonify({"message": "I aint missing my post requests..."}), 200

    elif request.method == 'PUT':
        # Return a custom message for PUT
        return jsonify({"message": "PUT!? What is this GOLF????"}), 200
    
    else:
        # Return a default message for other methods
        return jsonify({"message": "Sorry bud, your exotic HTTP methods are not welcome here."}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
