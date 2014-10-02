Api Features
=========================

####Pagination
Default Pagination Settings (`snippit/settings/base.py`):
  
    REST_FRAMEWORK = {
      'PAGINATE_BY': 10,                 # Default to 10
      'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
      'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
    }

Payload

| Paramether        | Type     |
| ----------------- | -------- |
| page_size         | integer  |
| page              | integer  |

For example, the first page of data and a maximum of 10 units

```bash
curl -X GET  -H "Content-Type: application/json" -d "page_size=10&page=1"
     http://snippit.in/api/tags/
```

####Ordering Filter

Payload

| Paramether        | Type     |
| ----------------- | -------- |
| ordering          | string   |

For example, to order tags by name:

```bash
curl -X GET  -H "Content-Type: application/json" -d "ordering=name"
     http://snippit.in/api/tags/
```

The client may also specify reverse orderings by prefixing the field name with '-', like so:

```bash
curl -X GET  -H "Content-Type: application/json" -d "ordering=-name"
     http://snippit.in/api/tags/
```

Multiple orderings may also be specified:

```bash
curl -X GET  -H "Content-Type: application/json" -d "ordering=name,pages"
     http://snippit.in/api/tags/
```

####Filtering

For example,  open to everyone listing of the snippets

```bash
curl -X GET  -H "Content-Type: application/json" -d "public=True"
     http://snippit.in/api/account/bahattincinic/snippets/
```

###Search Filtering

Payload

| Paramether        | Type     |
| ----------------- | -------- |
| search            | string   |

For example, to search for tags

```bash
curl -X GET  -H "Content-Type: application/json" -d "search=django"
     http://snippit.in/api/tags/
```
