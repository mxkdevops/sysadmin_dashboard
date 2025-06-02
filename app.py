from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

tasks = [
    "Check CPU Usage",
    "Check Uptime",
    "Check Firewall Status",
    # Add all your tasks here
]

def run_your_command(task):
    # Map tasks to shell commands or Python checks
    commands = {
        "Check CPU Usage": "top -bn1 | grep 'Cpu(s)'",
        "Check Uptime": "uptime",
        "Check Firewall Status": "sudo ufw status",
        # Add commands here
    }
    cmd = commands.get(task)
    if not cmd:
        return "Unknown task"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result
    except Exception as e:
        return f"Error running task: {e}"

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/run_task_json', methods=['POST'])
def run_task_json():
    data = request.get_json()
    task = data.get('task')
    output = run_your_command(task)
    return jsonify({'task': task, 'output': output})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
