List Snippet Stars
==================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/star/users/            |
| Allowed Methods | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| Ordering Fields | username, first_name, last_name (?ordering=-username) |

#####Request

```bash
curl -X GET -H "Content-Type: application/json"
     http://snippit.in/api/snippets/django-view-render/star/users/
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

List User Starred Snippets
===============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`username`/stars/                        |
| Allowed Methods | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| Ordering Fields | stars, comments, name, created_at (?ordering=-name)   |

#####Request

```bash
curl -X GET -H "Content-Type: application/json"
     http://snippit.in/api/account/bahattincinic/stars/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
  {
   "name": "Python JS Test",
   "slug": "python-js-test",
   "owner": {
     "username": "barisguler",
     "email": "barisguler@gmail.com",
     "first_name": null,
     "last_name": null,
     "location": null,
     "website": null,
     "created_at": "17-06-2014 21:18",
     "followers": 1,
     "followings": 1,
     "avatar": "<Gravatar URL>"
    },
    "created_at": "17-06-2014 21:26",
    "stars": 1,
    "comments": 1,
    "pages": 1,
    "url": "http://snippit.in/api/snippets/python-js-test/",
    "comments_url": "http://snippit.in/api/snippets/django-view-render/comments/",
    "star_url": "http://snippit.in/api/snippets/django-view-render/star/"
   }
  ]
 }
```

Star a Snippet
=======================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/star/                  |
| Allowed Methods | POST, DELETE, GET                                     |
| Status Codes    | 201, 403,                                             |
| Permission      | Authenticated                                         |

#####Request

```bash
curl -X POST -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/snippets/django-view-render/star/
```    
     
#####Response (Status: 201 CREATED)

```json
{
 "url": "http://localhost:8000/api/snippets/django-view-render/",
 "comments_url": "http://localhost:8000/api/snippets/python-js-test/comments/",
 "star_url": "http://localhost:8000/api/snippets/python-js-test/star/",
 "name": "Python JS Test",
 "slug": "python-js-test",
 "owner": {
   "username": "barisguler",
   "email": "barisguler@gmail.com",
   "first_name": null,
   "last_name": null,
   "location": null,
   "website": null,
   "created_at": "17-06-2014 21:18",
   "followers": 1,
   "followings": 1,
   "avatar": "<Gravatar URL>"
  },
  "created_at": "17-06-2014 21:26",
  "stars": 1,
  "comments": 1,
  "tags": [
    {
     "name": "python",
     "slug": "python",
     "snippets": 1
    }
   ],
   "pages": [
     {
      "content": "Hello World",
      "language": {
        "name": "Python",
        "slug": "python",
        "pages": 1
       }
     }
    ],
    "public": true,
    "subscribers": []
 }
```

#####Errors (Status: 403)

Already star for starred snippet, unstar for not starred snippet

```json
{
 "status_code": 403,
 "detail": "You do not have permission to perform this action."
}
```

Unstar a Snippet
============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/star/                  |
| Allowed Methods | DELETE, POST, GET                                     |
| Status Codes    | 201, 403,                                             |
| Permission      | Authenticated                                         |

#####Request

```bash
curl -X DELETE -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/snippets/django-view-render/star/
```

#####Response (Status: 204 NO CONTENT)

    <Response body is empty>


Check if a snippet is starred
==============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/star/                  |
| Allowed Methods | POST, DELETE, GET                                     |
| Status Codes    | 201, 403,                                             |
| Permission      | Authenticated                                         |

#####Request

```bash
curl -X GET -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/snippets/django-view-render/star/
```

#####Response
**Response if snippet is starred:** 204 - NO CONTENT

**Response if snippet is not starred:** 200 - OK
