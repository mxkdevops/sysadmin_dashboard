
from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

tasks = [
    "Check CPU Usage",
    "Check Uptime",
    "Check Firewall Status",
    "Check SSH Status",
    "Check Logins",
]

def run_command(task):
    commands = {
        "Check CPU Usage": "top -bn1 | grep 'Cpu(s)'",
        "Check Uptime": "uptime",
        "Check Firewall Status": "sudo ufw status",
        "Check SSH Status": "systemctl status ssh",
        "Check Logins": "who",
    }
    cmd = commands.get(task)
    if not cmd:
        return "Unknown task", "danger"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        # Mark success if command returned without error
        return result, "success"
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e}", "danger"
    except Exception as e:
        return f"Error: {e}", "danger"

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/run_task_json', methods=['POST'])
def run_task_json():
    data = request.get_json()
    task = data.get('task')
    output, status = run_command(task)
    return jsonify({'task': task, 'output': output, 'status': status})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
