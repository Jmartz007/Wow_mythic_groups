from . import db
from sqlalchemy.sql import func

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Players(db.Model):
    PlayerID = db.Column(db.Integer, server_default=func.nextval('non_pkey_auto_inc_seq'))
    PlayerName = db.Column(db.String(80), primary_key=True, unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    characters = db.relationship("Characters")

class Characters(db.Model):
    CharacterID = db.Column(db.Integer)
    CharacterName = db.Column(db.String(80), primary_key=True, unique=True)
    PlayerName = db.Column(db.String(80), db.ForeignKey("players.PlayerName"))
    Class = db.Column(db.String(80))
    keys = db.relationship("Keys")
    roles = db.relationship("Role_Entries")

class Role_Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CharacterName = db.Column(db.String(80), db.ForeignKey("characters.CharacterName"))
    Role = db.Column(db.String(80))

class Keys(db.Model):
    KeyID = db.Column(db.Integer, primary_key=True)
    CharacterName = db.Column(db.String(80), db.ForeignKey("characters.CharacterName"))
    Dungeon = db.Column(db.String(80))
    Level = db.Column(db.Integer)





"""  "Jmartz": {"Calioma" : {"Level": 7, "Dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"Level": 3, "Dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"Level": 16, "Dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}}, """