# AMMD DB Manual



## Content
1. [Introduction](#introduction)
    1. [Docker](#docker)
    2. [MySQL](#mysql)
    3. [SFTP](#sftp)
2. [Installation](#installation)
    1. [Docker installation](#docker-installation)
    2. [Server initiation](#server-initiation)
    3. [Port forwarding](#port-forwarding)
3. [User Management](#user-management)
    1. [User addition](#user-addition)
    2. [User update](#user-update)
    3. [User delete](#user-delete)

## Introduction
### Docker
Docker is a platform that runs the software in the package called the container. 
The container offers a stable virtual environment that contains the software, enabling easy deployment and build of the server. 
It uses less resource and even quicker than using virtual machines.

![image](https://user-images.githubusercontent.com/72897259/146742546-49e28e4f-906e-45da-b26a-9ba4e62d4c0f.png)


AMMD DB contains two servers: MySQL server and SFTP server.
To run the server, some software has to be downloaded and settings must be done.
However, downloading server components separately is time-consuming and problematic 
since the server software can crash with the existing software.
Therefore, the Docker is used to build AMMD DB without setting up the server with a few simple steps by using the ```AMMD_DB_initiator.exe```.

The container is a temporal environment, which means that the data produced or saved will be gone when the container is down.
Therefore, the data which needs to be preserved needs to be connected to the host OS. (the main operating system)
This process is called a volume mount, and the required volume setting is contained in the ```AMMD_DB_initiator.zip``` file, which will be presented on the [Server initiation](#server-initiation) section.

![image](https://user-images.githubusercontent.com/72897259/146746241-b99ca72d-783d-4641-b870-e20fdd7552bb.png)

As shown in the image above, the two folders (```mysql```, ```sftp``` folder) are the volume folder that will be mounted to the container. Every data uploaded to the database will be saved to these files. Therefore, the whole data of the database will be backed-up by backing up these two files (preferably the whole AMMD_DB_initiator directory). <br>
(The file system_config is recommended not to be modified)


![image](https://user-images.githubusercontent.com/72897259/146750079-a45b6244-4a10-4357-b715-922cd1c912eb.png)
<br>The image above shows the structure of the AMMD-DB server. Each square element represents a database table, and each tree-view represents the data folder of the property.
Addition or modification of the characterization database are managed through the AMMD_DB_Manager app.



### MySQL
MySQL is an RDBMS (Relational database management system) that stores and manages data in a tabular form. 
The metadata, experimental condition of the thin-film deposition, or the characterization process is stored in the MySQL server on the corresponding table.
Each metadata is saved as a single row in the table. 

MySQL has a concept of primary key and foreign key. The primary key is the value that uniquely identifies each row in the table. Every data stored in the MySQL table must have and can have only one primary key column. The foreign key is the value that references the primary key of the other table, which shows the relationship between the two tables.

For example, when the synthesized sample metadata (deposition temperature, target composition, Argon pressure, and more) are uploaded to the MySQL server, the metadata will be saved as a single row with the primary key (id_sample) filling each column of the Sample table. Likewise, the characterization process' metadata is stored the same way. The primary key (id_property) of the characterization metadata is also assigned, and the foreign key (id_sample) is labeled to this metadata to identify which sample this characterization is for. 


### SFTP
SFTP (SSH File Transfer Protocol) is a file transfer protocol that uses the SSH connection. SSH connection encrypts the data by a two-key method called a handshake. 
The transferred file through the network is encrypted, preventing the data leak through the unsecured network.
The data produced by the characterization process are stored in the file server with a familiar form of a directory separated by the process, as shown in the image above.

The file or folder (differs by the data type of the characterization process) names in the directory are labeled by the primary key of the sample and characterization table ([id_sample]-[id_ property]), keeping the relationship between the data in the file server and the metadata.
The format needs to be pre-defined by the research group to establish standardization. 


## Installation

[![IMAGE ALT TEXT](https://user-images.githubusercontent.com/72897259/149836796-6a98b8d6-b6ad-4721-88ea-4796644cfe44.png)](https://www.youtube.com/watch?v=klupDXRGA1M "Video Title")


    Step by step information of the installation are in this block, You can skip the explanation.

### Docker installation
First, we need to download the Docker to be able to build virtual environment of the AMMD-DB server.

    Download Docker of your OS version. (Windows might have to reboot the system after the download)

You can download Docker from [here](https://www.docker.com/get-started) or docker.com .
![image](https://user-images.githubusercontent.com/72897259/146742887-aa0f43aa-4cc3-46cf-917e-4fa34929f7ea.png)

Then install WSL 2.

    Go to https://aka.ms/wsl2kernel
    and download the WSL2 Linux kernel from step 4.

![image](https://user-images.githubusercontent.com/72897259/148879104-a6531763-2c25-4a8c-b497-53886931f42e.png)


### Server initiation
You can either download the source code from this git, or download the zip file [here](https://drive.google.com/file/d/11yxfydTJpb3joSHFeTdzLHlHFP-LfPwB/view?usp=sharing)

    download AMMD_DB initator.zip file to your device, and unzip the file.
    Open AMMD_DB_initiator.exe.
  
You can initiate the server by setting port numbers. <br>
(For the security purpose, Port numbers should be set by the server manager.) 

#### What is port?
Three elements are required for the server connection: IP address, port number, and user information (id, password). IP address locates the server in the network. The port determines which process or application a message should be delivered. Finally, user information verifies if the user has the authentication to use the service in the server.

For example, if the MySQL port is set as 8806 and the SFTP port is set as 8802, the IP address will be the same since both applications are running on the same server. However, if the user requests through the 8806 port, the server will answer with the MySQL response, and it will respond with SFTP if the connection is through the 8802 port. 

Therefore, the port must be allocated to make the right connection and recommended to be set by the manager for security purposes.



    input MySQL Port, SFTP port into the edit. 
    
![image](https://user-images.githubusercontent.com/72897259/146760382-045402c8-c330-41dd-ae0e-b8064a3a53fa.png)

    Click the Initiate Server button.
    (The console below will appear and disappear on the screen.)
    Press OK button.

![image](https://user-images.githubusercontent.com/72897259/145782092-5883612a-df20-4545-8654-4de9e1766fac.png)
![image](https://user-images.githubusercontent.com/72897259/146762724-0ff96855-cf59-404e-a07c-6dec260e79cb.png)


Now, your server is running. The applicathion will show you the server status and the connected ports. You can also check your server status on Docker desktop app.

![image](https://user-images.githubusercontent.com/72897259/145782179-5d5e0a1a-7eec-4bac-92da-8876493bdb2d.png)

### Port forwarding
The server is now installed in your system. __But, you can only use the server with the system using the same router (wifi-machine) for now.__ 

It is because the router has its own ports, and this port needs to be connected to your desktop device's port.

__If your network is in the university or the institution, you need to contact the IT team or the network office of your facility since there can be an additional network control of your facility.__

To open the access from the outside of your facility (router), you need to forward the port from your router to your computer.

    Check your PC's local ip.

Click [here](https://www.avast.com/c-how-to-find-ip-address#gref) to find out how.

    Check your router's manufacturer, and search google for the '(manufacturer's name) portforwarding'. 
    
Each router has different setting environment. Here are some examples of port forwarding. The image below is a guide sample for IPtime router.
[Here](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/) is general guide to multiple router brands.
#### IPtime
![image](https://user-images.githubusercontent.com/72897259/145784794-554eaad6-9f53-47cf-823e-534c3de234b5.png)


## User Management
After running the server, you can manage the user by user tab.
    
    Press User button.
    
![image](https://user-images.githubusercontent.com/72897259/145783172-e41ad2d6-3c69-4516-a0c6-180358e6aa79.png)

![image](https://user-images.githubusercontent.com/72897259/145783477-194d6265-c4ed-48b2-8dae-8a5db11b3d50.png)

    By clicking the - button, you can delete the selected user.
    By clicking the + button, you can create a new user.
    By double-clicking the user, you can manipulate the user's status and password.

The user permission is described below.
```Manager```       user can update, upload, delete, download the data and manipulate the database.<br>
```Researcher```    user can update, upload, and download the data.<br>
```Visitor```       user can only view and download the data from the database.<br>

There are conditions of the password:
<br>8 to 20 characters long.
<br>1 uppercase & 1 lowercase character.
<br>1 number.
<br>1 Symbolic character. (@$!#%*?&)<br>


__Since the server restarts when the user is generated, it is recommended to press ```Save and Restart``` button after the user management is done.__
(If you want to add, delete, modify multiple users, confirm them all and press ```Save and Restart``` button at the end. 

### User addition
![image](https://user-images.githubusercontent.com/72897259/146767327-797a807a-7f59-45a0-90b2-77a3ff8020e8.png)

    Click the + button to create the new user.
    Insert ID, Password and select the user's permission.
    Click confirm to add the user. (At this step, the user is not generated yet)
    Press Save and Restart to confirm every change.
    
### User update
![image](https://user-images.githubusercontent.com/72897259/146768825-0775facf-14c4-45b2-b0da-c1b461d44850.png)

    Doubleclick the id which you want to update.
    If you want to change the password, fill in the New PW and PW confirm.
    If you want to change the authentication, check the desired authentication.
    Click confirm to add the user. (At this step, the user is not generated yet)
    Press Save and Restart to confirm every change.
    
### User delete
![image](https://user-images.githubusercontent.com/72897259/146769192-14af5eaf-efe0-403b-a1b0-96dd0974687b.png)

    Click the id which you want to delete.
    Click the - button to delete the user.
    Press Save and Restart to confirm every change.
