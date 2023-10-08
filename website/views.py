import logging
from flask import Blueprint, render_template, request, Response, jsonify, make_response, flash, redirect, url_for, session
from sqlconnector.sqlReader import *
from mythicgroupmaker.group_init import main
from sqlconnector.sqlReader import clear_database
from sqlconnector.sqlReader import create_dict_from_db, delete_query, delete_entry
import requests

views = Blueprint('views', __name__)

logger = logging.getLogger(f"main.{__name__}")



@views.route("/cookie", methods=["GET", "POST"])
def cookies():
    if "group id" in session:
        groupid = session["group id"]
        logger.debug("group id is present in cookies")
        return groupid
        
    else:
        session.permanent = False
        session["group id"] = "007"
        logger.debug("no group id in session cookies")
        return render_template("home.html")


@views.route("/set_cookie")
def set_cookie():
    s = requests.Session()
    a_response = make_response("Hello World")
    a_response.set_cookie("mycookie", "myvalue")
    return a_response

@views.route("/show_cookie")
def show_cookie():
    if request.cookies.get("mycookie"):
        cookie_value = request.cookies.get("mycookie")
        return cookie_value
    else:
        return make_response("No cookie set")



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
        elif "Tank" in role or "Healer" in role:
            tankConfidence = request.form.get("tank-confidence")
            healerConfidence = request.form.get("healer-confidence")
            if "Tank" in role and "Healer" in role:
                entryResponse = player_entry(playerName, characterName, className, role, tankConfidence=tankConfidence, healerConfidence=healerConfidence)
            elif "Tank" in role:
                entryResponse = player_entry(playerName, characterName, className, role, tankConfidence=tankConfidence)
            else:
                entryResponse = player_entry(playerName, characterName, className, role, healerConfidence=healerConfidence)
                
            
        else:
            entryResponse = player_entry(playerName, characterName, className, role)

        if entryResponse.status_code == 200:
            flash(f"Character {characterName} added successfully", "message")
            return render_template("/player_entry.html")
        elif entryResponse.status_code == 500:
            flash("There was an error adding your character", "error")
            return render_template("/player_entry.html")
    return render_template("player_entry.html")

@views.route("/admin/delete_players")
def delete_all_players_prompt():
    return render_template("delete_players_prompt.html")


@views.route("/admin/players_deleted")
def delete_all_players():
    clear_database()
    logger.info("All players deleted")
    return render_template("tables_deleted.html")

       

@views.route("/error", methods=["GET"])
def error():
    return render_template("error.html")



@views.route("/current_players", methods=["GET", "POST"])
def current_players():
    if request.method == "POST":
        CharacterName = request.form.get("characterName")
        return render_template("delete_verify.html", CharacterName=CharacterName)
    else:
        playersDictDB = create_dict_from_db()
        return render_template("current_players.html", playersListDB=playersDictDB)



@views.route("/api/current_players", methods=["GET", "POST"])
def get_players_from_db():

    if request.method == "POST":
        pdict = create_dict_from_db()
        playerName = request.form.get("playerName")
        redirect(url_for(delete_user))
        render_template("current_players_api.html", playersListDB=pdict, j=playerName)
    else:
        pdict = create_dict_from_db()
        return render_template("current_players_api.html", playersListDB=pdict, j="None")



@views.route("/create_groups")
def create_groups():
    groupsList = main()
    length = len(groupsList)
    if length == 0:
        logger.warning("No Groups formed, or not enough players and/or roles to make a group")
        return render_template("/error.html", error="No Groups formed, or not enough players and/or roles to make a group")
    else:
        for i in groupsList:
            for j in i.group_members:
                print(j)
        return render_template("groups_verify.html", groupsList=groupsList, len=length)



@views.route("/somethingcool")
def something_cool():
    return render_template("somethingcool.html")



@views.route("/delete_entry", methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        CharacterName = request.form.get("CharacterName")
        result = delete_entry(CharacterName)
        return render_template("deleted_user.html", result=result )
    return render_template("delete_entry.html", CharacterName=CharacterName)

@views.route("/delete_verify", methods=["GET", "POST"])
def delete_verify():
    if request.method == "POST":
        CharacterName = request.form.get("CharacterName")
        results = delete_entry(CharacterName)
        return render_template("deleted_user.html", results=results)
    return render_template("delete_verify.html")

