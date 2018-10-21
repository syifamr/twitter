from flask import Flask, Blueprint, request
from flask_restful import Resource, Api, reqparse, abort
import json
import datetime

user = []
tweet = []

with open('user.json') as file:
    user = json.load(file)

with open('tweet.json') as file:
    tweet = json.load(file)


class readAll(Resource):
    def get(self):
        return [user, tweet]

class logIn(Resource):
    def post(self):
        data = request.json
        with open('user.json') as file:
            user = json.load(file)
        for daftar in user:
            if daftar["email"] == data["email"]:
                if daftar["password"] == data["password"]:
                    return "Login Berhasil"
        return "Password kamu Salah"

def emailExist(email): 
    for data in user:
        if data["email"] == email:
            abort(400, message = "Email sudah terdaftar")

def saveUser(user):
    with open('user.json', 'w') as outfile:
            json.dump(user, outfile)
            outfile.close()

def saveTweetFile(tweet):
    with open('tweet.json', 'w') as outfile:
            json.dump(tweet, outfile)
            outfile.close()


class SignUp(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            help = "username kosong",
            required = True, 
            location = ["json"],
        )
        self.reqparse.add_argument(
            "email",
            help = "email tidak ada",
            required = True, 
            location = ["json"],
        )
        self.reqparse.add_argument(
            "password",
            help = "password tidak ada",
            required = True, 
            location = ["json"],
        )
        self.reqparse.add_argument(
            "fullname",
            help = "fullname kosong",
            required = True, 
            location = ["json"],
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        emailExist(request.json["email"])
        user.append(request.json)
        saveUser(user)
        return "Berhasil Input Data Baru"

def cek(email):
    for data in user:
        if data["email"] == email:
            return "email terdaftar"
    abort(400, message = "Email belum terdaftar")

class Tweet(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "tweet",
            help = "Tweet kamu lupa diisi",
            required = True, 
            location = ["json"]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        data = request.json
        cek(data["email"])
        time = str(datetime.datetime.now())
        penampung = {}
        penampung ["time"] = time
        req = data.copy()
        req.update(penampung) 
        tweet.append(req)
        saveTweetFile(tweet)
        return "Berhasil input tweet"

    def delete(self):
        data = request.json
        for text in tweet:
            if text["email"] == data["email"] and text["tweet"] == data["tweet"]:
                tweet.remove(text)
                saveTweetFile(tweet)
                return "Berhasil dihapus"
        return "tweetnya ga ada", 404

    def put(self):
        data = request.json
        for text in tweet:
            if text["email"] == data["email"] and text["tweet"] == data["tweetlama"]:
                text["tweet"] = data["tweetbaru"]
                text["time"] = str(datetime.datetime.now())
                saveTweetFile(tweet)
                return "Update berhasil"
        return "Gagal"


tweet_api = Blueprint('resources/tweet', __name__)
api = Api(tweet_api)
api.add_resource(readAll, 'baca')
api.add_resource(logIn, 'login')
api.add_resource(SignUp, 'Signup')
api.add_resource(Tweet, 'tweet')