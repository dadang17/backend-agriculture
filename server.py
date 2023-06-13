from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from fuzzy import fuzzy_logic

app = Flask(__name__)
app.debug = True
app.config[
    "MONGO_URI"
] = "mongodb+srv://iskandardzulqornain38:6KsKFbNIqC3aHHGF@mongodb-dadang.g2jqw6s.mongodb.net/ex-data-db?retryWrites=true&w=majority"
mongo = PyMongo(app)
# Check database connection
@app.route("/check-connection", methods=["GET"])
def check_connection():
    try:
        users = mongo.db.list_collection_names()
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500
        mongo.server_info()  # trigger exception if can't connet to db

############################### CRUD USER ################################################
# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    user = request.json
    current_time = datetime.now()
    user["createdAt"] = current_time
    user["updatedAt"] = current_time
    result = mongo.db.users.insert_one(user)
    response = {
        "message": "User Created",
        "id": str(result.inserted_id)
    }
    return jsonify(response), 201


# Retrieve all users
@app.route("/users", methods=["GET"])
def get_all_users():
    users = list(mongo.db.users.find())
    # Convert ObjectId to string
    users = [{**user, "_id": str(user["_id"])} for user in users]
    return jsonify(users), 200


# Retrieve a single user
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    else:
        return jsonify({"message": "user not found"}), 404


# Update a user
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user = request.json
    user["updatedAt"] = datetime.now() 
    result = mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set": user})
    if result.modified_count > 0:
        return jsonify({"message": "user updated successfully"}), 200
    else:
        return jsonify({"message": "user not found"}), 404


# Delete a user
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = mongo.db.users.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "user deleted successfully"}), 200
    else:
        return jsonify({"message": "user not found"}), 404



############################### CRUD SENSOR ################################################
# Create a new data sensor
@app.route("/sensors", methods=["POST"])
def create_data_sensor():
    sensor = request.json
    current_time = datetime.now()
    sensor["createdAt"] = current_time
    sensor["updatedAt"] = current_time
    result = mongo.db.sensors.insert_one(sensor)
    response = {
        "message": "Data Created",
        "id": str(result.inserted_id)
    }
    logicProcess()
    
    return jsonify(response), 201


# Retrieve all data sensors
@app.route("/sensors", methods=["GET"])
def get_all_sensors():
    sensors = list(mongo.db.sensors.find())
    # Convert ObjectId to string
    sensors = [{**sensor, "_id": str(sensor["_id"])} for sensor in sensors]
    return jsonify(sensors), 200


# Retrieve a single data
@app.route("/sensors/<id>", methods=["GET"])
def get_data_sensors(id):
    sensor = mongo.db.sensors.find_one({"_id": ObjectId(id)})
    if sensor:
        sensor["_id"] = str(sensor["_id"])
        return jsonify(sensor), 200
    else:
        return jsonify({"message": "Data not found"}), 404


# Update a data
@app.route("/sensors/<id>", methods=["PUT"])
def update_sensor(id):
    sensor = request.json
    sensor["updatedAt"] = datetime.now()
    result = mongo.db.sensors.update_one({"_id": ObjectId(id)}, {"$set": sensor})
    if result.modified_count > 0:
        logicProcess()
        return jsonify({"message": "Data updated successfully"}), 200
    else:
        return jsonify({"message": "Data not found"}), 404


# Delete a data
@app.route("/sensors/<id>", methods=["DELETE"])
def delete_sensor(id):
    result = mongo.db.sensors.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        logicProcess()
        # fuzzy_logic()
        return jsonify({"message": "Data deleted successfully"}), 200
    else:
        return jsonify({"message": "Data not found"}), 404


############################### CRUD RESULT ################################################
# Create a new result
@app.route("/results", methods=["POST"])
def create_result():
    data_result = request.json
    current_time = datetime.now()
    data_result["createdAt"] = current_time
    data_result["updatedAt"] = current_time
    result = mongo.db.results.insert_one(data_result)
    response = {
        "message": "Result Created",
        "id": str(result.inserted_id)
    }
    return jsonify(response), 201

# Retrieve all data result
@app.route("/results", methods=["GET"])
def get_all_result():
    results = list(mongo.db.results.find())
    # Convert ObjectId to string
    results = [{**result, "_id": str(result["_id"])} for result in results]
    return jsonify(results), 200


# Retrieve a single resurlt
@app.route("/results/<id>", methods=["GET"])
def get_data_results(id):
    result = mongo.db.results.find_one({"_id": ObjectId(id)})
    if result:
        result["_id"] = str(result["_id"])
        return jsonify(result), 200
    else:
        return jsonify({"message": "Result not found"}), 404


# Update a user
@app.route("/results/<id>", methods=["PUT"])
def update_result(id):
    data_result = request.json
    data_result["updatedAt"] = datetime.now() 
    result = mongo.db.results.update_one({"_id": ObjectId(id)}, {"$set": data_result})
    if result.modified_count > 0:
        return jsonify({"message": "Result updated successfully"}), 200
    else:
        return jsonify({"message": "Result not found"}), 404


# Delete a user
@app.route("/results/<id>", methods=["DELETE"])
def delete_result(id):
    result = mongo.db.results.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Result deleted successfully"}), 200
    else:
        return jsonify({"message": "Result not found"}), 404

def logicProcess():
    data = list(mongo.db.sensors.find())
    data_soil = data[-1]
    # print(data_soil)
    fuzzy_logic(data_soil['soil'])

# def get_all_result():
#     results = list(mongo.db.results.find())
#     # Convert ObjectId to string
#     results = [{**result, "_id": str(result["_id"])} for result in results]
#     return jsonify(results), 200


if __name__ == "__main__":
    app.run()
