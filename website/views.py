import logging
from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for, session
from sqlconnector.sqlReader import *
from mythicgroupmaker.group_init import main
from sqlconnector.sqlReader import clear_database
from sqlconnector.sqlReader import create_dict_from_db, delete_entry
import requests
import random

views = Blueprint('views', __name__)

logger = logging.getLogger(f"main.{__name__}")


@views.route("/create_session")
def new_session():
    invalidSession = True
    while invalidSession is True:
        rndNum = random.randint(1000, 9999)
        invalidSession = check_session_exists(rndNum)

    session["group id"] = rndNum
    logger.debug(rndNum)
    return redirect(url_for('views.submit_player', groupsession=rndNum))


@views.route("/join_session", methods=["POST"])
def join_session():
    groupid = request.form.get("groupid")
    session["group id"] = groupid
    logger.debug(f"joined session with groupid: {groupid}")
    return redirect(url_for("views.submit_player", groupsession=groupid))


@views.route("/cookie", methods=["GET", "POST"])
def cookies():
    if "group id" in session:
        groupid = session["group id"]
        logger.debug(f"group id is present in cookies: {groupid}")
        return render_template("home.html")
    elif "mycookie" in session:
        request.cookies.lists
        
    else:
        session["group id"] = "007"
        logger.debug("no group id in session cookies")
        return render_template("home.html")


@views.route("/set_cookie")
def set_cookie():
    s = requests.Session()
    session.permanent = True
    a_response = make_response("Hello World")
    a_response.set_cookie("mycookie", "myvalue")
    session.pop("group id")
    return a_response

@views.route("/show_cookie")
def show_cookie():
    if request.cookies.get("mycookie"):
        cookie_value = request.cookies.get("mycookie")
        logger.debug(f"mycookie value is: {cookie_value}")
        return cookie_value
    else:
        logger.debug("No cookie set")
        return make_response("No cookie set")



@views.route("/")
@views.route("/home")
def home():
    s = requests.Session()
    session.permanent = True
    if "group id" in session:    
        randSession = session.get("group id")
        return render_template("home.html", groupsession=randSession)
    
    return render_template("home.html")
 

@views.route("/player_entry", methods=["GET", "POST"])
def submit_player():
    if request.method == "POST":
        playerName = request.form.get("playerName")
        characterName = request.form.get("characterName")
        className = request.form.get("class")
        role = request.form.getlist("role")
        groupid = request.form.get("groupSession")
        randSession = session.get("group id")
        logger.debug(f"group id associated with this entry: {groupid}")


        if len(role) < 1:
            flash("Please select at least One role", "error")
            return render_template("player_entry.html",groupsession=randSession)
        elif "Tank" in role or "Healer" in role:
            tankConfidence = request.form.get("tank-confidence")
            healerConfidence = request.form.get("healer-confidence")
            if "Tank" in role and "Healer" in role:
                entryResponse = player_entry(playerName, characterName, className, role, groupid, tankConfidence=tankConfidence, healerConfidence=healerConfidence)
            elif "Tank" in role:
                entryResponse = player_entry(playerName, characterName, className, role, groupid, tankConfidence=tankConfidence)
            else:
                entryResponse = player_entry(playerName, characterName, className, role, groupid, healerConfidence=healerConfidence)
                
            
        else:
            entryResponse = player_entry(playerName, characterName, className, role, groupid)

        if entryResponse.status_code == 200:
            flash(f"Character {characterName} added successfully", "message")
            return render_template("/player_entry.html", groupsession=randSession)
        elif entryResponse.status_code == 500:
            flash("There was an error adding your character", "error")
            return render_template("/player_entry.html", groupsession=randSession)
    elif "group id" in session:    
        randSession = session.get("group id")
        logger.debug(f"group id is: {randSession}")
        return render_template("player_entry.html", groupsession=randSession)
    else:
        flash("you need to join a session or create a new session", "error")
        logger.debug("no 'group id' found in session")
        return render_template("home.html")

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
        randSession = session.get("group id")
        CharacterName = request.form.get("characterName")
        return render_template("delete_verify.html", CharacterName=CharacterName)
    else:
        if "group id" in session:    
            randSession = session.get("group id")
            playersDictDB = create_dict_from_db(randSession)
            playersDictlength = []
            if playersDictDB:
                for i in playersDictDB:
                    playersDictlength.append(playersDictDB.get(i))
                TotalPlayers = []
                for player in playersDictlength:
                    TotalPlayers.append(playersDictlength.index(player)+1)
                logger.debug(f"Total players: {TotalPlayers}")
                return render_template("current_players.html", playersListDB=playersDictDB, totalplayers=TotalPlayers[-1],groupsession=randSession)
            else:
                return render_template("current_players.html", playersListDB=playersDictDB, totalplayers=0, groupsession=randSession)
        else:
            flash("you need to join a session or create a new session", "error")
            logger.debug("no 'group id' found in session")
            return render_template("home.html")    




@views.route("/api/current_players", methods=["GET", "POST"])
def get_players_from_db():

    if request.method == "POST":
        pdict = create_dict_from_db()
        playerName = request.form.get("playerName")
        redirect(url_for('delete_user'))
        render_template("current_players_api.html", playersListDB=pdict, j=playerName)
    else:
        pdict = create_dict_from_db()
        return render_template("current_players_api.html", playersListDB=pdict, j="None")



@views.route("/create_groups")
def create_groups():
    randSession = session.get("group id")
    groupsList = main(randSession)
    length = len(groupsList)
    if length == 0:
        logger.warning("No Groups formed, or not enough players and/or roles to make a group")
        return render_template("/error.html", error="No Groups formed, or not enough players and/or roles to make a group", groupsession=randSession)
    else:
        for i in groupsList:
            for j in i.group_members:
                logger.debug(j)
        return render_template("groups_verify.html", groupsList=groupsList, len=length, groupsession=randSession)



@views.route("/somethingcool")
def something_cool():
    return render_template("somethingcool.html")



@views.route("/delete_entry", methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        randSession = session.get("group id")
        CharacterName = request.form.get("CharacterName")
        result = delete_entry(CharacterName, randSession)
        return render_template("deleted_user.html", result=result )
    return render_template("delete_entry.html", CharacterName=CharacterName)

@views.route("/delete_verify", methods=["GET", "POST"])
def delete_verify():
    if request.method == "POST":
        CharacterName = request.form.get("CharacterName")
        results = delete_entry(CharacterName)
        return render_template("deleted_user.html", results=results)
    return render_template("delete_verify.html")

