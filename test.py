import requests
import urllib3
import pytest
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# / endpoint
@pytest.mark.filterwarnings("ignore")
def test_root_endpoint():
    '''
    Check response code and content of / endpoint
    '''
    response = requests.get("https://localhost:8080/", verify=False)
    assert response.status_code == 200
    assert response.text == '<pre>\n    Welcome to the Stringinator 3000 for all of your string manipulation needs.\n\n    GET / - You\'re already here!\n    POST /stringinate - Get all of the info you\'ve ever wanted about a string. Takes JSON of the following form: {"input":"your-string-goes-here"}\n    GET /stats - Get statistics about all strings the server has seen, including the longest and most popular strings.\n    </pre>'

# /stringinate endpoint
@pytest.mark.filterwarnings("ignore")
def test_stringinate_get():
    '''
    Check response code and content of /stringinate endpoint
    Use GET method
    Test the length and Most repeated character in string along with it's count
    '''
    payload = {"input":"your-string-goes-here"}
    response = requests.get("https://localhost:8080/stringinate", params=payload,  verify=False)
    responseDict = json.loads(response.text)
    sortDict = responseDict['Most repeated character']
    sortDict.sort()
    assert response.status_code == 200
    assert sortDict == ['e', 'r']
    assert responseDict['Repeat count'] == 3
    assert responseDict['length'] == 21

@pytest.mark.filterwarnings("ignore")
def test_stringinate_post_0():
    '''
    Check response code and content of /stringinate endpoint
    Use POST method
    Test the length and Most repeated character in string along with it's count
    '''
    payload = '{"input":"your-string-goes-here"}'
    response = requests.post("https://localhost:8080/stringinate", data=payload, headers={"Content-Type": "application/json"}, verify=False)
    responseDict = json.loads(response.text)
    sortDict = responseDict['Most repeated character']
    sortDict.sort()
    assert response.status_code == 200
    assert sortDict == ['e', 'r']
    assert responseDict['Repeat count'] == 3
    assert responseDict['length'] == 21

@pytest.mark.filterwarnings("ignore")
def test_stringinate_post_1():
    '''
    Check response code and content of /stringinate endpoint
    Use POST method
    Test the length and Most repeated character in string along with it's count

    '''
    payload = '{"input":"Comcast"}'
    response = requests.post("https://localhost:8080/stringinate", data=payload, headers={"Content-Type": "application/json"}, verify=False)
    responseDict = json.loads(response.text)
    sortDict = responseDict['Most repeated character']
    sortDict.sort()
    assert response.status_code == 200
    assert sortDict == ['C', 'a', 'c', 'm', 'o', 's', 't']
    assert responseDict['Repeat count'] == 1
    assert responseDict['length'] == 7

@pytest.mark.filterwarnings("ignore")
def test_stringinate_post_special():
    '''
    Check response code and content of /stringinate endpoint
    Use POST method
    Test the length and Most repeated character in string along with it's count
    Input - "!@#$%^&*+" (Only special char)
    '''
    payload = '{"input":"!@#$%^&*+"}'
    response = requests.post("https://localhost:8080/stringinate", data=payload, headers={"Content-Type": "application/json"}, verify=False)
    responseDict = json.loads(response.text)
    assert response.status_code == 200
    assert responseDict['Most repeated character'] == "No alphanumeric character available"
    assert responseDict['Repeat count'] == "NA"
    assert responseDict['length'] == 9

@pytest.mark.filterwarnings("ignore")
def test_stringinate_post__null():
    '''
    Check response code and content of /stringinate endpoint
    Use POST method
    Null input
    '''
    payload = '{"input":""}'
    response = requests.post("https://localhost:8080/stringinate", data=payload, headers={"Content-Type": "application/json"}, verify=False)
    responseDict = json.loads(response.text)
    assert response.status_code == 200
    assert responseDict['Error'] == "No input provided"

@pytest.mark.filterwarnings("ignore")
def test_stringinate_post_non_str_0():
    '''
    Check response code and content of /stringinate endpoint
    Use POST method
    Non-string input
    '''
    payload = '{"input":69}'
    response = requests.post("https://localhost:8080/stringinate", data=payload, headers={"Content-Type": "application/json"}, verify=False)
    responseDict = json.loads(response.text)
    assert response.status_code == 200
    assert responseDict['Error'] == "Stringinator accepts only string"

@pytest.mark.filterwarnings("ignore")
def test_stringinate_post_non_str_1():
    '''
    Check response code and content of /stringinate endpoint
    Use POST method
    Non-string input
    '''
    payload = '{"input":[6,9]}'
    response = requests.post("https://localhost:8080/stringinate", data=payload, headers={"Content-Type": "application/json"}, verify=False)
    responseDict = json.loads(response.text)
    assert response.status_code == 200
    assert responseDict['Error'] == "Stringinator accepts only string"

# /stats endpoint
@pytest.mark.filterwarnings("ignore")
def test_root_endpoint():
    '''
    Check response code and keys of /stats endpoint
    '''
    response = requests.get("https://localhost:8080/stats", verify=False)
    responseDict = json.loads(response.text)
    assert response.status_code == 200
    assert "data" in responseDict['inputs'].keys()
    assert "report" in responseDict['inputs'].keys()
