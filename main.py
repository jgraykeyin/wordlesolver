import enchant
import random
import itertools

# Setup an alphabet for each letter slot
# The returned hints will help clear out unused letters
wordle = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
]

# List of good starting words to choose from
starters = [
    "adieu","tears","lares","alert","alone","atone","audio","blind",
    "canoe","cough","media","notes","orate","radio","raise","resin",
    "senor","steam","stone","tares"
    ]


# Container for catching all the 'yellow' hints, this will be used for filtering out words
yellows = []


# Function for getting the returned hint information from user
def userColorInput(word):
    word_data = []
    count=0
    for i in word:
        # Ask the user what hint was returned for each letter
        print("1) Correct [green]")
        print("2) Wrong place [yellow]")
        print("3) Not in word [black]")

        while True:
            count+=1
            status = int(input("Status of letter #{} -> {}: ".format(count,i.upper())))

            # Input validation so it'll make sure 1,2 or 3 was entered
            if status >= 1 and status <= 3:
                word_data.append({
                    "letter":i.lower(),
                    "status":status
                })
                break
            else:
                print("Enter 1, 2 or 3")

    return word_data


# Function for processing the hints returned
def processAttempt(data):
    global wordle
    global yellows

    count=0
    for d in data:
        if d["status"] == 1:
            # Green
            # Replace the entire alphabet with the correct letter for this slot
            wordle[count] = d["letter"]
        elif d["status"] == 2:
            # Yellow
            # Remove this letter from the current slot's alphabet
            if wordle[count]:
                wordle[count].remove(d["letter"])
                # Also add it to the yellow tracker
                if d["letter"] not in yellows:
                    yellows.append(d["letter"])
        elif d["status"] == 3:
            # Remove this letter from every slot's alphabet
            i=0
            while i < 5:
                if type(wordle[i]) == list:
                    wordle[i].remove(d["letter"])
                i+=1
        count+=1


# Function for generating list of possible words for the next choice
def generateNextChoice():
    global wordle
    global yellows

    # Initialize the dictionary
    d = enchant.Dict("en_US")

    # Placeholders for all generated words and a solution
    solution = ["","","","",""]
    possible_words = []

    # This function could take a few minutes, patience!
    print("Thinking...")

    # Place all the green correct letters into the solution slots
    count=0
    for w in wordle:
        if len(w) == 1:
            solution[count] = w
        count+=1

    # Get all possible combinations of letters remaining from each slot's alphabet
    combos = list(itertools.product(*wordle))

    # Run through each combination and check to see if it's a word
    for combo in combos:
        word = ""
        x=0
        while x < 5:
            word += combo[x]
            x+=1
        if d.check(word) == True:
            # If it's an actual word, let's add it to the placeholder
            possible_words.append(word)

    # Check all the possible words and filter out any that don't contain yellow letters
    filtered_words = []
    if yellows:
        for word in possible_words:
            check = all(yellow in word for yellow in yellows)
            if check == True:
                # If the word contains a yellow, move it to the new filtered word list
                filtered_words.append(word)
            
    return filtered_words
        

# Start the main program loop and repeat for each try
user_try=1
while user_try < 7:

    if user_try > 1:
        try_word = input("Select word from list: ")
    else:
        # Grab a random start word
        try_word = random.choice(starters)

    # Show the selected word that we're starting with.
    # User will have to enter this word into the game so we can get our hints.
    print("\n*** Try #{}: {} ***\n".format(user_try,try_word.upper()))

    # Ask the user for the returned hints
    word_data = userColorInput(try_word)

    # Start processing the attempt
    processAttempt(word_data)

    # Generate a list of possible choices for next try
    next_choices = generateNextChoice()

    if len(next_choices) == 1:
        print("Solution: {}".format(next_choices))
        break
    else:
        print("Possible words for next try: \n{}".format(next_choices))

    
    user_try+=1
