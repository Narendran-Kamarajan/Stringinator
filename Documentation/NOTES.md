# Stringinator

The application supports a small set of API endpoints that can be used to get information about and manipulate string values. The application also tracks statistics about all the strings that have been sent to the server.

I have chosen Python for this project, as I have already worked with Flask module.

## Documentation

###/
The root of the server displays info about the other endpoints. This is the only endpoint that does not return JSON.

###/stringinate
Get all the info you've ever wanted about a string. Accepts GET and POST requests. For POSTs the endpoint takes JSON of the following form:
    {"input":"your-string-goes-here"}

For GETs an input string is specified as ?input=<your-input>.

###/stats
Get statistics about all strings the server has seen, including the number of times each input has been received along with the longest and most popular strings etc.


##Improvements
For the /stringinate endpoint, for a given input string we need to find the character that occurs most frequently and add that character, along with its number of occurrences to the API response JSON. You decide how to represent this in the JSON response. Ignore white space and punctuation.
