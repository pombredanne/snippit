Get a single user
=======================

| Key             | Value                      |
| ----------------|----------------------------|
| URL             | /api/account/`<username>`/ |
| Method          | GET                        |
| Status Codes    | 200, 400                   |
| Permission      | Allow Any                  |


#####Request

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/account/bahattincinic/
```

#####Response (Status: 200 OK)

```json
{
 "username": "bahattincinic",
 "email": "bahattincinic@gmail.com",
 "first_name": null,
 "last_name": null,
 "location": null,
 "website": null,
 "created_at": "16-06-2014 20:51",
 "followers": 1,
 "followings": 1,
 "avatar": "https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd?s=130&d="
}
```

Update the authenticated user
============================

| Key             | Value                      |
| ----------------|----------------------------|
| URL             | /api/account/`<username>`/ |
| Method          | PUT                        |
| Status Codes    | 200, 400                   |
| Permission      | Authenticated              |


#####Payload - raw

| Paramether    | Type     | Required            |
| ------------- | ---------|---------------------|
| username      | String   | Yes                 |
| email         | String   | Yes                 |
| first_name    | String   | No                  |
| last_name     | String   | No                  |
| location      | String   | No                  |
| website       | String   | No                  |

#####Request

```bash
curl -X PUT  -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     -d '{"username":"bahattincinic","email":"bahattincinic@gmail.com", "first_name": "bahattincinic"}'
     http://snippit.in/api/account/bahattincinic/
```

#####Response (Status: 200 OK)

```json
{
 "username": "bahattincinic"
 "email": "bahattincinic@gmail.com",
 "first_name": "bahattincinic",
 "last_name": null,
 "location": null,
 "website": null,
 "created_at": "16-06-2014 20:51",
 "followers": 1,
 "followings": 1,
 "avatar": "https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd?s=130&d="
 }
```

#####Errors (Status: 400 Bad Request)

```json
{
 "username": ["This field is required."],
 "email": ["This field is required."]
}
```

```json
{
 "username": ["User with this Username already exists."],
 "email": ["User with this Email address already exists."]
}
```
