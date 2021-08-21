from flask import Flask
from flask import request
from os.path import exists as file_exists
import re
import pickle


app = Flask(__name__)

if file_exists("Backup/seen_strings.pickle"):
    with open("Backup/seen_strings.pickle", "rb") as pickledFile :
        seen_strings=pickle.load(pickledFile)
else:
    print("Backup/seen_strings.pickle file is not available")
    seen_strings = {"data":{},"report":{}}

def pickleData(store_strings):
    with open("Backup/seen_strings.pickle", "wb") as outFile :
        pickle.dump(store_strings,outFile)

@app.route('/')
def root():
    return '''
    <pre>
    Welcome to the Stringinator 3000 for all of your string manipulation needs.

    GET / - You're already here!
    POST /stringinate - Get all of the info you've ever wanted about a string. Takes JSON of the following form: {"input":"your-string-goes-here"}
    GET /stats - Get statistics about all strings the server has seen, including the longest and most popular strings.
    </pre>
    '''.strip()

@app.route('/stringinate', methods=['GET','POST'])
def stringinate():
    input = ''
    if request.method == 'POST':
        input = request.json['input']
    else:
        input = request.args.get('input', '')

    if input == "" :
        raise ValueError("No input provided")
    elif type(input) != str:
        raise TypeError("Stringinator accepts only string")
    else:
        if input in seen_strings["data"]:
            seen_strings["data"][input]["Check count"] += 1
        else:
            seen_strings["data"][input] = {}
            seen_strings["data"][input]["Check count"] = 1

        #Get all the alphanumeric characters
        chars = "".join(re.split("[^a-zA-Z]*", input))
        charsSet = set(chars) #Unique characters
        maxCount = 0

        for char in charsSet: #Iterate for each charcter
            if chars.count(char) > maxCount:
                maxCount = chars.count(char)
                maxChar = [char]
            elif chars.count(char) == maxCount: #Append to list if the count is same
                maxChar.append(char)

        if maxCount != 0 :
            seen_strings["data"][input]["Most repeated"] = {
                "Character": maxChar,
                "Count": maxCount
                }
        else: #If there is only special characters in the input
            seen_strings["data"][input]["Most repeated"] = {
                "Character": "Null",
                "Count": 0
                }
            pickleData(seen_strings)
            return {
                "input": input,
                "length": len(input),
                "Most repeated character": "No alphanumeric character available",
                "Repeat count": "NA"
            }

        pickleData(seen_strings)
        return {
            "input": input,
            "length": len(input),
            "Most repeated charcter": maxChar,
            "Repeat count": maxCount
        }

@app.route('/stats')
def string_stats():
    mostCount = 0
    maxLength = 0
    mostString = []
    lengthyString = []
    for strData in seen_strings["data"]: #Loop through all inputs
        #Longest string
        if len(strData) > maxLength :
            maxLength = len(strData)
            lengthyString = [strData]
        elif len(strData) == maxLength :
            lengthyString.append(strData)
        #Repeated string
        if seen_strings["data"][strData]["Check count"] > mostCount :
            mostCount = seen_strings["data"][strData]["Check count"]
            mostString = [strData]
        elif seen_strings["data"][strData]["Check count"] == mostCount :
            mostString.append(strData)

    if mostString: #Update only if not empty
        seen_strings["report"]["most_popular"] = mostString
        seen_strings["report"]["most_popular_count"] = mostCount

    if lengthyString: #Update only if not empty
        seen_strings["report"]["longest_input_received"] = lengthyString
        seen_strings["report"]["longest_input_received_length"] = maxLength

    pickleData(seen_strings)
    return {
        "inputs": seen_strings
    }

@app.errorhandler(Exception)
def basic_error(errArg):
    return {"Error": str(errArg)}
