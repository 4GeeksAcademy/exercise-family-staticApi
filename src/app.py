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
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET', 'POST', 'DELETE'])
def retrive_one_menber(member_id):
    # this is how you can get a member
    if request.method == 'GET': 
        member = jackson_family.get_member(member_id)
        return jsonify(member), 200
    
    # this is how you can create a member
    if request.method == 'POST': 
        data = request.json  # Assuming you send JSON data in the request
        new_member = jackson_family.add_member(data)
        return jsonify(new_member), 200
    
    # DELETE request
    if request.method == 'DELETE':
        deleted = jackson_family.delete_member(member_id)
        if deleted:
            return jsonify({"message": "Member deleted successfully"}), 200
        else:
            return jsonify({"message": "Member not found"}), 404

    content = {
      "details": "Hey, there has been an error on your request"
    }
    return jsonify(content), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
