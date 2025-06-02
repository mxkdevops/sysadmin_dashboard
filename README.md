# sysadmin_dashboard
### What this does:
- Tasks show as Bootstrap buttons.
- Clicking a task opens a tab (or focuses existing tab) with that task’s live output.
- Each tab has a loading spinner while fetching.
- Output refreshes every 10 seconds automatically.
- Output includes a colored badge: green for success, red for failure.
- Tabs have a close (×) button.
- Multiple task outputs shown simultaneously with easy switching.
- Styled with Bootstrap 5 for a clean, responsive UI.

### What Was Missing and How It Was Resolved:
1. Flask binding to all network interfaces:
   - changed Flask app to run with host='0.0.0.0', which made Flask listen on all IP addresses, not just localhost.

3. Lightsail firewall rules:
-  opened port 5000 for incoming traffic, allowing your IP or all IPs (0.0.0.0/0) in the Lightsail instance’s firewall settings.

4. Instance internal firewall (ufw):
 - Lightsail instance had its own firewall (ufw) blocking port 5000.
 -  sudo ufw allow 5000/tcp to open port 5000 on the instance itself.
