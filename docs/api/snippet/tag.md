List Of Tags
==============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/tags/                                            |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | name, snippets (?ordering=-name)                      |
| [Search Fields](../features.md#search-filtering)   | name  (?search=name)                                  |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/tags/
```

#####Response (Status: 200 OK)

```json
{
 "count": 36,
 "next": "http://snippit.in/api/tags/?page=2",
 "previous": null,
 "results": [
   {
    "name": "java",
    "slug": "java",
    "snippets": 0
   },
   {
    "name": "c#",
    "slug": "c",
    "snippets": 0
   },
   {
    "name": "javascript",
    "slug": "javascript",
    "snippets": 1
   },
   {"name": "php",
    "slug": "php",
    "snippets": 0
   },
   {"name": "android",
    "slug": "android",
    "snippets": 0
   },
   {
    "name": "jquery",
    "slug": "jquery",
    "snippets": 0
   },
   {
    "name": "python",
    "slug": "python",
    "snippets": 1
   },
   {
    "name": "html",
    "slug": "html",
    "snippets": 0
   },
   {
    "name": "c++",
    "slug": "c-2",
    "snippets": 0
   },
   {
    "name": "mysql",
    "slug": "mysql",
    "snippets": 0
   }
  ]
}
```

List Tag Snippets
==============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/tags/`<tag-slug>`/snippets/                      |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | name, created_at (?ordering=-name) |
| [Search Fields](../features.md#search-filtering)   | name  (?search=name) |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/tags/python/snippets/
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
      "followers": 0,
      "followings": 1,
      "avatar": "https://secure.gravatar.com/avatar/0e9c41bcb61898589d9d1ebfa18c62b4?s=130&d="
     },
     "created_at": "17-06-2014 21:26",
     "stars": 0,
     "comments": 1,
     "pages": 1,
     "url": "http://snippit.in/api/snippets/python-js-test/",
     "comments_url": "http://snippit.in/api/snippets/python-js-test/comments/",
     "star_url": "http://snippit.in/api/snippets/python-js-test/star/"
    }
  ]
}
```