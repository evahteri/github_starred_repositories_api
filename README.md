# Github Starred Repositories API

The API retrieves user's starred repositories from Github and displays the number of starred (public) repositories and their info in JSON format.

## Requirements
- Python 3.10.12 or higher

## Instructions

### Configuration
- Create a [new OAuth app in Github developer settings](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app).
- Configure the Homepage URL to ```http://localhost:8000/```
- Configure Authorization callback URL to ```http://localhost:8000/callback```
- Generate a new client secret
- Add your application's Client ID and Client secret to ```src/configuration.py```
- Install required packages with ```pip install -r requirements.txt```

### Running
- Start server in src folder with ```python3 main.py```
- Create a GET request to ```http://localhost:8000/```
- Sign in with Github credentials
- The application will use the token to fetch starred repositories
- Shut down the server from command line with CTRL + C

### Testing
- Run tests in root folder with ```pytest```
- Run ```coverage run --branch -m pytest src && coverage report -m``` to get test coverage

## Using the included Dockerfile
- After adding the Client ID and Client Secret, run ```docker build -t <IMAGE_NAME> .```
- Start the container with ```sudo docker run -d --name <CONTAINER_NAME> -p 8000:8000 <IMAGE_NAME>```
- The API is now operating at ```http://localhost:8000/```
- Shut down the API with ```docker kill <CONTAINER_NAME>```

## Example
TODO

## References/sources used for development

- 1 [Creating async requests to external API's with FastAPI (geeksforgeeks)](https://www.geeksforgeeks.org/making-http-requests-from-a-fastapi-application-to-an-external-api/)
- 2 [Generating random strings (geeksforgeeks)](https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/)
- 3 [JSON convention for empty values](https://stackoverflow.com/questions/9619852/what-is-the-convention-in-json-for-empty-vs-null)