__version__ = '001'
__author__ = 'Smruti Mohanty'

from flask import request, jsonify
from app import app, db
from models import Family, Person, GiftAssigned
import random
import time
import pandas as pd
import re


def sanitize_sticker(sticker):
    if not sticker:
        return None
    sanitized = re.sub(r'[^a-zA-Z0-9]', '', sticker)
    return sanitized.lower()


print(sanitize_sticker("You're A Star"))

@app.route('/test_populate_db', methods=['POST'])
def populate_db():
    test_data = [
        ("Jitu", "Jitu", False, "Sparkle"),
        ("Mana", "Jitu", False, "Whimsy"),
        ("", "Jitu", True, "Starry"),
        ("Murali", "Murali", False, "Mistletoe"),
        ("Rishvi", "Murali", False, "Frosty"),
        ("Akshara", "Murali", True, "Cheer"),
        ("Arjun", "Murali", True, "Radiance"),
        ("Sibu", "Sibu", False, "Dazzle"),
        ("Bandita", "Sibu", False, "Glee"),
        ("Rio", "Sibu", True, "Bliss"),
        ("Bulu", "Bulu", False, "Twinkle"),
        ("Manisha", "Bulu", False, "Charm"),
        ("Tanvi", "Bulu", True, "Sassy"),
        ("Suresh", "Suresh", False, "Happy"),
        ("Piyali", "Suresh", False, "Playful"),
        ("Adya", "Suresh", True, "Bubbly"),
        ("Kaya", "Suresh", True, "Giggles"),
        ("Nishant", "Nishant", False, "Cuddle"),
        ("Vini", "Nishant", False, "Funky"),
        ("", "Nishant", True, "Cloudy"),
        ("Raghav", "Raghav", False, "Lively"),
        ("Anuja", "Raghav", False, "Daring"),
        ("Eshani", "Raghav", True, "Punny"),
        ("Jassi", "Jassi", False, "Silly"),
        ("Richa", "Jassi", False, "Jolly"),
        ("Neer", "Jassi", True, "Nifty"),
        ("Ranji1", "Ranji1", False, "Zany"),
        ("Aaron", "Ranji1", True, "Chill"),
        ("Anoop", "Ranji1", False, "Witty"),
        ("Anusha", "Ranji1", False, "Fabulous"),
        ("Neha", "Ranji1", False, "Quirky"),
        ("Nikita", "Ranji1", False, "Vibrant"),
        ("Sandy", "Sandy", False, "Dandy"),
        ("Shradha", "Sandy", False, "Eager"),
        ("Krish", "Sandy", True, "Lovely"),
        ("Mahesh", "Mahesh", False, "Dovey"),
        ("", "Mahesh", True, "Howdy"),
    ]

    try:
        # Clear existing data (optional)
        db.session.query(Person).delete()
        db.session.query(Family).delete()

        families_set = set()  # To track unique families

        for person_name, family_name, is_child_gift, sticker_name in test_data:
            if family_name not in families_set:
                new_family = Family(family_name=family_name)
                db.session.add(new_family)
                families_set.add(family_name)

            new_person = Person(
                person_name=person_name,
                family_name=family_name,
                sticker_name=sticker_name,
                is_child_gift=is_child_gift
            )
            db.session.add(new_person)

        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Database populated successfully!'}), 201


@app.route('/getFamilyGift/<family>', methods=['GET'])
def get_family_gift(family):
    gifts = Person.query.filter_by(family_name=family).all()
    result = [[gift.family_name, gift.person_name, gift.is_child_gift, gift.sticker_name] for gift in gifts]
    return jsonify(result), 200


@app.route('/person', methods=['GET'])
def get_person():
    persons = Person.query.all()
    result = [person.person_name for person in persons if person.person_name]
    return jsonify({"names": result}), 200


@app.route('/selectWinner/<sticker_name>', methods=['GET'])
def select_winner(sticker_name):
    # Step 1: Check if the sticker exists and has not been delivered
    print("********" * 10)
    print(f"Assigning Gift: {sticker_name}")
    sticker_name = sanitize_sticker(sticker_name)
    person_gift_object = Person.query.filter_by(sticker_name=sticker_name).first()

    if not person_gift_object:
        return jsonify({'error': 'Sticker not found.'}), 404

    # Step 2: Check if the sticker has already been delivered
    if person_gift_object.is_delivered:  # Assuming recipient field is populated when a gift is assigned
        return jsonify({'error': 'This sticker has already been delivered.'}), 400

    originating_family = person_gift_object.family_name
    print(f'Originating Family: {originating_family}')

    # Step 3: Get all persons excluding those from the originating family
    eligible_recipients = Person.query.filter(
        Person.family_name != originating_family,
        Person.is_child_gift == person_gift_object.is_child_gift,
        Person.person_name is not None,
        Person.person_name != ""
    ).all()
    print(f'eligible_recipients : {eligible_recipients}')
    # Step 4: Ensure at least everyone has received a gift once before repeating names
    already_received_names = {g.recipient for g in GiftAssigned.query.all()}
    print(f'already_received_names : {already_received_names}')
    # Step 5: Filter recipients based on whether it's a kid or adult gift
    filtered_recipients = [p for p in eligible_recipients if p.person_name not in already_received_names]
    print(f'filtered_recipients : {filtered_recipients}')
    if not filtered_recipients:
        winner = random.choice(eligible_recipients)
        print(f"Random Winner is: {winner}")
    else:
        winner = random.choice(filtered_recipients)
        print(f"Next winner is {winner}")

    # Mark the gift as delivered
    print("Marking Delivery Complete")
    person_gift_object.is_delivered = True
    db.session.commit()
    time.sleep(0.25)

    print("Updating New Assignment")
    # Update the GiftAssigned table to reflect that this sticker has been delivered
    new_gift_assignment = GiftAssigned(sticker_name=sticker_name, giver_family=originating_family,
                                       recipient=winner.person_name)
    db.session.add(new_gift_assignment)
    db.session.commit()
    time.sleep(0.25)
    print("Updated New Assignment")
    print("********" * 10)
    return jsonify({
        'winner': winner.person_name,
        'sticker_name': sticker_name,
        'giver_family': originating_family
    }), 200


@app.route('/register', methods=['POST'])
def register():
    try:
        file = "static/data/SecretSanta.xlsx"
        df = pd.read_excel(file, header=None, skiprows=1)
        print(df)
        families_set = set()
        for idx, row in df.iterrows():
            print(row)
            family_name = row[0].strip() if pd.notna(row[0]) else None
            person_name = row[1].strip() if pd.notna(row[1]) else None
            is_child_gift = row[2] if pd.notna(row[2]) else None
            sticker_name = row[3].strip() if pd.notna(row[3]) else None
            sticker_name = sanitize_sticker(sticker_name)
            if family_name and family_name not in families_set:
                new_family = Family(family_name=family_name)
                db.session.add(new_family)
                families_set.add(family_name)


            if sticker_name:
                new_person = Person(
                    person_name = person_name,
                    family_name = family_name,
                    sticker_name = sticker_name,
                    is_child_gift=is_child_gift
                )
                db.session.add(new_person)
        db.session.commit()
        return jsonify({'message': 'Guest Registered Successfully!'}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error',str(e)}),500
