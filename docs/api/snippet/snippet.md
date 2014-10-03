List Snippets
====================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/                                        |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | name, created_at    |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/snippets/
```

#####Response (Status: 200 OK)

```json
{
 "count": 2,
 "next": null,
 "previous": null,
 "results": [
   {
     "url": "http://snippit.in/api/snippets/python-js-test/",
     "comments_url": "http://snippit.in/api/snippets/python-js-test/comments/",
     "star_url": "http://snippit.in/api/snippets/python-js-test/star/",
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
       "followers": 0,
       "followings": 1,
       "avatar": "<Gravatar url>"
      },
      "created_at": "17-06-2014 21:26",
      "stars": 0,
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
  ]
}
```

Get a single snippet
=====================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`                        |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/snippets/python-js-test/
```

#####Response (Status: 200 OK)

```json
 {
     "url": "http://snippit.in/api/snippets/python-js-test/",
     "comments_url": "http://snippit.in/api/snippets/python-js-test/comments/",
     "star_url": "http://snippit.in/api/snippets/python-js-test/star/",
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
       "followers": 0,
       "followings": 1,
       "avatar": "<Gravatar url>"
      },
      "created_at": "17-06-2014 21:26",
      "stars": 0,
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

Create a Snippet
=================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/                                        |
| Method          | POST                                                  |
| Status Codes    | 201, 400                                              |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Payload - raw

| Paramether        | Type     | Required |
| ----------------- | -------- | -------- |
| name              | String   | Yes      |
| pages             | List     | Yes      |
| tags              | List     | Yes      |
| public            | Boolean  | Yes      |

#####Request ([Other request types](../example.md))

```bash
curl -X POST -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
    -d '{"tags": ["java"], "public": true, "name": "Python JS Test", "pages": [{"content": "Hello World", "language": "javascript"}]}'
     http://snippit.in/api/snippets/
```

#####Response (Status: 200 OK)

```json
 {
     "url": "http://snippit.in/api/snippets/python-js-test/",
     "comments_url": "http://snippit.in/api/snippets/python-js-test/comments/",
     "star_url": "http://snippit.in/api/snippets/python-js-test/star/",
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
       "followers": 0,
       "followings": 1,
       "avatar": "<Gravatar url>"
      },
      "created_at": "17-06-2014 21:26",
      "stars": 0,
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

Edit a Snippet
====================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/                       |
| Method          | PUT                                                   |
| Status Codes    | 200                                                   |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Payload - raw

| Paramether        | Type     | Required |
| ----------------- | -------- | -------- |
| name              | String   | Yes      |
| pages             | List     | Yes      |
| tags              | List     | Yes      |
| public            | Boolean  | Yes      |


#####Request ([Other request types](../example.md))

```bash
curl -X PUT -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
    -d '{"tags": ["java"], "public": false, "name": "Python JS Test", "pages": [{"content": "Hello World", "language": "javascript"}]}'
     http://snippit.in/api/snippets/python-js-test/
```

#####Response (Status: 200 OK)

```json
 {
     "url": "http://snippit.in/api/snippets/python-js-test/",
     "comments_url": "http://snippit.in/api/snippets/python-js-test/comments/",
     "star_url": "http://snippit.in/api/snippets/python-js-test/star/",
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
       "followers": 0,
       "followings": 1,
       "avatar": "<Gravatar url>"
      },
      "created_at": "17-06-2014 21:26",
      "stars": 0,
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

Delete a snippet
====================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/snippets/`<snippet-slug>`/                       |
| Method          | DELETE                                                |
| Status Codes    | 204                                                   |
| Permission      | Authenticated                                         |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X DELETE -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://snippit.in/api/snippets/python-js-test/
```


List of user snippets
================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`<username>`/snippets/                   |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | name, created_at    |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/account/barisguler/snippets/
```

#####Response (Status: 200 OK)

```json
{
 "count": 2,
 "next": null,
 "previous": null,
 "results": [
   {
     "url": "http://snippit.in/api/snippets/python-js-test/",
     "comments_url": "http://snippit.in/api/snippets/python-js-test/comments/",
     "star_url": "http://snippit.in/api/snippets/python-js-test/star/",
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
       "followers": 0,
       "followings": 1,
       "avatar": "<Gravatar url>"
      },
      "created_at": "17-06-2014 21:26",
      "stars": 0,
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
  ]
}
```