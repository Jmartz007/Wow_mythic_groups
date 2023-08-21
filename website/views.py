import logging
from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from group_init import main
from . import player_entry, clear_database
from sqlconnector.sqlReader import read_current_players_db

views = Blueprint('views', __name__)

logger = logging.getLogger()


@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")
 

@views.route("/player_entry", methods=["GET", "POST"])
def submit_player():
    if request.method == "POST":
        playerName = request.form.get("playerName")
        characterName = request.form.get("characterName")
        className = request.form.get("class")
        role = request.form.getlist("role")

        if len(role) < 1:
            flash("Please select at least One role", "error")
            return render_template("player_entry.html")
        else:
            entryResponse = player_entry(playerName, characterName, className, role)

        if entryResponse.status_code == 200:
            flash("Character added successfully", "message")
            return render_template("/player_entry.html")
        elif entryResponse.status_code == 500:
            flash("There was an error adding your character", "error")
            return render_template("player_entry")
    return render_template("player_entry.html")

@views.route("/admin/delete_players")
def delete_all_players():
    clear_database()
    return render_template("tables_deleted.html")

       

@views.route("/error", methods=["GET"])
def error():
    return render_template("error.html")



@views.route("/current_players")
def current_players():
    playersListDB = read_current_players_db()
    if type(playersListDB) ==  Response:
        return playersListDB, render_template("error.html")
    
    length = len(playersListDB)
    return render_template("current_players.html", playersListDB=playersListDB, len=length)



@views.route("/api/current_players")
def get_players_from_db():
    playersListDB = read_current_players_db()
    length = len(playersListDB)
    print("Players DB read")
    return render_template("current_players_api.html", playersListDB=playersListDB, len=length)



@views.route("/create_groups")
def create_groups():
    groupsList = main()
    length = len(groupsList)
    if length == 0:
        return render_template("/error.html")
    else:
        for i in groupsList:
            for j in i.group_members:
                print(j)
        return render_template("groups_verify.html", groupsList=groupsList, len=length)



@views.route("/somethingcool")
def something_cool():
    return render_template("somethingcool.html")



@views.route("/email", methods=["GET", "POST"])
def email():
    """ if request.method == "POST":
        email = request.form.get("email")
        print(email)
        user = Users.query.filter_by(email=email).first()
        if user:
            return redirect("/error")
        new_user = Users(email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("views.email")) """
    return render_template("email.html")

