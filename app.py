
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
    import subprocess
    import re

    def format_result(msg, status):
        return msg, status

    try:
        if task == "Check CPU Usage":
            result = subprocess.check_output("top -bn1 | grep 'Cpu(s)'", shell=True, text=True)
            usage = float(re.search(r'(\d+\.\d+)\s*id', result).group(1))
            cpu_used = 100 - usage
            if cpu_used > 80:
                return format_result(f"⚠️ High CPU usage: {cpu_used:.1f}%", "warning")
            return format_result(f"✅ CPU usage normal: {cpu_used:.1f}%", "success")

        elif task == "Check Memory Usage":
            result = subprocess.check_output("free -m", shell=True, text=True)
            lines = result.splitlines()
            mem = [int(x) for x in lines[1].split()[1:4]]
            used_percent = (mem[1] / mem[0]) * 100
            if used_percent > 80:
                return format_result(f"⚠️ High memory usage: {used_percent:.1f}%", "warning")
            return format_result(f"✅ Memory usage normal: {used_percent:.1f}%", "success")

        elif task == "Check Firewall Status":
            result = subprocess.check_output("sudo ufw status", shell=True, text=True)
            if "inactive" in result.lower():
                return format_result("❌ Firewall is INACTIVE", "danger")
            return format_result("✅ Firewall is ACTIVE\n" + result, "success")

        elif task == "Check SSH Status":
            result = subprocess.check_output("systemctl is-active ssh", shell=True, text=True).strip()
            if result == "active":
                return format_result("✅ SSH is running", "success")
            else:
                return format_result("❌ SSH is not running", "danger")

        elif task == "Check Logins":
            result = subprocess.check_output("last -n 5", shell=True, text=True)
            return format_result("✅ Last 5 login attempts:\n" + result, "success")

        elif task == "Check Open Ports":
            result = subprocess.check_output("sudo ss -tuln", shell=True, text=True)
            risky_ports = []
            for line in result.splitlines():
                if re.search(r':23\b', line):  # Telnet
                    risky_ports.append("⚠️ Telnet (23) is open")
                elif re.search(r':21\b', line):  # FTP
                    risky_ports.append("⚠️ FTP (21) is open")
            summary = "\n".join(risky_ports) if risky_ports else "✅ No risky ports open"
            return format_result(summary + "\n\n" + result, "warning" if risky_ports else "success")

        elif task == "Check Failed Login Attempts":
            result = subprocess.check_output("grep 'Failed password' /var/log/auth.log | tail -n 5", shell=True, text=True)
            if result.strip():
                return format_result("⚠️ Failed login attempts detected:\n" + result, "warning")
            else:
                return format_result("✅ No failed login attempts found", "success")

        else:
            return format_result("Unknown task", "danger")

    except subprocess.CalledProcessError as e:
        return format_result(f"Command failed: {e}", "danger")
    except Exception as e:
        return format_result(f"Error: {e}", "danger")

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
