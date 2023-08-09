from flask import Blueprint, render_template, request, redirect, url_for
from .models import Users, Players, Characters, Role_Entries
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@views.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        email = request.form.get("email")
        print(email)
        user = Users.query.filter_by(email=email).first()
        if user:
            return redirect("/error")
        new_user = Users(email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("views.email"))
    return render_template("email.html")


@views.route("/player_entry", methods=["GET", "POST"])
def player_entry():
    if request.method == "POST":
        playerName = request.form.get("playerName")
        user = Players.query.filter_by(PlayerName=playerName).first()
        if not user:
            new_player = Players(PlayerName=playerName)
            db.session.add(new_player)
        characterName = request.form.get("characterName")
        className = request.form.get("class")
        role = request.form.getlist("role")
        for i in role:
            print(i)


        new_character = Characters(CharacterName=characterName, PlayerName=playerName, Class=className)
        db.session.add(new_character)
        
        for i in role:
            new_role = Role_Entries(Role=i, CharacterName=characterName)
            db.session.add(new_role)
        db.session.commit()
        
    return render_template("player_entry.html")



@views.route("/error", methods=["GET"])
def error():
    return render_template("error.html")