import enchant
import random
import itertools

# Setup an alphabet for each letter slot
wordle = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
]

# List of good starting words to choose from
starters = ["soare","roate","raise","party"]

# Grab a random start word
first_try = random.choice(starters)

yellows = []


# Function for getting the returned hint information from user
def userColorInput(word):
    word_data = []
    count=0
    for i in word:
        print("1) Correct [green]")
        print("2) Wrong place [yellow]")
        print("3) Not in word [black]")

        while True:
            count+=1
            status = int(input("Status of letter #{} -> {}: ".format(count,i.upper())))

            if status >= 1 and status <= 3:
                word_data.append({
                    "letter":i.lower(),
                    "status":status
                })
                break
            else:
                print("Enter 1, 2 or 3")

    return word_data


def processAttempt(data):
    global wordle
    global yellows

    count=0
    for d in data:
        if d["status"] == 1:
            wordle[count] = d["letter"]
        elif d["status"] == 2:
            if wordle[count]:
                wordle[count].remove(d["letter"])
                if d["letter"] not in yellows:
                    yellows.append(d["letter"])
        elif d["status"] == 3:
            i=0
            while i < 5:
                if wordle[i]:
                    wordle[i].remove(d["letter"])
                i+=1
        count+=1


def generateNextChoice():
    global wordle
    global yellows

    # Initialize the dictionary
    d = enchant.Dict("en_US")

    solution = ["","","","",""]
    words = []
    possible_words = []

    # Place all the corrects into the solution slots
    count=0
    for w in wordle:
        if len(w) == 1:
            solution[count] = w
        count+=1

    # Get all possible combinations of letters
    combos = list(itertools.product(*wordle))

    # Run through the combinations and check to see if it's a word
    for combo in combos:
        word = ""
        x=0
        while x < 5:
            word += combo[x]
            x+=1
        if d.check(word) == True:
            possible_words.append(word)

    filtered_words = []
    if yellows:
        for word in possible_words:
            print(word)
            check = any(yellow in word for yellow in yellows)
            if check == True:
                filtered_words.append(word)
            

    print(filtered_words)
        

# Show the selected word that we're starting with.
# User will have to enter this word into the game so we can get our hints.
print("\n*** First try: {} ***\n".format(first_try.upper()))

word_data = userColorInput(first_try)

processAttempt(word_data)

next_choices = generateNextChoice()
