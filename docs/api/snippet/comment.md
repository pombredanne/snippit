List comments on a snippet
=====================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/comments/              |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | created_at |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/snippets/python-dict/comments/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
   {
    "author": {
     "username": "bahattincinic",
     "email": "bahattincinic@gmail.com",
     "first_name": "bahattincinic",
     "last_name": null,
     "location": null,
     "website": null,
     "created_at": "16-06-2014 20:51",
     "followers": 1,
     "followings": 0,
     "avatar": "<Gravatar URL>"
  },
  "snippet": {
    "name": "Python Dict",
    "slug": "python-dict",
    "owner": {
      "username": "bahattincinic",
      "email": "bahattincinic@gmail.com",
      "first_name": "bahattincinic",
      "last_name": null,
      "location": null,
      "website": null,
      "created_at": "16-06-2014 20:51",
      "followers": 1,
      "followings": 0,
      "avatar": "<Gravatar URL>"
    },
    "created_at": "17-06-2014 21:26",
    "stars": 0,
    "comments": 1,
    "pages": 1,
    "url": "http://snippit.in/api/snippets/python-dict/",
    "comments_url": "http://snippit.in/api/snippets/python-dict/comments/",
    "star_url": "http://snippit.in/api/snippets/python-dict/star/"
  },
  "comment": "test",
  "created_at": "17-06-2014 21:42"
  }
 ]
}
```

Create a comment
=================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/comments/              |
| Method          | POST                                                  |
| Status Codes    | 201                                                   |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Payload - raw

| Paramether        | Type     | Description                      | Required |
| ----------------- | -------- |--------------------------------- | -------- |
| comment           | String   | The comment text.                | Yes      |

#####Request ([Other request types](../example.md))

```bash
curl -X POST -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"    
    -d '{"comment":"test"}'
     http://snippit.in/api/snippets/python-dict/comments/
```

#####Response (Status: 201 CREATED)

```json
{
 "author": {
     "username": "bahattincinic",
     "email": "bahattincinic@gmail.com",
     "first_name": "bahattincinic",
     "last_name": null,
     "location": null,
     "website": null,
     "created_at": "16-06-2014 20:51",
     "followers": 1,
     "followings": 0,
     "avatar": "<Gravatar URL>"
  },
  "snippet": {
    "name": "Python Dict",
    "slug": "python-dict",
    "owner": {
      "username": "bahattincinic",
      "email": "bahattincinic@gmail.com",
      "first_name": "bahattincinic",
      "last_name": null,
      "location": null,
      "website": null,
      "created_at": "16-06-2014 20:51",
      "followers": 1,
      "followings": 0,
      "avatar": "<Gravatar URL>"
    },
    "created_at": "17-06-2014 21:26",
    "stars": 0,
    "comments": 1,
    "pages": 1,
    "url": "http://snippit.in/api/snippets/python-dict/",
    "comments_url": "http://snippit.in/api/snippets/python-dict/comments/",
    "star_url": "http://snippit.in/api/snippets/python-dict/star/"
  },
  "comment": "test",
  "created_at": "17-06-2014 21:42"
  }
```
