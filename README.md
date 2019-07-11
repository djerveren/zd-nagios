# Zenduty Nagios Integration
Nagios is a free and open source computer-software application that monitors systems, networks and infrastructure. Nagios offers monitoring and alerting services for servers, switches, applications and services. To integrate Nagios with Zenduty, complete the following steps:

### On the Zenduty Dashboard:

1. To add a new Nagios integration, go to "Teams" on Zenduty and click on the "Manage" button corresponding to the team you want to add the integration to.

2. Next, go to "Services" and click on the "Manage" button correspoding to the relevant Service.

3. Go to "Integrations" and then "Add New Integration". Give it a name and select the application "Nagios" from the dropdown menu.

4. Go to "Configure" under your integrations and copy the integration key generated.

### In Nagios: 

1. Install Nagios Core on your system.
2. Download the Zenduty-Nagios files by following the steps given below:
```
$ cd /tmp
$ git clone https://github.com/Zenduty/zd-nagios.git
$ cd zd-nagios
```
3. Open zenduty_nagios.cfg file and enter the integration key provided into the “pager” field.
4. Move the Nagios Core configuration file into place. For Debian-based systems this is usually /etc/nagios3/conf.d:
```
$ mv zenduty_nagios.cfg /etc/nagios3/conf.d
```
For RHEL-based systems this is usually /etc/nagios:
```
$ mv zenduty_nagios.cfg /etc/nagios
```
For source installations, move the file to /usr/local/nagios/etc/objects:
```
$ mv zenduty_nagios.cfg /usr/local/nagios/etc/objects
```
5. Skip this step if you are using a Debian-based distribution. If you are using a RHEL-based distribution, you will need to edit the Nagios Core config to load the ZenDuty config. To do this, open /etc/nagios/nagios.cfg and add this line to the file:
```
$ cfg_file=/etc/nagios/zenduty_nagios.cfg
```
If using a source installation, add this line to the main config file at /usr/local/nagios/etc/nagios.cfg
```
$ cfg_file=/usr/local/nagios/etc/objects/zenduty_nagios.cfg
```
6. Add the contact “zenduty” to your Nagios Core configuration’s main contact group. If you’re using the default configuration, open /etc/nagios3/conf.d/contacts_nagios2.cfg (onDebian-based systems) or /etc/nagios/objects/contacts.cfg (on RHEL-based systems) or/usr/local/nagios/etc/objects/contacts.cfg  (for source installations) and look for the “admins” contact group. Then, simply add the “zenduty” contact.
```
define contactgroup{
contactgroup_name admins
alias Nagios Administrators
members root,zenduty ; Add zenduty here
}
```
7. Move zenduty_nagios.py to the Nagios plugin folder. For Debian-based systems this is usually /usr/lib/cgi-bin/nagios3/:
```
$ mv zenduty_nagios.py /usr/lib/cgi-bin/nagios3/
```
For most RHEL-based systems this is usually /usr/lib64/nagios/cgi/:
```
$ mv zenduty_nagios.py /usr/lib64/nagios/cgi/
```
For Amazon Linux & CentOS 6+ systems this is usually /usr/local/nagios/sbin:
```
$ mv zenduty_nagios.py /usr/local/nagios/sbin/
```
8. Make the zenduty_nagios.py file executable. For Debian-based systems:
```
$ chmod +x /usr/lib/cgi-bin/nagios3/zenduty_nagios.py
```
For most RHEL-based systems:
```
$ chmod +x /usr/lib64/nagios/cgi/zenduty_nagios.py
```
For Amazon Linux and CentOS 6+ systems:
```
$ chmod +x /usr/local/nagios/sbin/zenduty_nagios.py
```
9. Restart nagios service and your zenduty integration is finished!
```
$ systemctl restart nagios
```
