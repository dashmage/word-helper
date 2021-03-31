# Program to find the definition of a word and save it in a notepad file

import requests, json, sys
import tkinter as tk
import tkinter.messagebox


def getClipboardText():
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    return root.clipboard_get()

def popUpWindow(title, message):
    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title, message)

copied_string = getClipboardText()

# check if only one word is being copied
if len(copied_string.split()) == 1:
    search_word = copied_string.strip()
else:
    # gives error pop up
    popUpWindow('Copy Error', 'Please select and copy a single word!')
    sys.exit(0)

# https://github.com/meetDeveloper/googleDictionaryAPI for dictionary API

url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + search_word

response = requests.get(url)
# response.text -> gives string output

# gives you a list output in json format
json_object = response.json()
# pretty prints the json object
# print(json.dumps(json_object, indent = 2))

# in case the word isn't present in dictionary
if 'title' in json_object:
    popUpWindow("Definition Error", "That word doesn't seem to exist!")
    sys.exit(0)

num_of_def = len(json_object[0]["meanings"][0]["definitions"])

index = 0
definitions = []
examples = []

# populating definitions, examples lists with the values from the json object
while index < num_of_def:
    definitions.append(json_object[0]["meanings"][0]["definitions"][index]["definition"])
    try:
        examples.append(json_object[0]["meanings"][0]["definitions"][index]["example"])
    except KeyError:
        examples.append("")
    index += 1


# need to loop through the defintion, example lists and print all values to txt file

# underline under search word
write_to_file = search_word + "\n" + "-"*len(search_word) + "\n"
# writing defintions and examples to file string
for i in range(len(definitions)):
    write_to_file += "{count}. {definition_i}\n".format(count = i+1, definition_i = definitions[i])
    if examples[i] != "":
        write_to_file += "Eg: " + examples[i] + "\n\n"

write_to_file += "\n\n"

f = open("new_words.txt", "a")
f.write(write_to_file)
f.close()
popUpWindow('Success ✔', 'Word definition has been added!')

