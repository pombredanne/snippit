list of snippet subscribers
==============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/subscribers/           |
| Method          | GET                                                   |
| Status Codes    | 200, 404                                              |
| Permission      | Allow Any                                             |
| Content-Type    | application/json                                      |


#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/snippets/python-dict/subscribers/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
    {
     "username": "bahattincinic",
     "email": "bahattincinic@gmail.com",
     "first_name": "bahattincinic",
     "last_name": null,
     "location": null,
     "website": null,
     "created_at": "16-06-2014 20:51",
     "followers": 1,
     "followings": 1,
     "avatar": "<Gravatar URL>"
    }
 ]
}
```

Subscribe to snippet
=======================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/subscribers/           |
| Method          | POST                                                  |
| Status Codes    | 201,404                                               |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X POST -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/snippets/python-dict/subscribers/
```

#####Response (Status: 201 CREATED)

```json
{
 "following": {
   "username": "barisguler",
   "email": "barisguler@gmail.com",
   "first_name": null,
   "last_name": null,
   "location": null,
   "website": null,
   "created_at": "17-06-2014 21:18",
   "followers": 0,
   "followings": 1,
   "avatar": "<Gravatar Url>"
  },
  "follower": {
    "username": "bahattincinic",
    "email": "bahattincinic@gmail.com",
    "first_name": "bahattincinic",
    "last_name": null,
    "location": null,
    "website": null,
    "created_at": "16-06-2014 20:51",
    "followers": 1,
    "followings": 0,
    "avatar": "<Gravatar Url>"
  }
}
```

#####Errors (Status: 409 CONFLICT)

```json
{
 "status_code": 409,
 "detail": "User already exists."
}
```

UnSubscribe to snippet
=======================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/subscribers/           |
| Method          | POST                                                  |
| Status Codes    | 204, 404, 403                                         |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X DELETE -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/snippets/python-dict/subscribers/
```

#####Response (Status: 204 NO CONTENT)

  `<Response body is empty>`
  
#####Errors (Status: 409 CONFLICT)

```json
{
 "status_code": 404,
 "detail": "User does not between subscribers"
}
```