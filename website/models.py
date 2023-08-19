
if __name__ == "__main__":

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
        keys = db.relationship("Keys")
        roles = db.relationship("Role_Entries")

    class Role_Entries(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        CharacterName = db.Column(db.Integer, db.ForeignKey("characters.CharacterName"))
        Role = db.Column(db.String(80))

    class Keys(db.Model):
        KeyID = db.Column(db.Integer, primary_key=True)
        CharacterName = db.Column(db.String(80), db.ForeignKey("characters.CharacterName"))
        Dungeon = db.Column(db.String(80))
        Level = db.Column(db.Integer)
