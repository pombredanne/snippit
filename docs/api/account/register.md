User Registration
=======================
User registration api endpoint

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/account/      |
| Method          | POST               |
| Status Codes    | 201, 400           |
| Permissions     | Allow Any          |
| Content-Type    | application/json   |


#####Payload - raw

| Paramether    | Type     | Validator
| ------------- | ---------|-----------------------|
| Username      | String   | ^[A-Za-z0-9-_]{4,25}$ |
| Password      | String   | min_length=4          |
| E-Mail        | String   | EmailField            |

#####Request ([Other request types](../example.md))

```bash
curl -X POST  -H "Content-Type: application/json"
     -d '{"username":"bahattincinic", "email": "bahattincinic@gmail.com", "password": "123456"}'
     http://snippit.in/api/account/
```

#####Response (Status: 201 CREATED)

```json
{"email": "bahattincinic@gmail.com", "username": "bahattincinic"}
```

#####Errors (Status: 400 Bad Request)

```json
{
 "username": ["User with this Username already exists."],
 "email": ["User with this Email address already exists."]
}
```

```json
{
 "username": ["This field is required."]
}
```

```json
{
 "email": ["Enter a valid email address."]
}
```

**Username Regex:** ^[A-Za-z0-9-_]{4,25}$
```json
{
 "username": ["invalid username"]
}
```
