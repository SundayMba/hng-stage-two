## HNG STAGE TWO ORGANISATION MANAGEMENT API
1. [POST] /auth/register

Registers a users and creates a default organisation Register

request body
``` 
{
"firstName": "string",
"lastName": "string",
"email": "string",
"password": "string",
"phone": "string",
}
```

### USAGE
1. install a virtual envirement
```
python3 -m venv venv
```

2. activate the virtual environment
```
source ./venv/bin/activate
```

3. install neccessary packages
```
pip install -r requirements.txt
```

4. environment variables
```
set the neccesary environment variables as defined in the config file
```
5. spin up the server
```
flask run
```

6. login endpoints

[POST] /auth/login : logs in a user. When you log in, you can select an organisation to interact with

* Login request body:
````
{
	"email": "string",
	"password": "string",
}
```