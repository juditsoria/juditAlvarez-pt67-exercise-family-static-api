"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200



@app.route('/member', methods=['POST'])
def add_member():
    request_data = request.json
    if not all (key in request_data for key in ["first_name", "age", "lucky_numbers"]):
        return jsonify ({"error" : "Bad request"}), 400
    new_member = {
        "first_name" : request_data ["first_name"],
        "age" : request_data ["age"],
        "lucky_numbers" : request_data["lucky_numbers"]
    }
    added_member = jackson_family.add_member (new_member)
    return jsonify (added_member), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    
    if member:
        
        member_response = {
            "name": f"{member['first_name']} {member['last_name']}",
            "id": member["id"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        return jsonify(member_response), 200
    else:
        return jsonify({"message": "Member not found"}), 404
    


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if jackson_family.delete_member(id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message": "Member not found"}), 404


    
@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    request_data = request.json
    updates = {key: value for key, value in request_data.items() if key in ["first_name", "age", "lucky_numbers"]}
    updated_member = jackson_family.update_member(id, updates)
    if updated_member:
        return jsonify(updated_member), 200
    else:
        return jsonify({"message": "Member not found"}), 404
    
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
