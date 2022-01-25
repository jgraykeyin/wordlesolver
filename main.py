import enchant
import itertools
from collections import Counter
from operator import itemgetter

d = enchant.Dict("en_US")
print(d.check("Hello"))

# First word attempt by the user
while True:
    word1 = str(input("First word attempt:"))

    if len(word1) == 5:
        break
    else:
        print("Please enter a 5 letter word")

# Init empty list to hold letter statuses
word1_data = []

# Get the returned status of each letter
count=1
for i in word1:
    print("1) Correct [green]")
    print("2) Wrong place [yellow]")
    print("3) Not in word [black]")

    while True:
        count+=1
        status = int(input("Status of letter #{} -> {}: ".format(count,i.upper())))

        if status >= 1 and status <= 3:
            word1_data.append({
                "letter":i.lower(),
                "status":status
            })
            break
        else:
            print("Enter 1,2 or 3")


# Setup a placeholder so we can move correct letters into it
holder = [".",".",".",".","."]

# Hold letters that are in the word, but in the wrong place
wrong_place = []

# Alphabet that we'll use to remove letters from as they get eliminated
alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


# Move any correct letters into the placeholder
count=0
for data in word1_data:
    if data["status"] == 1:
        holder[count] = data["letter"]
    elif data["status"] == 2:
        wrong_place.append(data["letter"])
    elif data["status"] == 3:
        # Remove letter from the alphabet if it's been eliminated
        if data["letter"] in alphabets:
            alphabets.remove(data["letter"])
    count+=1
    
print(holder)
print(alphabets)

# Generate possible letter combos based on letters removed from alphabet
keywords = [''.join(i) for i in itertools.product(alphabets, repeat = 5)]

possible_words = []
# Check to see if letter combo is a word
for k in keywords:
    if d.check(k) == True:
        possible_words.append(k)


matches = []
# Start matching correct characters with the possible words
for p in possible_words:

    if holder[0] != "." and holder[1] != "." and holder[2] != "." and holder[3] != "." and holder[4] != ".":
        i=0
        while i < 5:
            if holder[i] == p[i]:
                if wrong_place:
                    for w in wrong_place:
                        if w in p:
                            matches.append(p)
                else:
                    matches.append(p)
            i+=1
    else:
        if wrong_place:
            for w in wrong_place:
                if w in p:
                    matches.append(p)
        
# Save the number of duplicates to find the most probable answer
maybes = []
list_of_all_values = []

for m in matches:
    dupes = matches.count(m)
    if dupes >= 2 and m not in list_of_all_values:
        maybes.append({
            "word":m,
            "score":dupes
        })
        # Update list of duplicates for the maybes
        list_of_all_values = [value for elem in maybes for value in elem.values()]

sorted_maybes = sorted(maybes, key=itemgetter("score"), reverse=True)

top=0
for s in sorted_maybes:
    if top == 0:
        top = s["score"]

    if top==5:
        if s["score"] < 5:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==4:
        if s["score"] < 4:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==3:
        if s["score"] < 3:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==2:
        if s["score"] < 2:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==1:
        if s["score"] < 1:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))


# Second word attempt by the user
while True:
    word2 = str(input("Second word attempt:"))

    if len(word2) == 5:
        break
    else:
        print("Please enter a 5 letter word")

word2_data = []

# Get the returned status of each letter
count=1
for i in word2:
    print("1) Correct [green]")
    print("2) Wrong place [yellow]")
    print("3) Not in word [black]")

    while True:
        count+=1
        status = int(input("Status of letter #{} -> {}: ".format(count,i.upper())))

        if status >= 1 and status <= 3:
            word2_data.append({
                "letter":i.lower(),
                "status":status
            })
            break
        else:
            print("Enter 1,2 or 3")


# Move any correct letters into the placeholder
count=0
for data in word2_data:
    if data["status"] == 1:
        holder[count] = data["letter"]
    elif data["status"] == 2:
        wrong_place.append(data["letter"])
    elif data["status"] == 3:
        # Remove letter from the alphabet if it's been eliminated
        if data["letter"] in alphabets:
            alphabets.remove(data["letter"])
    count+=1
    
print(holder)
print(alphabets)

# Generate possible letter combos based on letters removed from alphabet
keywords = [''.join(i) for i in itertools.product(alphabets, repeat = 5)]

possible_words = []
# Check to see if letter combo is a word
for k in keywords:
    if d.check(k) == True:
        possible_words.append(k)

matches = []
# Start matching correct characters with the possible words
for p in possible_words:

    if holder[0] != "." and holder[1] != "." and holder[2] != "." and holder[3] != "." and holder[4] != ".":
        i=0
        while i < 5:
            if holder[i] == p[i]:
                if wrong_place:
                    for w in wrong_place:
                        if w in p:
                            matches.append(p)
                else:
                    matches.append(p)
            i+=1
    else:
        if wrong_place:
            for w in wrong_place:
                if w in p:
                    matches.append(p)

# Save the number of duplicates to find the most probable answer
maybes = []
list_of_all_values = []

for m in matches:
    dupes = matches.count(m)
    if dupes >= 2 and m not in list_of_all_values:
        maybes.append({
            "word":m,
            "score":dupes
        })
        # Update list of duplicates for the maybes
        list_of_all_values = [value for elem in maybes for value in elem.values()]

sorted_maybes = sorted(maybes, key=itemgetter("score"), reverse=True)

top=0
for s in sorted_maybes:
    if top == 0:
        top = s["score"]

    if top==5:
        if s["score"] < 5:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==4:
        if s["score"] < 4:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==3:
        if s["score"] < 3:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==2:
        if s["score"] < 2:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
    elif top==1:
        if s["score"] < 1:
            continue
        else:
            print("{} [{}]".format(s["word"].upper(), s["score"]))
