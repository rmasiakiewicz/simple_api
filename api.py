import csv
import io

from flask import Flask, make_response

from database import Database

app = Flask(__name__)
db = Database(check_same_thread=False)


@app.route('/')
def index():
    return 'hello'


@app.route("/app/user_task")
def get_csv():
    users = db.get_users()
    todos = db.get_todos()
    user_by_user_id = {user.user_id: user for user in users}
    header = ["name", "city", "title", "completed"]
    data = []
    for todo in todos:
        user = user_by_user_id[todo.user_id]
        completed = "YES" if todo.completed == 1 else "NO"
        data.append([user.name, user.address["city"], todo.title, completed])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(header)
    writer.writerows(data)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=user_task.csv"
    response.headers["Content-type"] = "text/csv"
    return response
