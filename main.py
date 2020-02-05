#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'game.json'


# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        return game
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)


def render(game,current):
    c = game[current]
    print("You are at the " + c["name"])
    print(c["desc"])

def get_input():
    response = input("What do you want to do? ")
    response = response.upper().strip()
    return response

def update(game,current,response,stopped):
    c = game[current]

    if current == "LOCATION2" and response == "LEAVE TOWN" and stopped:
        print("You need to get a Tokeman from the lab first!")
        return current
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]
    print("Sorry, not an option, try again")
    return current

def battling():
    print("A wild Podgey Appears!")
    print("You Send out your Peekachoo!")
    print("OPTIONS:")
    print("USE THUNDERSHOOK")
    print("USE FAST ATTACK")
    response = get_input()
    while (response != "THUNDERSHOOK") and (response != "FAST ATTACK"):
        print("USE THUNDERSHOOK or FAST ATTACK")
        if response == "USE THUNDERSHOOK":
            print("PODGEY uses BEAK STRIKE, but MISSES")
            print("PEEKACHOO uses THUNDERSHOOK: CRITICAL HIT PODGEY FAINTS")
            return "GO FORWARD"
        if response == "USE FAST ATTACK":
            print("PEEKACHOO uses FAST ATTACK, but MISSES")
            print("PODGEY uses GALE: PEEKACHOO FAINTS")
            return "LOST"
        response = get_input()

def options(game,current):
    c = game[current]
    print("Options: ")
    for e in c["exits"]:
        print(e["exit"])
# The main function for the game
def main():
    current = 'START'  # The starting location
    end_game = ['LOCATION8']  # Any of the end-game locations
    battleScenes = ["LOCATION6"]
    game = load_files()
    battle = False
    stopped = True
    while True:
        render(game,current)

        for e in end_game:
            if current == e:
                print("You win!")
                break #break out of the while loop
        for e in battleScenes:
            if current == e:
                battle = True
                battleScenes.remove(current)
        if not battle:
            if current == "LOCATION4" and stopped:
                print("The Tokeman Proffesor gives you a PEEKACHOO!")
                stopped = False
            options(game,current)
            response = get_input()
        else:
            response = battling()
            battle = False
            current = "LOCATION5"
        if response == "LOST":
            while(response != "Q"):
                print("You Blacked Out and fainted, YOU LOSE! Press Q to quit")
                response = get_input()
        if response == "QUIT" or response == "Q":
            break #break out of the while loop

        current = update(game,current,response,stopped)

    print("Thanks for playing!")

# run the main function
if __name__ == '__main__':
	main()