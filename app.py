from flask import Flask
from flask import request
import re

app = Flask(__name__)

seen_strings = {"data":{},"report":{}}

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
        return {
            "input":""
            }
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
            return {
                "input": input,
                "length": len(input),
                "Most repeated character": "No alphanumeric character available",
                "Repeat count": "NA"
            }

        return {
            "input": input,
            "length": len(input),
            "Most repeated charcter": maxChar,
            "Repeat count": maxCount
        }

@app.route('/stats')
def string_stats():
    mostCount = 0
    for strData in seen_strings["data"]:
        if seen_strings["data"][strData]["Check count"] > mostCount :
            mostCount = seen_strings["data"][strData]["Check count"]
            mostString = [strData]
        elif seen_strings["data"][strData]["Check count"] == mostCount :
            mostString.append(strData)

    if seen_strings:
        seen_strings["report"]["most_popular"] = mostString
        seen_strings["report"]["most_popular_count"] = mostCount

    return {
        "inputs": seen_strings
    }
