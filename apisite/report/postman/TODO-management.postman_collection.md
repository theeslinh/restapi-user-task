|  info.\_postman_id                     | info.name       | info.schema      |
| ------------------------------------ | --------------- |---------------------- | 
| fbaff0d9-9eac-4a89-a6b5-03f773f4055b | TODO-management | https://schema.getpostman.com/json/collection/v2.1.0/collection.json |

# SIGN-UP | POST
```json
{
    "name": "dname",
    "password": "dpass"
} 
```
json  | 127.0.0.1:8000/app/signup
-----------------------
SIGN-UP là API cho phép người dùng mới đăng ký vào hệ thống. Để sign up người dùng cần nhập 2 trường thông tin
*   `"name" (char) [max_length=16, blank=False, null=False]`
*   `"password" (char) [max_length=16, blank=False, null=False]`

Hệ thống sau khi nhận được password sẽ mã hoá trước khi lưu vào database. Ví dụ:

|  | name | password |
| --- | --- | --- |
| user side | `dname` | `dpass` |
| server side | `dname` | `pbkdf2_sha256$260000$ltu9dqF70KW5kCeyBoSFAk$VZmnotRM61xMT47TP11v+a+lBX7TCuotNMzA2+iA/BY=` |

Response từ server có dạng như sau:

``` json
{
    "id": 4,
    "name": "dname"
}
``` 

# SIGN-IN  | noauth | POST 
```json
{
    "id": "4",
    "password": "dpass"
}
```
json | 127.0.0.1:8000/app/signin
----------
SIGN-IN là API cho phép người dùng đăng nhập vào hệ thống. Để sign in người dùng cần nhập 2 trường thông tin

*   `"id" (char) [max_length=16, blank=False, null=False]`
*   `"password" (char) [max_length=16, blank=False, null=False]`
    

Nếu đăng nhập thành công, response data từ server có dạng như sau:

``` json
{
    "message": "signed in"
}
```

Chứng thực JWT được lưu ở cookie, thời gian sống là 60 phút, có thể được trích xuất như sau:

``` python
token = request.COOKIES.get('jwt')
print(token)
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwiZXhwIjoxNjQ4MjY5MzY1LCJpYXQiOjE2NDgyNjU3NjV9.lQ1sDLv3FrSQqQx-SHLAF85Ci6h0Ory5ozGs5eKazkE'
```
# ADD-TO-DO   | POST        
```json
{
    "name": "read",
    "descr": "read stuff",
    "user_id": 2,
    "due": "2022-03-26T09:09:09"
} 
```
json       | 127.0.0.1:8000/app/tasks
----
Cho phép người dùng thêm 1 record to-do vào database. Thông tin 1 record to-do bao gồm:

*   `"id" (int) [hidden=True, editable=False]`: id của task
*   `"name\' (char) [max_length=16, blank=False, null=False]`: tên của task
*   `"descr" (char) [max_length=255]:`mô tả chi tiết của task
*   `"user_id" (int)`: Id của user được assign task này
*   `"due" (datetime)`: task phải được hoàn thành trước thời gian này
*   `"status" (char) [default=\'NEW\']`: nhận một trong 2 giá trị NEW hoặc COMPLETE
*   `"created" (datetime) [hidden=True, editable=False]`: ngày khởi tạo
*   `"modified" (datetime) [hidden=True]`: ngày chỉnh sửa cuối
    

Response từ server có dạng:

``` json
{
    "id": 5,
    "name": "read",
    "descr": "read stuff",
    "user_id": 2,
    "due": "2022-03-26T09:09:09",
    "status": "NEW",
    "created": "2022-03-25T12:49:18.044541",
    "modified": "2022-03-25T12:49:18.044541"
}
``` 
# UPDATE-TO-DO | PATCH  
```json
{
    "descr": "eval lots of stuffs"
}
```
json       | 127.0.0.1:8000/app/tasks/2 
------
Cho phép người dùng cập nhật 1 record to-do nếu trạng thái của nó không phải là COMPLETE. Các miền được phép chỉnh sửa:

*   `"name" (char) [max_length=16, blank=False, null=False]`: tên của task
*   `"descr" (char) [max_length=255]`: mô tả chi tiết của task
*   `"user_id" (int)`: Id của user được assign task này
*   `"due" (datetime)`: task phải được hoàn thành trước thời gian này
*   `"status" (char) [default=\'NEW\']`: nhận một trong 2 giá trị ` NEW` hoặc ` COMPLETE`
    

Ví dụ: request bên trên yêu cầu chỉnh sửa `"descr"` của task, response có dạng như sau:

``` json
{
    "id": 1,
    "name": "search",
    "descr": "eval lots of stuffs",
    "user_id": 1,
    "due": "2022-03-26T06:06:06",
    "status": "NEW",
    "created": "2022-03-25T12:12:33.419464",
    "modified": "2022-03-25T14:31:10.973016"
}
```
# REMOVE-TO-DO | DELETE  
127.0.0.1:8000/app/tasks/2 
----
Cho phép người dùng xóa 1 task record nếu trạng thái của nó không phải là `COMPLETE`.

Response là trạng thái trước khi bị xoá của task

``` json
{
    "id": 2,
    "name": "eval",
    "descr": "eval lots of stuffs",
    "user_id": 2,
    "due": "2022-03-26T07:07:07",
    "status": "NEW",
    "created": "2022-03-25T12:13:10.381345",
    "modified": "2022-03-25T12:15:19.148293"
}
```
# GET-ALL-TO-DO | GET 
127.0.0.1:8000/app/tasks
----
Trả về danh sách tất cả các tasks hiện có.

Response có dạng như sau:

``` json
[
    {
        "id": 1,
        "name": "search",
        "descr": "eval lots of stuffs",
        "user_id": 1,
        "due": "2022-03-26T06:06:06",
        "status": "NEW",
        "created": "2022-03-25T12:12:33.419464",
        "modified": "2022-03-25T14:31:10.973016"
    },
    {
        "id": 4,
        "name": "write",
        "descr": "write stuff",
        "user_id": 2,
        "due": "2022-03-26T06:06:06",
        "status": "NEW",
        "created": "2022-03-25T12:37:47.978286",
        "modified": "2022-03-25T12:38:37.059619"
    }
]
```
# GET-TO-DO   | GET 
127.0.0.1:8000/app/tasks/1
----
Trả về chi tiết của một task với đầu vào là `"id"` của task đó.

Response có dạng như sau:

``` json
{
    "id": 1,
    "name": "search",
    "descr": "eval lots of stuffs",
    "user_id": 1,
    "due": "2022-03-26T06:06:06",
    "status": "NEW",
    "created": "2022-03-25T12:12:33.419464",
    "modified": "2022-03-25T14:31:10.973016"
}
``` 
# GET-ALL-USERS | GET 
127.0.0.1:8000/app/users
-----
Trả về danh sách tất cả các users hiện có.

Response có dạng như sau:

``` json
[
    {
        "id": 1,
        "name": "aname"
    },
    {
        "id": 2,
        "name": "bname"
    },
    {
        "id": 4,
        "name": "dname"
    },
    {
        "id": 5,
        "name": "ename"
    }
]
``` 
# GET-ALL-TASKS-BY-USER | GET 
127.0.0.1:8000/app/users/2/tasks
-----
Trả về danh sách tất cả các task được assign cho một user.

Response có dạng như sau:

``` json
[
    {
        "id": 4,
        "name": "write",
        "descr": "write stuff",
        "user_id": 2,
        "due": "2022-03-26T06:06:06",
        "status": "NEW",
        "created": "2022-03-25T12:37:47.978286",
        "modified": "2022-03-25T12:38:37.059619"
    },
    {
        "id": 5,
        "name": "read",
        "descr": "read stuff",
        "user_id": 2,
        "due": "2022-03-26T09:09:09",
        "status": "NEW",
        "created": "2022-03-25T12:49:18.044541",
        "modified": "2022-03-25T12:49:18.044541"
    }
]
```
# ASSIGN-TO-DO | POST       
```json
{
    "taskid": 1
} 
```
json       | 127.0.0.1:8000/app/users/2/tasks
----
Với đầu vào là `"taskid"` id của 1 task, thực hiện assign task này cho một user hiện có trong hệ thống. User được assign không trùng với user tạo ra chứng thực JWT đang được dùng.

API này tương tự như UPDATE-TO-DO, nhưng chỉ có field `"user_id"` cần thay đổi:

*   `"taskid" (int)`: id của task được gán cho người dùng này.
    

Response có dạng như sau:

``` json
{
    "id": 1,
    "name": "search",
    "descr": "search lots of stuffs",
    "user_id": 2,
    "due": "2022-03-26T06:06:06",
    "status": "NEW",
    "created": "2022-03-25T12:12:33.419464",
    "modified": "2022-03-25T14:52:28.988721"
}
``` 