Nagios is a free and open source computer-software application that monitors systems, networks and infrastructure. Nagios offers monitoring and alerting services for servers, switches, applications and services. To integrate Nagios with Zenduty, complete the following steps:

## On the Zenduty Dashboard:

1. To add a new Nagios integration, go to "Teams" on Zenduty and click on the "Manage" button corresponding to the team you want to add the integration to.

2. Next, go to "Services" and click on the "Manage" button correspoding to the relevant Service.

3. Go to "Integrations" and then "Add New Integration". Give it a name and select the application "Nagios" from the dropdown menu.

4. Go to "Configure" under your integrations and copy the webhooks URL generated.

## In Nagios: 

### ON THE REMOTE HOST:

**1. Installing the Nagios plugins:**
	Move into the directory for downloads. If not make one.

```
$ mkdir ~/Downloads
$ cd ~/Downloads
```

Download the source code tarball of the Nagios plugins (visit http://www.nagios.org/downloads/ for links to the latest versions). At the time of writing, the latest stable version of the Nagios plugins was 2.1.1.

```
$ wget http://nagios-plugins.org/download/nagios-plugins-2.2.1.tar.gz
```

Extract the Nagios plugins from the folder.

```
$ tar xzf nagios-plugins-2.2.1.tar.gz
$ cd nagios-plugins-2.2.1
```

Compile and install the plugin.

```
$ ./configure
$ make
$ make install
```

Depending on the version of the plugins, the permissions on the plugin directory and the plugins may need to be fixed at this point. If so run the following commands:

```
$ useradd nagios
$ groupadd nagios
$ usermod -a -G nagios nagios
$ chown nagios.nagios /usr/local/nagios
$ chown -R nagios.nagios /usr/local/nagios/
```
**2. Installing xinetd:**
	
We will install xinetd using the following command. This may vary based on the OS.
	
```
$ apt-get install xinetd
```

**3. Installing the NRPE daemon:**
	
Download the source code tarball of the NRPE addon. Make sure you have downloaded the latest version.

```
$ cd ~/Downloads$ wget https://github.com/NagiosEnterprises/nrpe/releases/download/nrpe-   3.2.1/nrpe-3.2.1.tar.gz
```

Extract the tarball:

```
$ tar xzf nrpe-3.2.1.tar.gz
$ cd nrpe-nrpe-3.2.1 
```

Compile the NRPE addon:

```
$ ./configure$ make all
```

Install the NRPE plugin (for testing), daemon, and sample daemon configuration file.

```
$ make install
$ make install-config
```
If you want NRPE to run per-connection under inetd, xinetd, launchd, systemd, smf, etc. run the following command:

```
$ make install-inted
```

Make sure nrpe 5666/tcp is in your /etc/services file, if applicable. 
If you want to run NRPE all the time under init, launchd, systemd, smf, etc. run the following command:
```
$ make install-init
```

**4. Testing the NRPE daemon locally:**

It is time to see if things are working properly. Make sure the nrpe daemon is running:

```
$ netstat -at | egrep "nrpe|5666"
```

If the two lines below show up, then it means everything going good so far.

```
tcp    0  0 0.0.0.0:nrpe        0.0.0.0:*           LISTEN
tcp6   0  0 [::]:nrpe           [::]:*               LISTEN
``` 

Else, make sure that:
* You added the nrpe entry to your /etc/services file
* The only_from directive in the /etc/xinetd.d/nrpe file contains an entry for "127.0.0.1"
* xinetd is installed and started
* The appropriate line in /etc/inetd.conf has been uncommented
* Check the system log files for references about xinetd or nrpe and fix any problems that are reported.

Next, check to make sure the NRPE daemon is functioning properly. To do this, run the check_nrpe plugin that was installed for testing purposes.

```
$ /usr/local/nagios/libexec/check_nrpe -H localhost
```

You should see the line below:

```
NRPE v3.2.1
```

**5. Open firewall rules:**

If the server has a firewall running, you need to allow access to the NRPE port (5666) from the Nagios server. In Ubuntu, you would use the following commands:

```
$ iptables -I INPUT -p tcp -m tcp --dport 5666 -j ACCEPT
$ service iptables save
```

On other systems and other firewalls, check the documentation or have an administrator open the port.At this point, you are done installing and configuring NRPE on the remote host. Now it is time to install a component and make some configuration entries on your monitoring server.

### ON THE MONITORING HOST:

On the monitoring host (the machine that runs Nagios), you'll need to do just a few things:
* Install the check_nrpe plugin
* Create a Nagios command definition for using the check_nrpe plugin
* Create Nagios host and service definitions for monitoring the remote host

These instructions assume that you have already installed Nagios on this machine according to the quickstart installation guide. The configuration examples that are given reference templates that are defined in the sample localhost.cfg and commands.cfg filesthat get installed if you follow the quickstart.

**1. Installing the check_nrpe plugin:** 

Download the source code tarball of the NRPE addon (visit https://www.nagios.org/downloads/nagios-core-addons/ for links to the latest versions). At the time of writing, the latest version of NRPE was 3.2.1.$ 

```
Scd ~/Downloads
$ wget https://github.com/NagiosEnterprises/nrpe/releases/download/nrpe-   3.2.1/nrpe-3.2.1.tar.gz
```

Extract the source tarball.

```
$ tar xzf nrpe-3.2.1.tar.gz

$ cd nrpe-nrpe-3.2.1
```

Compile the NRPE addon:

```
$ ./configure$ make check_nrpe
```

Install the NRPE plugin

```
$ make install-plugin
```

**2. Test communication with the NRPE daemon:** 

Make sure the check_nrpe plugin can talk to the NRPE daemon on the remote host. Replace "192.168.0.1" in the command below with the IP address of the remote host that has NRPE installed. 

```
$ /usr/local/nagios/libexec/check_nrpe -H 192.168.0.1
```

Expected response:

```
NRPE v3.2.1
```

If the plugin returns a timeout error, check the following:
* Make sure there isn't a firewall between the remote host and the monitoring server that is blocking communication
* Make sure that the NRPE daemon is installed properly and running on the remote host
* Make sure the remote host doesn't have local firewall rules that prevent the monitoring server from talking to the NRPE daemon

**3. Creating a command definition:**

You'll need to create a command definition in one of your Nagios object configuration files in order to use the check_nrpe plugin. Open the sample commands.cfg file for editing.

```
$ vim /usr/local/nagios/etc/objects/commands.cfg
```

and add the following definition to the file:

```
define command{
	command_name check_nrpe
	command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
}
```

You are now ready to start adding services that should be monitored on the remote machine to the Nagios configuration.

**4. Creating host and service definitions:**

You'll need to create some object definitions in order to monitor the remote Linux/Unix machine. These definitions can be placed in their own file or added to an already existing object configuration file.

First, its best practice to create a new template for each different type of host you'll be monitoring. Let's create a new template for linux boxes.

```
define host{    
	name                     linux-box                 ;Name of this template    
	use                      generic-host              ;Inherit default values    
	check_period         	 24x7    
	check_interval        	 5    
	retry_interval           1    
	max_check_attempts  	 10    
	check_command     		 check-host-alive    
	notification_period   	 24x7   
	notification_interval 	 30    
	notification_options     d,r    
	contact_groups        	 admins    
	register                 0    						; DON’T REGISTER THIS - ITS A TEMPLATE
	}
```

Next, define a new host for the remote Linux/Unix box that references the newly created linux-box host template.
```
define host{
	use                 linux-box
	host_name    		remotehost    
	alias               Fedora Core 6    
	address         	192.168.0.1
	}
```
**5. Restarting Nagios:** Restart Nagios using one of the commands below, or whatever is appropriate on your server.
```
$ service nagios restart
$ systemctl restart nagios
$ svcadm disable nrpe && svcadm enable nrpe
$ /etc/rc.d/nrpe restart
```
### RUNNING THE ZENDUTY - NAGIOS INTEGRATION SOFTWARE

**1. Downloading the software:**

Download the software from https://github.com/Zenduty/zd-nagios.git

**2. Installing the software:**

Extract the source code.
```
$ tar xvf NagiosZendutyIntegration.tar.gz
$ cd NagiosZendutyIntegration.tar.gz
```
**3. Start Nagios Core:**

Start Nagios core using the same command used to restart it in the previous sections, replacing “restart” with “start”.

**4. Start the Zenduty Integration Software:**

Run the executable file to begin monitoring it. The webhook URL with your integration key must be passed as a parameter, as shown below. Replace the URL below with your own

```
$ ./zenduty https://www.zenduty.com/api/integration/nagios/49152724-ec1a-475c-91b5-18bf8e390d93/

```
And that’s it! You’re system is now being monitored by Nagios and any alerts will be communicated to your zenduty account
