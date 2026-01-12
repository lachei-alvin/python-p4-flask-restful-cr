#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter  # Make sure your models.py defines Newsletter and db

# --- App Setup ---
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///newsletters.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# --- Resources ---


class Home(Resource):
    def get(self):
        return make_response({"message": "Welcome to the Newsletter RESTful API"}, 200)


class Newsletters(Resource):
    def get(self):
        newsletters = [n.to_dict() for n in Newsletter.query.all()]
        return make_response(newsletters, 200)

    def post(self):
        new_newsletter = Newsletter(
            title=request.form["title"], body=request.form["body"]
        )
        db.session.add(new_newsletter)
        db.session.commit()
        return make_response(new_newsletter.to_dict(), 201)


class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            return make_response(newsletter.to_dict(), 200)
        return make_response({"error": "Newsletter not found"}, 404)


# --- Add Resources to API ---
api.add_resource(Home, "/")
api.add_resource(Newsletters, "/newsletters")
api.add_resource(NewsletterByID, "/newsletters/<int:id>")

# --- Run Server ---
if __name__ == "__main__":
    app.run(port=5555, debug=True)
