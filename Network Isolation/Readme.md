Network Isolation

The script is written following the Certification Framework requirement. 

Input configuration
The input configuration is a .ini file parsed via ConfigParser (for now. This behaviour will be changed with the next testAgent release)

[0]
MIN_PORT=

MAX_PORT=

TARGET_IP=

TARGET_UUID=
[1]

OS_AUTH_URL=

OS_TENANT_NAME=

OS_TENANT_ID=

OS_USERNAME=

OS_PASSWORD=

OS_REGION_NAME=

[2]

ENABLE_TCP_SCAN=

ENABLE_UDP_SCAN=

Explanation:
*   0 - General settings
    -   MIN_PORT
    -   MAX_PORT
        +   These two parameters define a range of ports to be scanned. They can be set as MIN_PORT=1 and MAX_PORT=65535 to cover the full port range.
    -   TARGET_IP
        +   The target IP address for the HoneyPot VM (we left the creation to the user)
    -   TARGET_UUID
        +   The OpenStack's UUID of the target VM
*   1 - Authentication
    -   OS_AUTH_URL
    -   OS_TENANT_NAME
    -   OS_TENANT_ID
    -   OS_USERNAME
    -   OS_PASSWORD
    -   OS_REGION_NAME
        +   These are the parameters to authenticate against Openstack APIs
*   2 - NMap configuration
    -   ENABLE_TCP_SCAN
        +   This enables TCP scan. 1=True
    -   ENABLE_UDP_SCAN
        +   This enables UDP scan. 1=True. Requires Root.
    -   TCP_SYN_SCAN
        +   This enables SYN scan. 1=True. Requires Root.

    UDP SCAN and TCP SYN SCAN cause the test to run slower.

To run the script type:
    
    $python sgnetwork.py --input config.cfg
