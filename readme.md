# HƯỚNG DẪN SỬ DỤNG
### CÀI ĐẶT THƯ VIỆN
- Cài đặt [Python](https://www.python.org/downloads/release/python-368/) và [thêm Python vào user PATH](https://docs.python.org/3/using/windows.html)
- Khởi động Windows Command Prompt và nhập lệnh
```
>>> pip install --user django==3.2.12 PyJWT django-cors-headers djangorestframework==3.13.1 mysqlclient
```
- Kiểm tra kết quả cài đặt
```
>>> pip show django PyJWT djangorestframework django-cors-headers mysqlclient
```
### DEPLOY 
- Tải xuống [project repo](https://github.com/theeslinh/restapi-user-task/archive/refs/heads/main.zip) và giải nén
- Khởi động Windows Command Prompt và chạy lệnh
```
>>> cd /thư/mục/project/repo
>>> python manage.py makemigrations taskapi
>>> python manage.py migrate
>>> python manage.py runserver
```
- Khởi động trình duyệt, truy cập vào địa chỉ [127.0.0.1:8000/app/](http://127.0.0.1:8000/app/)
----------
## THỬ NGHIỆM CÁC  API
#### 1. SIGN-UP
Truy cập vào địa chỉ http://127.0.0.1:8000/app/signup và điền vào ô CONTENT như sau:
```json
{
    "name": "myname",
    "password": "mypassword"
}
```
rồi nhấn `POST`. Response sẽ giống như sau:
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 6,
    "name": "myname"
}
```
#### 2. SIGN-IN
Sau khi đăng ký, server đã trả về id của `"myname"` là `6`, ta sẽ dùng id này để đăng nhập. Truy cập vào địa chỉ http://127.0.0.1:8000/app/signin và điền vào ô CONTENT như sau, 
```json
{
    "id": 6,
    "password": "mypassword"
}
```
rồi nhấn POST. Response sẽ giống như sau:
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "signed in"
}
```
#### 3. GET-ALL-USER
Sau khi đã đăng nhập, ta đã có chứng thực JWT lưu trong cookie nên có thể truy cập được những api khác. Trước hết ta xem danh sách users trong hệ thống đã được cập nhật mới chưa.
Truy cập vào địa chỉ http://127.0.0.1:8000/app/users ta nhận được response như sau
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "aname"
    },
    ...
    {
        "id": 6,
        "name": "myname"
    }
]
```
#### 4. GET-ALL-TO-DO
Truy cập vào địa chỉ http://127.0.0.1:8000/app/users ta nhận được response như sau
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "search",
        "descr": "search lots of stuffs",
        "user_id": 2,
        "due": "2022-03-26T06:06:06",
        "status": "NEW",
        "created": "2022-03-26T12:12:33.419464",
        "modified": "2022-03-26T14:52:28.988721"
    },
    ...
]
```
#### 5. ADD-TO-DO
Ta sẽ thêm to-do record vào danh sách có sẵn. Truy cập vào địa chỉ http://127.0.0.1:8000/app/tasks và điền vào ô CONTENT như sau, 
```json
{
    "name": "eval",
    "descr": "evaluate stuffs",
    "user_id": 4,
    "due": "2022-04-01T01:01:01",
    "status": "COMPLETE"
}
```
rồi nhấn `POST`. Response sẽ giống như sau:
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 6,
    "name": "eval",
    "descr": "evaluate stuffs",
    "user_id": 4,
    "due": "2022-04-01T01:01:01",
    "status": "COMPLETE",
    "created": "2022-03-25T18:18:35.049334",
    "modified": "2022-03-25T18:18:35.049334"
}
```
#### 6. GET-TO-DO-BY-ID
Ta sẽ xem riêng 1 record trong danh sách. Truy cập vào địa chỉ http://127.0.0.1:8000/app/tasks/4 ta nhận được response như sau
```
HTTP 200 OK
Allow: GET, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 4,
    "name": "write",
    "descr": "write stuff",
    "user_id": 2,
    "due": "2022-03-26T06:06:06",
    "status": "NEW",
    "created": "2022-03-26T12:37:47.978286",
    "modified": "2022-03-26T12:38:37.059619"
}
```
#### 7. UPDATE-TO-DO
Ta sẽ cập nhật riêng 1 record trong danh sách. Truy cập vào địa chỉ http://127.0.0.1:8000/app/tasks/4 và nhập vào ô content như sau:
```json
{
    "status": "COMPLETE"
}
```
Sau khi nhấn `PATCH`, ` "status": "NEW"` chuyển thành ` "status": "COMPLETE"`.
#### 8. REMOVE-TO-DO
Ta sẽ xoá 1 record trong danh sách. Truy cập vào địa chỉ http://127.0.0.1:8000/app/tasks/4 và nhấn vào ô `DELETE`, xác nhận và tải lại trang, response là
```
HTTP 404 Not Found
Allow: GET, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Not found."
}
```
Record đã bị xoá trong database
#### 9. GET-ALL-TASK-BY-USER
Ta sẽ xem danh sách to-do của một user. Truy cập vào địa chỉ http://127.0.0.1:8000/app/users/2/tasks nhận được response như bên dưới. User có 2 to-dos.
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "search",
        "descr": "search lots of stuffs",
        "user_id": 2,
        "due": "2022-03-26T06:06:06",
        "status": "NEW",
        "created": "2022-03-26T12:12:33.419464",
        "modified": "2022-03-26T14:52:28.988721"
    },
    ...
]
```

#### 10. ASSIGN-TO-USER
Ta sẽ gán to-do cho một user. Truy cập vào địa chỉ http://127.0.0.1:8000/app/users/2/tasks và nhập vào ô content như sau:
```json
{
    "taskid": 6
}
```
nhấn `POST` rồi tải lại, ta thấy user 2 có thêm 1 task mới, là task 6 vừa được gán.

-------
## QUẢN LÝ DATABASE
Nhập lệnh sau vào Windows Command Prompt để bật giao diện IPython
```python
>>> python manage.py shell
In [1]: from taskapi.models import Task, User
In [2]: User.objects.all()
Out[2]: <QuerySet [<User: aname>, <User: bname>, <User: dname>, <User: ename>, <User: myname>]>
In [3]: Task.objects.all()
Out[3]: <QuerySet [<Task: search>, <Task: read>, <Task: eval>]>
In [4]: User.objects.get(pk=2).task_set.all()
Out[4]: <QuerySet [<Task: search>, <Task: read>, <Task: eval>]>
```
Vậy, cả 2 phía người dùng lẫn server đều hoạt động tốt.
