import sqlite3

db = sqlite3.connect('users.db')
c = db.cursor()

# Creating/Opening database
c.executescript("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    choosen_team TEXT,
    bet INTEGER,
    UNIQUE(username, choosen_team)
    );

CREATE TABLE IF NOT EXISTS teams (
    name TEXT UNIQUE
    );
""")
db.commit()

print("If you need a help write help")
while True:
    command = input(">>>")
    if command == 'exit':
        break
    elif command == 'help':
        print("There is all commands that you can write:")
        print("add <username> <team> <bet> - adding new user or new bet of user")
        print("delete <username> <team> - delete user's bet")
        print(" users - find all users and all the bets they have made")
        print(" user <username> - find a user and all the bets they have made")
        print("add team <team name> - add new team")
        print("teams - find all teams that exists")
    elif command.startswith("add team"):
        command = command.split(" ", 3)
        if len(command) == 3:
            team_name = command[2]
            try:
                c.execute("INSERT INTO teams (name) VALUES (?)", (team_name, ))
                db.commit()
            except sqlite3.IntegrityError:
                print(f"ERROR: Team {team_name} is already exists")
                continue
            print(f"Team {team_name} is added")
        else:
            print("add team <team name>")

    elif command.startswith("add"):
        command = command.split(" ", 4)
        if len(command) == 4 and command[1] != 'team':
            name = command[1]
            team = command[2]
            try:
                bet = int(command[3])
            except ValueError as e:
                print(e)
                continue
            c.execute("SELECT * FROM teams WHERE name = ?", (team, ))
            answer = c.fetchone()
            if not answer:
                print("team is not exists, write help for help")
            else:
                try:
                    c.execute("""INSERT INTO users (username, choosen_team, bet) VALUES (?, ?, ?)""", 
                            (name, team, bet)
                    )
                except sqlite3.IntegrityError:
                    print("User exists already")
                    
                db.commit()
                print(f"User {name}'s bet on the {team}'s team is registered. Bet: {bet} XP")
        else:
            print("add <username> <team> <bet>")

    elif command == "teams":
        c.execute("SELECT * FROM teams")
        answer = c.fetchall()
        print("All Teams:")
        for a in answer:
            print(a[0])

    elif command.startswith("delete"):
        command = command.split(" ", 3)
        if len(command) == 3:
            username = command[1]
            team = command[2]
            try:
                c.execute("DELETE * FROM users WHERE username = ? AND choosen_team = ?", (username, team))
            except Exception as e:
                print(e)
                continue
            if c.rowcount > 0:
                print(f"Bet {username} on {team} is deleted.")
            else:
                print(f"Bet {username} on {team} is not exists")

        else:
            print("delete <username> <team>")




db.close()