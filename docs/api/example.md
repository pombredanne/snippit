Javascript Example
===================

```javascript
var payload = {"username":"bahattincinic","email":"bahattincinic@gmail.com", "first_name": "bahattincinic"};

$.ajax({
    type: "PUT",
    url: 'http://snippit.in/api/account/bahattincinic/',
    headers: { "Authorization" : "Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2" },
    contentType: "application/json",
    data: JSON.stringify(payload),
    success: function(data) {
        alert(JSON.stringify(data));
    },
    error: function(error) {
        alert(JSON.stringify(error));
    }
});
```

Python Example
=====================
```python
import requests # http://docs.python-requests.org/en/latest/
url = 'http://snippit.in/api/account/bahattincinic/'
payload = {"username":"bahattincinic","email":"bahattincinic@gmail.com", "first_name": "bahattincinic"}
response = requests.put(url, payload, headers={'Authorization': 'Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2'})

response.status_code # 200 OK
```