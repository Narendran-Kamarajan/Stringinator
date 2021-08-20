# Stringinator

The application supports a small set of API endpoints that can be used to get information about and manipulate string values. The application also tracks statistics about all the strings that have been sent to the server.

I have chosen Python for this project, as I have already worked with Flask module.

I want to extract only the Alpha-Numeric characters avoiding all the special characters and whitespaces. re module would be used to extract the characters.

I have updated the function to check the count of each alphanumberic character and populate the list of most repeated charcters.

To get the count, I traversed through the keys at multiple levels

After started working on the stats endpoint, mid-way, I realized that I have to change the json structure to capture required details.

Hitting stats endpoint started to throw error, whenever I restarted the application. To handle empty stats, I would return a default response.

Stats function is updated to calculate the lengthiest input received

As I have implemented and validated the required features, I want to enable secure protocol with SSL certificate

To improve application stability, I have included the exception handling. This will ensure not to crash the App with incorrect inputs.
