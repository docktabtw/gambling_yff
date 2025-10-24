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
        print("There is all commands that you can write:\n")
        print("Console commands:")
        print("    exit - Exiting the program")
        print("    help - List of all commands with an explanation of each")
        print("\nUsers Commands:")
        print("    users - Find all users and all the bets they have made")
        print("    find user <username> - Find a user and all the bets they have made")
        print("    add user <username> <team> <bet> - Adding new user or new bet of user")
        print("    delete user <username> <team> - Delete user's bet")
        print("\nTeams Commands:")
        print("    teams - Find all teams that exists")
        print("    add team <team name> - Add new team")
        print("    delete team <team> - Delete team")
    
    elif command == "teams":
        c.execute("SELECT * FROM teams")
        answer = c.fetchall()
        if answer:
            print("All Teams:\n")
            for i in answer:
                print(f"Team: {i[0]}")
    
    elif command == "users":
        c.execute("SELECT * FROM users")
        answer = c.fetchall()
        if answer:
            print("All users and their bets:\n")
            for i in answer:
                print(f"Name: {i[0]}")
                print(f"Team: {i[1]}")
                print(f"Bet: {i[2]} XP\n")
        else:
            print("ERROR: No registered users")

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

    elif command.startswith("add user"):
        command = command.split(" ", 4)
        if len(command) == 4:
            name = command[1]
            c.execute("SELECT * FROM users WHERE name = ?", (name, ))
            answer = c.fetchone()
            if not answer:
                print("user is not exists, write help for help")
            else:
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
                        print("User exists already\nUpdating his bet")
                        c.execute("UPDATE users SET bet = ? WHERE username = ? AND choosen_team = ?", 
                                (bet, name, team)
                        )
                        
                    db.commit()
                    print(f"User {name}'s bet on the {team}'s team is registered. Bet: {bet} XP")
        else:
            print("add user <username> <team> <bet>")

    elif command.startswith("delete user"):
        command = command.split(" ", 4)
        if len(command) == 4:
            username = command[2]
            team = command[3]
            try:
                c.execute("DELETE FROM users WHERE username = ? AND choosen_team = ?", (username, team))
                db.commit()
            except Exception as e:
                print(f"database Error: {e}")
                continue
            if c.rowcount > 0:
                print(f"Bet {username} on {team} is deleted.")
            else:
                print(f"ERROR: Bet {username} on {team} is not exists")

        else:
            print("delete user <username> <team>")

    elif command.startswith("delete team"):
        command = command.split(" ", 3)
        if len(command) == 3:
            name = command[2]
            try:
                c.execute("DELETE FROM teams WHERE name = ?", (name, ))
                db.commit()
            except Exception as e:
                print(f"Database Error: {e}")
                continue
            if c.rowcount > 0:
                print(f"Team {name} is deleted.")
            else:
                print(f"ERROR: Team {name} is not exists")

        else:
            print("delete team <username> <team>")

    elif command.startswith("find user"):
        command = command.split(" ", 3)
        if len(command) == 3:
            username = command[2]
            c.execute("SELECT * FROM users WHERE username = ?", (username, ))
            answer = c.fetchall()
            if answer:
                if len(answer) == 1:
                    name, team, bet = answer[0]
                    print("User is found!\n")
                    print(f"Name: {name}")
                    print(f"Team: {team}")
                    print(f"Bet: {bet} XP\n")
                else:
                    print("User is found! Multiple bets detected:\n")
                    for i, (name, team, bet) in enumerate(answer, start=1):
                        print(f"Bet #{i}:")
                        print(f"  Name: {name}")
                        print(f"  Team: {team}")
                        print(f"  Bet: {bet} XP\n")
        else:
            print("find user <username>")




db.close()