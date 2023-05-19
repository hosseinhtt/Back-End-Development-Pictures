from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    pictures = data
    return jsonify(pictures)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for pic in data:
            if pic["id"]== id:
                return jsonify(pic)
        abort(404)        
    return "no such an account"      


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pictures = data
    picture = request.get_json()
    id = picture.get('id')

    for existing_picture in pictures:
        if existing_picture['id'] == id:
            return jsonify({'Message': f"picture with id {id} already present"}), 302

    pictures.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pictures = data
    picture_data = request.get_json()
    for picture in pictures:
        if picture['id'] == id:
            picture['event_state'] = picture_data['event_state']
            return jsonify(picture)
    abort(404)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pictures = data
    for picture in pictures:
        if picture['id'] == id:
            pictures.remove(picture)
            return '', 204
    abort(404)
