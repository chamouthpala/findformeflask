import werkzeug
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/uploadimage', methods=["POST"])
def uploadimage():
    if(request.method == "POST"):
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("./UploadedImage/" + filename)
        imagefile.save("./UploadedImage/" + filename)
        return jsonify({
            "message": "Image Uploaded Successfully"
        })





if __name__ == '__main__':
    app.run()
