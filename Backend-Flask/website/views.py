import logging
import requests


from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    flash,
    redirect,
    url_for,
    session,
)
from mythicgroupmaker.group_init import main
from sqlconnector.sqlReader import *

from website.auth import login_required
from utils.helpers import build_success_response, build_error_response

views = Blueprint("views", __name__, url_prefix="/groups")

logger = logging.getLogger(f"main.{__name__}")


@views.route("/index")
@views.route("/")
def home():
    return redirect(url_for(".submit_player"))


@views.route("/api/create-groups", methods=["POST"])
def create_groups():
    if request.method == "POST":
        data = request.json
        logger.debug("Create groups with: %s", data)
        groups_list, players_list = main(data)
        logger.debug("playerlist after groups made: %s", players_list)
        length = len(groups_list)
        if length == 0:
            logger.warning(
                "No Groups formed, or not enough players and/or roles to make a group"
            )
            return build_error_response(
                "No groups formed, or not enough players and/or roles to make a group",
                400,
            )
        return build_success_response("Groups created successfully", 200)


@views.route("/edit_entry", methods=["GET", "POST"])
@login_required
def edit_entry():
    if request.method == "POST":
        data = request.form.to_dict()
        logger.debug(data)
        if data.get("characterName"):
            CharacterName = data["characterName"]
            logger.info(f"Editing key info for: {CharacterName}")
            keyinfo = get_key_info(CharacterName)
            return render_template(
                "edit_key.html",
                character=keyinfo[0],
                dungeon=keyinfo[1],
                keylevel=keyinfo[2],
                dungeons_list=get_dugeons_list(),
            )
        if data.get("dungeon"):
            CharacterName = data.get("charactername")
            result = edit_key_info(
                CharacterName=data.get("charactername"),
                level=data.get("keylevel"),
                dungeon=data.get("dungeon"),
            )
            if result > 0:
                flash(f"Character {CharacterName} Key edited successfully", "message")
                return redirect(url_for(".current_players"))
            else:
                flash(
                    f"there was an error updating the key info, rows edited: {result}"
                )
                return redirect(url_for(".current_players"))


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
    return redirect(url_for("views.submit_player"))


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
