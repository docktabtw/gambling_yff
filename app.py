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
    name TEXT
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
        print("user - find a user and all the bets they have made")
        print("add team - add new team")
        print("teams - find all teams that exists")
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
                c.execute("""INSERT INTO users (username, choosen_team, bet)
                            VALUES (?, ?, ?)
                            ON CONFLICT(username, choosen_team)
                            DO UPDATE SET bet = excluded.bet;""", (name, team, bet))
        else:
            print("add <username> <team> <bet>")

    elif command.startswith("delete"):
        command = command.split(" ", 3)
        if len(command) == 3:
            username = command[1]
            team = command[2]
            c.execute("DELETE * FROM users WHERE username = ? AND choosen_team = ?", (username, team))
            if c.rowcount > 0:
                print(f"Bet {username} on {team} is deleted.")
            else:
                print(f"Bet {username}")

        else:
            print("delete <username> <team>")




db.close()