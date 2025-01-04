from flask_sqlalchemy import SQLAlchemy

# Create a global db object
db = SQLAlchemy()


class Family(db.Model):
    __tablename__ = 'family'

    family_name = db.Column(db.String(8), primary_key=True)  # Increased length

    def __repr__(self):
        return f'<Family {self.family_name}>'


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_name = db.Column(db.String(8), nullable=True)  # Increased length
    family_name = db.Column(db.String(8), db.ForeignKey('family.family_name'), nullable=False)
    sticker_name = db.Column(db.String(50), unique=True, nullable=False)
    is_child_gift = db.Column(db.Boolean, default=False)
    is_delivered = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Person {self.person_name}, Family: {self.family_name}, Sticker: {self.sticker_name}>'


class GiftAssigned(db.Model):
    __tablename__ = 'gift_assigned'

    sticker_name = db.Column(db.String(50), primary_key=True)
    giver_family = db.Column(db.String(8), nullable=False)  # Increased length
    recipient = db.Column(db.String(8), nullable=False)  # Increased length

    def __repr__(self):
        return f'<GiftAssigned {self.sticker_name}, Giver: {self.giver_family}, Recipient: {self.recipient}>'
