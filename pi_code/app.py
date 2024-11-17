import base64
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import qrcode


app = Flask(__name__)
CORS(app)

# In-memory task storage
tasks = []

# Sort tasks function
def sort_tasks():
    global tasks
    tasks.sort(key=lambda x: x['text'].lower())

# Home route to render the HTML page
@app.route('/')
def index():
    sort_tasks()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        task = {"id": len(tasks) + 1, "text": task_text}
        tasks.append(task)
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/print', methods=['POST'])
def print():
    global tasks

    
    img = qrcode.make('Some data here')
    type(img)  # qrcode.image.pil.PilImage
    img.save("qr_code.png")

    data = open('qr_code.png', 'rb').read() # read bytes from file
    data_base64 = base64.b64encode(data)  # encode to base64 (bytes)
    data_base64 = data_base64.decode()    # convert bytes to string

    # Save the output to a file
    with open('label_to_print.html', 'w') as f:
        f.write(render_template('label.html', tasks=tasks, qr_code=data_base64))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
