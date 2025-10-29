import sqlite3

db = sqlite3.connect('users.db')
c = db.cursor()

# Creating/Opening database
c.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        print("    coeff - calculates the winning coefficient for each team")
        print("    count winners - calculation of the coefficient and output of the winning amount of each user")
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
        else:
            print("ERROR: No registered teams")
    
    elif command == "users":
        c.execute("SELECT * FROM users")
        answer = c.fetchall()
        if answer:
            print("All users and their bets:\n")
            for i in answer:
                print(f"Name: {i[1]}")
                print(f"Team: {i[2]}")
                print(f"Bet: {i[3]} XP")
                print(f"Received award: {bool(int(i[4]))}\n")
        else:
            print("ERROR: No registered users")

    elif command == "coeff":
        all_xp = 0
        c.execute("SELECT bet FROM users")
        all_bets = c.fetchall()
        for a in all_bets:
            all_xp += a[0]
        c.execute("SELECT * FROM teams")
        print(f"All XP: {all_xp}")
        print(f"All Bets: {len(all_bets)}")
        teams = c.fetchall()
        for t in teams:
            team_xp = 0
            c.execute("SELECT bet FROM users WHERE choosen_team = ?", (t[0], ))
            users = c.fetchall()
            bets = len(users)
            for u in users:
                team_xp += u[0]

            print(f"\nTeam: {t[0]}")
            print(f"    Team XP: {team_xp}")
            print(f"    Bets: {bets}")
            try:
                print(f"    Coefficient: {all_xp/team_xp}")
            except ZeroDivisionError:
                print(f"    Coefficient: 0")

    #count winners
    elif command == "count winners":
        teams_counter = 1
        teams_won = []
        while True:
            try:
                teams_won_count = int(input("How much teams won: "))
                break
            except ValueError:
                print("ERROR: You wrote text, not a number.")
        while teams_counter <= teams_won_count:
            print(f"Team {teams_counter}:")
            team_name = input("write team name: ")
            c.execute("SELECT * FROM teams WHERE name = ?", (team_name, ))
            team = c.fetchone()
            if not team:
                print(f"ERROR: Team {team_name} is not exists")
                continue
            else:
                teams_won.append(team_name)
                teams_counter += 1
        all_xp = 0
        c.execute("SELECT bet FROM users")
        all_bets = c.fetchall()
        for a in all_bets:
            all_xp += a[0]
        c.execute("SELECT * FROM teams")
        teams = c.fetchall()
        print(f"All XP: {all_xp}")
        print(f"All Bets: {len(all_bets)}")
        for t in teams:
            team_xp = 0
            c.execute("SELECT * FROM users WHERE choosen_team = ?", (t[0], ))
            users = c.fetchall()
            bets = len(users)
            for u in users:
                team_xp += u[3]
            if t[0] in teams_won:
                print(f"\nTeam {t[0]} won!")
                print(f"All rewards of users that betted on {t[0]}:")
                for uu in users:
                    print(f"\nID: {uu[0]}")
                    print(f"Name: {uu[1]}")
                    print(f"Bet: {uu[3]} XP")
                    print(f"Reward: {uu[3]*(all_xp/(team_xp*teams_won_count))} XP")
            else:
                print(f"\nTeam {t[0]} lose!")
                print(f"All bets of users that betted on {t[0]}:")
                for uu in users:
                    print(f"\nID: {uu[0]}")
                    print(f"Name: {uu[1]}")
                    print(f"Bet: {uu[3]} XP")
                    print(f"Reward: No award because the team lost")
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
        command = command.split(" ", 5)
        if len(command) == 5:
            name = command[2]
            c.execute("SELECT * FROM users WHERE username = ?", (name, ))
            answer = c.fetchone()
            team = command[3]
            try:
                bet = int(command[4])
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
                    db.commit()
                    print(f"User {name}'s bet on the {team}'s team is registered. Bet: {bet} XP")
                except sqlite3.IntegrityError:
                    print("INFO: User exists already\nWe add his new bet to the existing one")
                    c.execute("UPDATE users SET bet = bet + ? WHERE username = ? AND choosen_team = ?", 
                            (bet, name, team)
                    )
                    db.commit()
                    print(f"User {name}'s bet on the {team}'s team is updated. Bet: {bet} XP")
                        
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
                c.execute("DELETE FROM users WHERE choosen_team = ?", (name, ))
                db.commit()
            except Exception as e:
                print(f"Database Error: {e}")
                continue
            if c.rowcount > 0:
                print(f"Team {name} is deleted.")
                print("And All bets on that team is deleted")
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
                    id, name, team, bet, is_awarded = answer[0]
                    print("User is found!\n")
                    print(f"ID: {id}")
                    print(f"Name: {name}")
                    print(f"Team: {team}")
                    print(f"Bet: {bet} XP")
                    print(f"Received award: {bool(int(is_awarded))}\n")
                else:
                    print("User is found! Multiple bets detected:\n")
                    for i, (id, name, team, bet, is_awarded) in enumerate(answer, start=1):
                        print(f"Bet #{i}:")
                        print(f"  ID: {id}")
                        print(f"  Name: {name}")
                        print(f"  Team: {team}")
                        print(f"  Bet: {bet} XP")
                        print(f"  Received award: {bool(int(is_awarded))}\n")
        else:
            print("find user <username>")




db.close()