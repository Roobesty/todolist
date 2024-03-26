from flask import Flask, render_template, request, redirect, url_for
import uuid  # for generating unique IDs

app = Flask(__name__, template_folder='templates', static_folder='static')

tasks = []  # initialize an empty list for tasks 

# render the index page and handle task creation
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_date = request.form['task_date']
        task_id = str(uuid.uuid4())  # generate a unique ID for the task
        tasks.append({'id': task_id, 'name': task_name, 'date': task_date})
        return redirect(url_for('index')) # redirect to the index page after task creation
    return render_template('index.html', tasks=tasks)

# render the add_task page
@app.route('/add_task', methods=['GET'])
def add_task():
    return render_template('add_task.html')

# delete a task based on its ID
@app.route('/delete_task/<string:task_id>', methods=['GET'])
def delete_task_route(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id] # remove task with matching ID
    return redirect(url_for('index')) # redirect to the index page after task deletion

# render the edit_task page and handle task editing
@app.route('/edit_task/<string:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return "Task not found", 404  # return a 404 error if task is not found
    if request.method == 'POST':
        task['name'] = request.form['task_name']
        task['date'] = request.form['task_date']
        return redirect(url_for('index')) # redirect to the index page after task editing
    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)