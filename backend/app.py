from crypt import methods
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask("bazinga")
CORS(app)
app.config["SECRET_KEY"] = "deadbeef"

USERS = {
    "admin": {
        'email': 'qqq@ppp.pl',
        'username': 'admin',
        'password': 'sha256$xiHnJDKat47txpFr$b293066587460c25e3da912e58a5ac0926714398556d5f23999d563c2683d1c0'
    }
}

def token_required(func):
    def decorator(*args, **kwargs):
        token = None
        print(request.headers)
        if "X-Access-Token" in request.headers:
            token = request.headers["X-Access-Token"]

        if token == None:
            return jsonify({"message": "token not found"})

        data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        current_user = USERS[data["username"]]

        return func(current_user, *args, **kwargs)
    return decorator

@app.route("/")
def home():
    return jsonify({"message": "Hello world"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    print(data)

    USERS[data["username"]] = {
        "email": data["email"],
        "username": data["username"],
        "password": generate_password_hash(data["password"], method="sha256")
    }

    print(USERS[data["username"]])

    return jsonify({"message": "user created"})

@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()

    user = USERS[data["username"]]

    if check_password_hash(user["password"], data["password"]):
        token = jwt.encode({
            "username": user["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        },
            app.config["SECRET_KEY"]
        )

        return jsonify({
            "token": token,
            "username": user.get("username"),
            "email": user.get("email"),
            "id": user.get("username"),
            "roles": ["administrator", "manager"]
        })

    return make_response("could not verify", 401, {"message": "login failed"})

@app.route("/user", methods=["GET"]) # GET jest domyślne
@token_required
def user_page(current_user):
    print(current_user)
    return jsonify({
        "message": f"You are authneticated as {current_user['username']}"
    })

if __name__ == "__main__":
    app.run(debug=True)
