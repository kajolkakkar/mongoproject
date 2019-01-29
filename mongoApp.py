from flask import Flask, request, jsonify
from bson.objectid import ObjectId

app = Flask(__name__)

# Database Connection
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
col = mydb["Users"]


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    new_user = request.json

    col.insert_one(new_user)
    return jsonify("Inserted")

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    users = []
    cur = col.find()
    print(cur)
    for data in cur:
        data["_id"] = str(data["_id"])
        users.append(data)

    return jsonify(users)

# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    data = col.find_one({"_id":ObjectId(id)})
    data["_id"]=str(data["_id"])
    return jsonify(data)

# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = request.json
    col.update_one({"_id":ObjectId(id)},{"$set":user})
    return jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    col.delete_one({"_id":ObjectId(id)})
    return "Deleted"


if __name__ == '__main__':
    app.run(debug=True,port="5000",host="0.0.0.0")