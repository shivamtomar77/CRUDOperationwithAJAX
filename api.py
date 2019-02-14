from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource
import mysql.connector
app = Flask(__name__)
api = Api(app)

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="bhai9630",
  database="mydatabase"
)

mycursor = db.cursor(dictionary=True)


TODOS = []
"""TODOS ={
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}
"""

@app.route("/template-2", methods=['GET'])
def get_tasks():
    return render_template('simpleform.html')


def abort_if_todo_doesnt_exist(id):
    if id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(id))

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('country_name')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def delete(self, id):
        sql = "DELETE FROM country_list WHERE id = %(id)s;"
        params = {
            'id': int(id)
        }
        mycursor.execute(sql, params)
        db.commit()

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        sql = "SELECT id, country_name FROM country_list"
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        countries = []
        for row in rows:
            countries.append({'id': row['id'], 'country_name': row['country_name']})
        return countries

    def post(self):
        sql = "INSERT INTO country_list (country_name) VALUES (%(country_name)s)"
        val = request.json['country_name']
        params = {
            'country_name': val
        }
        mycursor.execute(sql, params)
        db.commit()

    def put(self):
        id = int(request.json['id'])
        country_name = request.json['country_name']
        sql = "UPDATE country_list SET country_name = %(country_name)s WHERE id = %(id)s;"
        params = {
            'id': id,
            'country_name': country_name
        }
        mycursor.execute(sql, params)
        db.commit()

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)