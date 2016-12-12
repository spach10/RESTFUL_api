#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

#returns the whole list of tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


from flask import abort
#returns the task that the user asks for
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
   	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		return not_found(404)
	return jsonify({'task': task[0]})


from flask import make_response
#Gives an error is the url isn't there
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from flask import request
#POST method: insert new item into the list
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
