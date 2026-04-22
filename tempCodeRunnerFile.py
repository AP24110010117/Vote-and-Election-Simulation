import json
import hashlib
import csv
import datetime
import os
import random
import time
import matplotlib.pyplot as plt

CANDIDATE_FILE = "candidates.json"
VOTER_FILE = "voters.json"

ADMIN_ID = "admin"
ADMIN_PASSWORD = "admin123"



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def initialize_files():
    for file in [CANDIDATE_FILE, VOTER_FILE]:
        if not os.path.exists(file):
            save_data(file, [])


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def admin_login():
    admin_id = input("Enter Admin ID: ")
    password = input("Enter Password: ")

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
        return True
    else:
        print("Wrong Admin Credentials")
        return False

def register_voter():
    voters = load_data(VOTER_FILE)

    voter_id = input("Enter Voter ID: ")

    # check duplicate
    for v in voters:
        if v["id"] == voter_id:
            print("Voter already exists")
            return

    password = input("Enter Password: ")

    if len(password) < 4:
        print("Password too short")
        return

    voter = {
        "id": voter_id,
        "password": hash_password(password),
        "has_voted": False
    }

    voters.append(voter)
    save_data(VOTER_FILE, voters)

    print("Voter Registered")


def login():
    voters = load_data(VOTER_FILE)

    voter_id = input("Enter Voter ID: ")
    password = hash_password(input("Enter Password: "))

    for v in voters:
        if v["id"] == voter_id and v["password"] == password:
            print("Login Success")
            return v

    print("Invalid Login")
    return None


def register_candidate():
    candidates = load_data(CANDIDATE_FILE)

    name = input("Enter Candidate Name: ")

    for c in candidates:
        if c["name"].lower() == name.lower():
            print("Candidate already exists")
            return

    party = input("Enter Party Name: ")

    candidate = {
        "id": len(candidates) + 1,
        "name": name,
        "party": party,
        "votes": 0
    }

    candidates.append(candidate)
    save_data(CANDIDATE_FILE, candidates)

    print("Candidate Added")


def vote(user):
    if user["has_voted"]:
        print("You already voted")
        return

    candidates = load_data(CANDIDATE_FILE)
    voters = load_data(VOTER_FILE)

    print("\nCandidates List:")
    for c in candidates:
        print(c["id"], c["name"], "-", c["party"])

    try:
        choice = int(input("Enter Candidate ID: "))
    except:
        print("Invalid Input")
        return

    selected = None
    for c in candidates:
        if c["id"] == choice:
            c["votes"] += 1
            selected = c
            break

    if selected is None:
        print("Invalid Candidate")
        return

    for v in voters:
        if v["id"] == user["id"]:
            v["has_voted"] = True

    save_data(CANDIDATE_FILE, candidates)
    save_data(VOTER_FILE, voters)

    print("Vote Successfully Done")


def show_results():
    candidates = load_data(CANDIDATE_FILE)

    total_votes = 0
    for c in candidates:
        total_votes += c["votes"]

    for c in candidates:
        print(c["name"], "-", c["votes"])

    if total_votes == 0:
        print("No votes yet")
        return

    winner = max(candidates, key=lambda x: x["votes"])
    print("Winner:", winner["name"])

def export_results():
    candidates = load_data(CANDIDATE_FILE)
    voters = load_data(VOTER_FILE)

    total_votes = sum(c["votes"] for c in candidates)
    turnout = (total_votes / len(voters) * 100) if voters else 0

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Report", datetime.datetime.now()])
        writer.writerow(["Total Voters", len(voters)])
        writer.writerow(["Total Votes", total_votes])
        writer.writerow(["Turnout", f"{turnout:.2f}%"])
        writer.writerow([])

        writer.writerow(["ID", "Name", "Party", "Votes"])
        for c in candidates:
            writer.writerow([c["id"], c["name"], c["party"], c["votes"]])

    print("CSV Exported")


def show_analysis():
    candidates = load_data(CANDIDATE_FILE)

    names = [c["name"] for c in candidates]
    votes = [c["votes"] for c in candidates]

    if sum(votes) == 0:
        print("No votes yet")
        return

    for c in candidates:
        percent = (c["votes"] / sum(votes)) * 100
        print(c["name"], f"{percent:.2f}%")

    plt.bar(names, votes)
    plt.title("Voting Results")
    plt.show()

    plt.pie(votes, labels=names, autopct='%1.1f%%')
    plt.show()



def menu():
    while True:
        clear()

        print("\n1. Register Voter")
        print("2. Register Candidate")
        print("3. Vote")
        print("4. Show Results")
        print("5. Analysis")
        print("6. Export")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear()
            if admin_login():
                clear()
                register_voter()
                input("Press Enter...")

        elif choice == "2":
            clear()
            if admin_login():
                clear()
                register_candidate()
                input("Press Enter...")

        elif choice == "3":
            clear()
            user = login()
            if user:
                clear()
                vote(user)
                input("Press Enter...")

        elif choice == "4":
            clear()
            show_results()
            input("Press Enter...")

        elif choice == "5":
            clear()
            show_analysis()
            input("Press Enter...")

        elif choice == "6":
            clear()
            export_results()
            input("Press Enter...")

        elif choice == "7":
            break

        else:
            print("Invalid Choice")
            input("Press Enter...")


initialize_files()
menu()