
from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

tasks = [
    "Check CPU Usage",
    "Check Uptime",
    "Check Firewall Status",
    "Check SSH Status",
    "Check Logins",
    "Check for Failed SSH Login Attempts",
    "List Blocked IPs (via UFW/IPTables)",
    "Check for Open Ports",
    "Verify Active UFW Rules",
    "Check for Root Login Attempts",
    "List Recently Installed Packages",
    "Check for Users with Sudo Access",
    "Scan for World-Writable Files",
    "Check for Suspicious Processes",
    "Check Cron Jobs for All Users",
    "Monitor Auth Log for Brute Force Patterns",
    "Check if SSH Root Login is Disabled",
    "Check for Publicly Accessible Services",
    "Check for Known Vulnerabilities (via apt)"
]

def run_command(task):
    commands = {
        "Check CPU Usage": "top -bn1 | grep 'Cpu(s)'",
        "Check Uptime": "uptime",
        "Check Firewall Status": "sudo ufw status",
        "Check SSH Status": "systemctl status ssh",
        "Check Logins": "who",

        # 🔐 Security-focused tasks
        "Check for Failed SSH Login Attempts": "sudo grep 'Failed password' /var/log/auth.log | tail -n 10",
        "List Blocked IPs (via UFW/IPTables)": "sudo iptables -L -n --line-numbers",
        "Check for Open Ports": "sudo ss -tuln",
        "Verify Active UFW Rules": "sudo ufw show added",
        "Check for Root Login Attempts": "sudo grep 'root' /var/log/auth.log | tail -n 10",
        "List Recently Installed Packages": "grep 'install ' /var/log/dpkg.log | tail -n 10",
        "Check for Users with Sudo Access": "getent group sudo",
        "Scan for World-Writable Files": "sudo find / -type f -perm -0002 -exec ls -l {} + 2>/dev/null | head -n 10",
        "Check for Suspicious Processes": "ps aux --sort=-%cpu | head -n 10",
        "Check Cron Jobs for All Users": "for user in $(cut -f1 -d: /etc/passwd); do crontab -u $user -l 2>/dev/null; done",
        "Monitor Auth Log for Brute Force Patterns": "sudo grep 'authentication failure' /var/log/auth.log | tail -n 10",
        "Check if SSH Root Login is Disabled": "sudo grep '^PermitRootLogin' /etc/ssh/sshd_config",
        "Check for Publicly Accessible Services": "sudo netstat -tulpn | grep '0.0.0.0'",
        "Check for Known Vulnerabilities (via apt)": "apt list --upgradable 2>/dev/null | grep -v Listing | head -n 10",
    }

    cmd = commands.get(task)
    if not cmd:
        return "Unknown task", "danger"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
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
