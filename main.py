import enchant
import itertools
from collections import Counter
from operator import itemgetter
import random

# Empty list placeholder for placing the correct letters in correct position (green)
# This should eventually become the solution to the puzzle
solution = ["","","","",""]

# Empty list placeholder to hold correct letters in wrong position (yellow)
yellows = []

# And here's our trust alphabet. We'll remove letters from this when hints eliminate letters (black / dark grey?)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


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


# Function for moving letters into their proper placeholders
def buildLetterCollections(data):
    
    # Make sure we can access these lists from inside the function
    global solution
    global yellows
    global alphabet

    # Iterate through the status of each letter
    count=0
    for d in data:
        # Move a correct letter into the correct position of the solution
        if d["status"] == 1:
            solution[count] = d["letter"]
        # Make note of the correct letter and it's wrong position
        elif d["status"] == 2:
            yellows.append({
                "letter":d["letter"],
                "not":count
            })
        # Remove the eliminated letter from the alphabet 
        elif d["status"] == 3:
            if d["letter"] in alphabet:
                alphabet.remove(d["letter"]) 
        count+=1


# Function to generate the best solution attempts for the solution
def generateAnswers():

    print("Thinking...")
    
    global alphabet
    global solution
    global yellows

    # Initialize our english dictionary
    d = enchant.Dict("en_US")
    
    # Generate possible letter combos based on letters removed from alphabet
    keywords = [''.join(i) for i in itertools.product(alphabet, repeat = 5)]

    # Placeholder to catch the actual english words from the keywords list
    possible_words = []
    
    # Check the words against the english dictionary to make sure it's valid and save it
    for k in keywords:
        if d.check(k) == True:
            possible_words.append(k)

    # Placeholder for the words that match up with our hints
    matches = []

    for word in possible_words:
        i=0
        while i < 5:
            if solution[i] == word[i]:
                if yellows:
                   for item in yellows:
                       if item["letter"] in word:
                           matches.append(word)
                else:
                    matches.append(word)
            i+=1

    for word in matches:
        i=0
        while i < 5:
            for item in yellows:
                if i == item["not"] and item["letter"] == word[i] and word in matches:
                    matches.remove(word)
                    break
            i+=1

    maybes = []
    list_of_all_values = []               

    for m in matches:
        dupes = matches.count(m)
        if dupes >= 2 and m not in list_of_all_values:
            maybes.append({
                "word":m,
                "score":dupes
            })
            list_of_all_values = [value for elem in maybes for value in elem.values()]

    sorted_maybes = sorted(maybes, key=itemgetter("score"), reverse=True)

    return sorted_maybes


# List of good starting words according to the internets
starters = ["soare","roate","raise"]

# Grab a random start word
first_choice = random.choice(starters)

# Show the selected word that we're starting with.
# User will have to enter this word into the game so we can get our hints.
print("\n*** First try: {} ***\n".format(first_choice.upper()))

# Ask the user to enter the hints returned from our first attempt
word_data = userColorInput(first_choice)

# Start building the solution, populate our placeholders
buildLetterCollections(word_data)

# Generate possible letter combos based on letters removed from alphabet
# TODO: This step needs to be optimized, it's way too slow.
next_choices = generateAnswers()

print("*** Best words for next try: ***")
for item in next_choices:
    print("{} ({})".format(item["word"].upper(),item["score"]))

# Ask the user to enter a word from the suggestions provided
# TODO: Automate this part 
second_try = str(input("Enter your second try: "))

# Ask the user to enter the hints returned from the second attempt
second_data = userColorInput(second_try)

buildLetterCollections(second_data)

next_choices = generateAnswers()

print("*** Best words for next try: ***")
for item in next_choices:
    print("{} ({})".format(item["word"].upper(),item["score"]))
