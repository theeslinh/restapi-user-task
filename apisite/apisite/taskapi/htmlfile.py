html = '''
<!DOCTYPE html>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>App index</title>
</head>
<body>
	App index:
	<ul>
		<li>[POST] signup at  <a href="/app/signup">/app/signup</a></li>
		<li>[POST] signin at  <a href="/app/signin">/app/signin</a></li>
		<li>[GET] view users list  <a href="/app/users">/app/users</a></li>
		<li>[GET] view tasks list  <a href="/app/tasks">/app/tasks</a></li>
		<li>[GET] view a single user  <a href="/app/users/1">/app/users/1</a></li>
		<li>[GET] view a single task  <a href="/app/tasks/1">/app/tasks/1</a></li>
		<li>[POST] add a new task  <a href="/app/tasks">/app/tasks</a></li>
		<li>[PATCH] update a task  <a href="/app/tasks/1">/app/tasks/1</a></li>
		<li>[DEL] remove a task  <a href="/app/tasks/1">/app/tasks/1</a></li>
		<li>[GET] view all tasks of a user  <a href="/app/users/1/tasks">/app/users/1</a></li>
		<li>[POST] assign tasks to a user  <a href="/app/users/1/tasks">/app/users/1</a></li>
	</ul>
</body>
</html>
'''