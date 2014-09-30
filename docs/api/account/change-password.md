User Change Password
=====================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/account/`<username>`/change-password/            |
| Method          | PUT                                                   |
| Status Codes    | 200                                                   |
| Permission      | Authenticated                                         |

```bash
curl -X PUT -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     -d '{"password":"12345", "new_password": "123456", "confirm_password": "123456"}'
     http://snippit.in/api/account/bahattincinic/change-password/
```

#####Payload - raw

| Paramether        | Type     | Description                      | Required |
| ----------------- | -------- |--------------------------------- | -------- |
| password          | String   | current password                 | Yes      |
| new_password      | String   | new password                     | Yes      |
| confirm_password  | String   | new password confirmation        | Yes      |


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
 "avatar": "<Gravatar Url>"
}
```

#####Errors (Status: 400 Bad Request)

```json
{
 "password": ["passwords invalid"]
}
```

```json
{
 "non_field_errors": ["passwords did not match"]
}
```