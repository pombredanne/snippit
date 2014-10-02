List Of languages
==================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/languages/                                       |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | name, pages (?ordering=-name)                         |
| Search Fields   | name  (?search=name)                                  |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/languages/
```

#####Response (Status: 200 OK)

```json
{
 "count": 284,
 "next": "http://snippit.in/api/languages/?page=2",
 "previous": null,
 "results": [
   {
    "name": "Text",
    "slug": "text",
    "pages": 0
   },
   {
    "name": "ActionScript",
    "slug": "actionscript",
    "pages": 0
   },
   {
    "name": "C",
    "slug": "c",
    "pages": 0
   },
   {
    "name": "C#",
    "slug": "c-2",
    "pages": 0
   },
   {
    "name": "C++",
    "slug": "c-3",
    "pages": 0
   },
   {
    "name": "Clojure",
    "slug": "clojure",
    "pages": 0
   },
   {
    "name": "CoffeeScript",
    "slug": "coffeescript",
    "pages": 0
   },
   {
    "name": "Common Lisp",
    "slug": "common-lisp",
    "pages": 0
   },
   {
    "name": "CSS",
    "slug": "css",
    "pages": 0
   },
   {
    "name": "Diff",
    "slug": "diff",
    "pages": 0
   }
  ]
}
```

List Language Snippets
==============================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/language/`<language-slug>`/snippets/             |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Permission      | Allow Any                                             |
| [Ordering Fields](../features.md#ordering-filter) | name, created_at (?ordering=-name)                    |
| [Search Fields](../features.md#search-filtering)   | name  (?search=name)                                  |
| Content-Type    | application/json                                      |

#####Request ([Other request types](../example.md))

```bash
curl -X GET -H "Content-Type: application/json" http://snippit.in/api/languages/javascript/snippets/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
   {
    "name": "Knockout JS Test",
    "slug": "knockout-js-test",
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
      "avatar": "https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd?s=130&d="
    },
    "created_at": "17-06-2014 21:26",
    "stars": 0,
    "comments": 1,
    "pages": 1,
    "url": "http://snippit.in/api/snippets/knockout-js-test/",
    "comments_url": "http://snippit.in/api/snippets/knockout-js-test/comments/",
    "star_url": "http://snippit.in/api/snippets/knockout-js-test/star/"
   }
  ]
}
```