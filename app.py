from flask import Flask
from flask import request
import re

app = Flask(__name__)

seen_strings = {}

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
        if input in seen_strings:
            seen_strings[input]["Check count"] += 1
        else:
            seen_strings[input] = {}
            seen_strings[input]["Check count"] = 1

        #Get all the alphanumeric characters
        chars = "".join(re.split("[^a-zA-Z]*", input))
        charsSet = set(chars) #Unique characters
        maxCount = 0
        for char in charsSet: #Iterate for each charcter
            if chars.count(char) > maxCount:
                maxCount = chars.count(char)
                maxChar = []
                maxChar.append(char)
            elif chars.count(char) == maxCount: #Append to list if the count is same
                maxChar.append(char)

        if maxCount != 0 :
            seen_strings[input]["Most repeated"] = {
                "Character": maxChar,
                "Count": maxCount
                }

        return {
            "input": input,
            "length": len(input),
            "Most repeated charcter": maxChar,
            "Repeat count": maxCount
        }

@app.route('/stats')
def string_stats():
    return {
        "inputs": seen_strings,
    }
