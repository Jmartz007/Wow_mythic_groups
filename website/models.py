from . import db
from sqlalchemy.sql import func

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Players(db.Model):
    PlayerID = db.Column(db.Integer, primary_key=True)
    PlayerName = db.Column(db.String(80), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    characters = db.relationship("Characters")

class Characters(db.Model):
    CharacterID = db.Column(db.Integer, primary_key=True)
    CharacterName = db.Column(db.String(80), unique=True)
    PlayerName = db.Column(db.String(80), db.ForeignKey("players.PlayerName"))
    Class = db.Column(db.String(80))
    Role = db.Column(db.String(80))
    keys = db.relationship("Keys")
    roles = db.relationship("Role_Entries")

class Roles(db.Model):
    RoleID = db.Column(db.Integer, primary_key=True)
    Role = db.Column(db.String(80), unique=True)
    roles = db.relationship("Role_Entries")

class Role_Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CharacterName = db.Column(db.Integer, db.ForeignKey("characters.CharacterName"))
    RoleID = db.Column(db.Integer, db.ForeignKey("roles.RoleID"))

class Keys(db.Model):
    KeyID = db.Column(db.Integer, primary_key=True)
    CharacterName = db.Column(db.String(80), db.ForeignKey("characters.CharacterName"))
    Dungeon = db.Column(db.String(80))
    Level = db.Column(db.Integer)





"""  "Jmartz": {"Calioma" : {"Level": 7, "Dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"Level": 3, "Dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"Level": 16, "Dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}}, """