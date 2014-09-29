Authentication
=======================
Simple token based authentication.

Expiration date (`15 days`) request based automatic Updating

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/auth/login/   |
| Allowed Methods | POST               |
| Status Codes    | 200, 400           |
|  Authenticate   | Allow Any          |


#####Request Paramethers

| Paramether    | Type     | Description         |
| ------------- | ---------|---------------------|
| Username      | String   | snippit.in username |
| Password      | String   | snippit.in password |


#####Request

```bash
curl -X POST  -H "Content-Type: application/json"
     -d '{"username":"<username>","password":"<password>"}'
     http://snippit.in/api/auth/login/
```
    
#####Response (Status: 200 OK)

```json
{
 "expiration_date": "2014-10-13T21:04:31.171Z",
 "token": "d2b443e34d64124dd6d20044c39f6a6c82fd0ee2",
 "user": {
     "username": "bahattincinic",
     "email": "bahattincinic@gmail.com",
     "first_name": "Bahattin",
     "last_name": "Cinic",
     "location": "istanbul",
     "website": "bahattincinic.com",
     "created_at": "16-06-2014 20:51",
     "followers": 1,
     "followings": 1,
     "avatar": "https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd?s=130&d="
  }
}
```
    

#####Errors (Status: 400 Bad Request)
    
**Username or password invalid**
```json
{
 "non_field_errors": ["Unable to login with provided credentials."]
}
```
    
**Username and password empty**
```json
{
 "username": ["This field is required."],
 "password": ["This field is required."]
}
```

**User inactive**
```json
{
 "non_field_errors": ["User account is disabled."]
}
```


Token usage
=========================
Clients should authenticate by passing the token key in the "Authorization" HTTP header, prepended with the string "Token ".  For example:


#####Sample Request

```bash
curl -X GET  -H "Authorization: Token 173f758803eb1fb0ffaf36a782caaa885bd42af2"
     http://snippit.in/api/account/bahattincinic/
```

#####Errors (Status: 401 Unauthorized)

```json
{
 "status_code": 401,
 "detail": "Invalid token"
 }
```

```json
{
 "status_code": 401,
 "detail": "Token has expired"
}
```

Logout
=========================
Log the user out of api

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/auth/logout/  |
| Allowed Methods | POST               |
| Status Codes    | 200, 401           |

#####Request

```bash
curl -X POST  -H "Authorization: Token 173f758803eb1fb0ffaf36a782caaa885bd42af2"
     http://snippit.in/api/auth/logout/
```