import logging

from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for, session
from sqlconnector.sqlReader import *
from mythicgroupmaker.group_init import main
from sqlconnector.sqlReader import clear_database
from sqlconnector.sqlReader import create_dict_from_db, delete_player
import requests
import random

views = Blueprint('views', __name__)

logger = logging.getLogger(f"main.{__name__}")



@views.route("/")
@views.route("/home")
def home():
    return redirect("/player_entry")
    # s = requests.Session()
    # session.permanent = True
    # if "group id" in session:    
    #     randSession = session.get("group id")
    #     return render_template("home.html", groupsession=randSession)
    # else:
    #    return redirect("/player_entry")   
    # return render_template("home.html")
 
@views.route("/player_entry", methods=["GET", "POST"])
def submit_player():
    if request.method == "POST":
        combat_roles = {}
        data = request.form
        playerName = data["playerName"]
        characterName = data["characterName"]
        className = data["class"]
        combat_roles["combat_role_tank"]= data.get("combat_role_tank")
        combat_roles["tankSkill"] = data.get("tank-skill")
        combat_roles["combat_role_healer"]= data.get("combat_role_healer")
        combat_roles["healerSkill"] = data.get("healer-skill")
        combat_roles["combat_role_dps"]= data.get("combat_role_dps")
        combat_roles["dpsSkill"] = data.get("dps-skill")
        role = request.form.getlist("role")
        logger.debug(role)
        logger.debug(combat_roles)
        if len(role) < 1:
            flash("Please select at least One role", "error")
            return render_template("player_entry.html")
        else:
            entryResponse = player_entry(playerName, characterName, className, role, combat_roles)
                
        if entryResponse.status_code == 200:
            flash(f"Character {characterName} added successfully", "message")
            return redirect(url_for(".current_players"))
        elif entryResponse.status_code == 500:
            flash("There was an error adding your character", "error")
            return render_template("/player_entry.html")
    else:
        return render_template("player_entry.html")

@views.route("/current_players", methods=["GET", "POST"])
def current_players():
    if request.method == "POST":
        data = request.form.to_dict()
        if data.get("characterName"):
            CharacterName = request.form.get("characterName")
            print(CharacterName)
            return render_template("delete_character.html", CharacterName=CharacterName)
        else:
            data.get("playerName")
            PlayerName = request.form.get("playerName")
            return render_template("delete_player.html", PlayerName=PlayerName)
    else: 
        playersDB = create_dict_from_db()
        Num_players = len(playersDB)
        if Num_players > 0:
            logger.debug(f"Total players: {Num_players}")
            return render_template("current_players.html", playersListDB=playersDB,totalplayers=Num_players)
        else:
            return render_template("current_players.html", playersListDB=playersDB, totalplayers=0)

@views.route("/create_groups")
def create_groups():
    # randSession = session.get("group id")
    groupsList = main()
    length = len(groupsList)
    if length == 0:
        logger.warning("No Groups formed, or not enough players and/or roles to make a group")
        return render_template("/error.html", error="No Groups formed, or not enough players and/or roles to make a group")
    else:
        for i in groupsList:
            for j in i.group_members:
                logger.debug(j)
        return render_template("groups_verify.html", groupsList=groupsList, len=length)

@views.route("/delete_entry", methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        data = request.form.to_dict()
        logger.debug(data)
        if data.get("PlayerName"):
        # data = data.strip("()'[]").replace("'", "").split(",")
        # logger.debug(f"data is: {data}")
        # CharacterName = data[0]
            PlayerName = data["PlayerName"]
            logger.debug(f"player to be deleted: {PlayerName}")
            result = delete_player(PlayerName)
            return render_template("deleted_user.html", result=result )

        elif data.get("CharacterName"):
            CharacterName = data["CharacterName"]
            logger.debug(f"player to be deleted: {CharacterName}")
            result = delete_character(CharacterName)
            return render_template("deleted_user.html", result=result )
    return render_template("delete_entry.html", CharacterName=CharacterName)

# @views.route("/delete_verify", methods=["GET", "POST"])
# def delete_verify():
#     if request.method == "POST":
#         if request.form.getlist("PlayerName"):
#             data = request.form.getlist("PlayerName")
#             logger.debug(data)
#             CharacterName = data[0]
#             results = delete_player(CharacterName)
#             return render_template("deleted_user.html", results=results)
#     return render_template("delete_verify.html")

@views.route("/api/current_players", methods=["GET", "POST"])
def get_players_from_db():
    if request.method == "POST":
        pdict = create_dict_from_db()
        playerName = request.form.get("CharacterName")
        redirect(url_for('delete_user'))
        render_template("current_players_api.html", playersListDB=pdict, j=playerName)
    else:
        pdict = create_dict_from_db()
        return render_template("current_players_api.html", playersListDB=pdict, j="None")

@views.route("/somethingcool")
def something_cool():
    return render_template("somethingcool.html")


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

@views.route("/create_session")
def new_session():
    # invalidSession = True
    # while invalidSession is True:
    #     rndNum = random.randint(1000, 9999)
    #     invalidSession = check_session_exists(rndNum)

    # session["group id"] = rndNum
    # logger.debug(rndNum)
    # return redirect(url_for('views.submit_player', groupsession=rndNum))
    return redirect(url_for('views.submit_player'))

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