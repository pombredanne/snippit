List followers of a user
===========================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`<username>`/followers/                  |
| Method          | GET                                                   |
| Status Codes    | 200, 201, 204                                         |
| Permission      | Allow Any                                             |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json"
     http://snippit.in/api/account/bahattincinic/followers/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
   {
    "username": "barisguler",
    "email": "barisguler@gmail.com",
    "first_name": null,
    "last_name": null,
    "location": null,
    "website": null,
    "created_at": "17-06-2014 21:18",
    "followers": 1,
    "followings": 1,
    "avatar": "<Gravatar Url>"
   }
  ]
}
```

List users followed by another user
===========================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`<username>`/followings/                 |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json"
     http://snippit.in/api/account/bahattincinic/followings/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
   {
    "username": "barisguler",
    "email": "barisguler@gmail.com",
    "first_name": null,
    "last_name": null,
    "location": null,
    "website": null,
    "created_at": "17-06-2014 21:18",
    "followers": 1,
    "followings": 1,
    "avatar": "<Gravatar Url>"
   }
  ]
}
```

Follow a user
==============================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`<username>`/followers/                  |
| Method          | POST                                                  |
| Status Codes    | 201                                                   |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X POST -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/account/bahattincinic/followers/
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

#####Errors (Status: 403)

Already Follow a user, himself to follow
```json
{
 "status_code": 403,
 "detail": "You do not have permission to perform this action."
}
```

UnFollow a user
==============================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`<username>`/followers/                  |
| Method          | DELETE                                                |
| Status Codes    | 204                                                   |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X DELETE -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/account/bahattincinic/followers/
```

#####Response (Status: 204 NO CONTENT)

  `<Response body is empty>`

#####Errors (Status: 403)

Already UnFollow a user,  himself to unfollow
```json
{
 "status_code": 403,
 "detail": "You do not have permission to perform this action."
}
```