### Using IHS and a the Plugin configuration with containers outside of Kubernetes

The plugin file cannot be updated automatically like in Liberty, so it is important to update the file for all the possible hosts and ports that will be used.  A single instance of the plugin file can be downloaded from the WAS Administration Console (port 9043), and can be modified by hand.  

1. [Install](https://www.ibm.com/docs/en/ibm-http-server/9.0.5?topic=archive-installing-http-server-from) IHS and the Plugin
2. Create the necessary directories under the Plugin directory.  In this case I am creating directories called `container` and that reference will be used in the plugin itself.
```
mkdir plugin/config/container
mkdir plugin/logs/container
```
3. Copy the plugin file from one of the WAS running instances to `plugin/config/container` as plugin-cfg.xml.
4. Update the file and chain all the directories to the correct location on your system.
5. For each container instance create another `<Server>` section and change the hostname and ports to the values on your system.
6. Change the `Name` field in the `<Server>` section for each container.
7. Add another `Server Name` entry under `PrimaryServers` with the name from step 6.

Example:
```
        <Server ConnectTimeout="5" ExtendedHandshake="false"
            MaxConnections="-1" Name="DefaultNode01_server1_0"
            ServerIOTimeout="900" WaitForContinue="false">
            <Transport ConnectionTTL="28" Hostname="lovecraft"
                Port="19080" Protocol="http"/>
            <Transport ConnectionTTL="28" Hostname="lovecraft"
                HostnameAlias="lovecraft" Port="19443" Protocol="https">
                <Property Name="keyring" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.kdb"/>
                <Property Name="stashfile" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.sth"/>
            </Transport>
        </Server>

        <PrimaryServers>
            <Server Name="DefaultNode01_server1_1"/>
        </PrimaryServers>
```

Adding two new servers:
```
        <Server ConnectTimeout="5" ExtendedHandshake="false"
            MaxConnections="-1" Name="DefaultNode01_server1_0"
            ServerIOTimeout="900" WaitForContinue="false">
            <Transport ConnectionTTL="28" Hostname="lovecraft"
                Port="19080" Protocol="http"/>
            <Transport ConnectionTTL="28" Hostname="lovecraft"
                HostnameAlias="lovecraft" Port="19443" Protocol="https">
                <Property Name="keyring" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.kdb"/>
                <Property Name="stashfile" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.sth"/>
            </Transport>
        </Server>

        <Server ConnectTimeout="5" ExtendedHandshake="false"
            MaxConnections="-1" Name="DefaultNode01_server1_1"
            ServerIOTimeout="900" WaitForContinue="false">
            <Transport ConnectionTTL="28" Hostname="lovecraft"
                Port="19081" Protocol="http"/>
            <Transport ConnectionTTL="28" Hostname="lovecraft"
                HostnameAlias="lovecraft" Port="19444" Protocol="https">
                <Property Name="keyring" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.kdb"/>
                <Property Name="stashfile" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.sth"/>
            </Transport>
        </Server>

        <Server ConnectTimeout="5" ExtendedHandshake="false"
            MaxConnections="-1" Name="DefaultNode01_server1_2"
            ServerIOTimeout="900" WaitForContinue="false">
            <Transport ConnectionTTL="28" Hostname="another.host"
                Port="19080" Protocol="http"/>
            <Transport ConnectionTTL="28" Hostname="another.host"
                HostnameAlias="another.host" Port="19443" Protocol="https">
                <Property Name="keyring" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.kdb"/>
                <Property Name="stashfile" Value="/opt/IBM/WebSphere/Plugins90/config/container/plugin-key.sth"/>
            </Transport>
        </Server>

        <PrimaryServers>
            <Server Name="DefaultNode01_server1_0"/>
            <Server Name="DefaultNode01_server1_1"/>
            <Server Name="DefaultNode01_server1_2"/>
        </PrimaryServers>
```

Of course the web server needs to be setup with configs:
```
LoadModule was_ap24_module plugin/bin/64bits/mod_was_ap24_http.so
WebSpherePluginConfig plugin/config/container/plugin-cfg.xml
```
