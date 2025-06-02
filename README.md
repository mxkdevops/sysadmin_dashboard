# Web-Based Dashboard (Lightweight HTML + Bash Hooks) sysadmin_dashboard
### What this does:
- Tasks show as Bootstrap buttons.
- Clicking a task opens a tab (or focuses existing tab) with that task’s live output.
- Each tab has a loading spinner while fetching.
- Output refreshes every 10 seconds automatically.
- Output includes a colored badge: green for success, red for failure.
- Tabs have a close (×) button.
- Multiple task outputs shown simultaneously with easy switching.
- Styled with Bootstrap 5 for a clean, responsive UI.

### 1️⃣ Install Flask
Make sure Python 3 and pip are installed:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install flask
```
### 2️⃣ Create your Flask app folder and files
```bash
mkdir ~/sysadmin_dashboard
cd ~/sysadmin_dashboard
Create a file app.py:
Create templates folder and HTML files
Create templates/result.html:
```
### 4️⃣ Run your Flask app locally
```bash
python3 app.py
Open your browser and go to:
http://127.0.0.1:5000/
```
### 5️⃣ Notes:
Some commands like sudo ufw status require sudo. You can configure /etc/sudoers to allow your user to run these commands without password, e.g.:
sudo visudo
# Add this line (replace username with your user):
username ALL=(ALL) NOPASSWD: /usr/sbin/ufw
You can add more tasks or adjust commands in TASKS dict in app.py.


### 🔍 1. Verify Flask is Listening on All Interfaces
Ensure your Flask application is configured to listen on all network interfaces. In your app.py, modify the app.run() line as follows:
```bash
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
```

This change allows Flask to accept connections from any IP address, not just 127.0.0.1 (localhost).

## 🔐 2. Check for Local Firewall Rules on the Lightsail Instance
Even if AWS Lightsail's firewall allows traffic on port 5000, the instance's internal firewall (e.g., ufw or iptables) might block it. To check and modify these settings:

For ufw (Uncomplicated Firewall):
Check the status:
```bash
sudo ufw status
If ufw is active and blocking port 5000, proceed to the next step.

Allow traffic on port 5000:

sudo ufw allow 5000/tcp
Reload ufw to apply changes:

sudo ufw reload
For iptables:
Allow traffic on port 5000:

sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
Save the iptables rules to ensure they persist after reboot:

sudo iptables-save > /etc/iptables/rules.v4
### 🔄 3. Restart Your Flask Application
After making the above changes, restart your Flask application:

python3 app.py
Ensure it starts without errors and is listening on 0.0.0.0:5000.

### 🌐 4. Access the Application from Your Local Browser
In your local browser, navigate to:

http://<your-lightsail-public-ip>:5000/
Replace <your-lightsail-public-ip> with the actual public IP address of your Lightsail instance.

### 🛠️ 5. Additional Debugging
If you're still unable to access the application:
Check if Flask is listening on port 5000:
sudo netstat -tlnp | grep 5000
or

sudo ss -tlnp | grep 5000
Ensure that Flask is indeed listening on 0.0.0.0:5000.

Verify that no other service is occupying port 5000:

sudo lsof -i :5000
This command will list any processes using port 5000.


### What Was Missing and How It Was Resolved:
1. Flask binding to all network interfaces:
   - changed Flask app to run with host='0.0.0.0', which made Flask listen on all IP addresses, not just localhost.

3. Lightsail firewall rules:
-  opened port 5000 for incoming traffic, allowing your IP or all IPs (0.0.0.0/0) in the Lightsail instance’s firewall settings.

4. Instance internal firewall (ufw):
 - Lightsail instance had its own firewall (ufw) blocking port 5000.
 -  sudo ufw allow 5000/tcp to open port 5000 on the instance itself.
