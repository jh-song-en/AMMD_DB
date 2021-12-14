# AMMD DB and Platform Manual



## Content

1. [Installation](#installation)
    1. [Docker installation](#docker-installation)
    2. [Server initiation](#server-initiation)
    3. [Port Forwarding](#port-forwarding)
2. [User Management](#user-management)

## Installation

    Step by step information of the installation are in this block, You can skip the explanation

### Docker installation
First, we need to download the Docker to be able to build virtual environment of the AMMD-DB server.

    Download Docker of your OS version. (Windows might have to reboot the system after the download)

You can download Docker from [here](https://www.docker.com/get-started) or docker.com .
![image](https://user-images.githubusercontent.com/72897259/141220925-86e777e5-8942-4297-8745-4d6e4b786462.png)

### Server initiation
You can either download the source code from this git, or download the zip file [here](https://drive.google.com/file/d/10pGwH0_15fONszIxSZcR4is7Cao_5Sx4/view?usp=sharing)

    download AMMD_DB initator.zip file to your device, and unzip the file.
    Open AMMD_DB_initiator.exe
  
You can initiate the server by setting port numbers and MySQL root password. <br>
(For the security purpose, Port numbers and password should be set by the server manager.) 

    input MySQL Port, SFTP port into the edit. 
    
![image](https://user-images.githubusercontent.com/72897259/145781935-a98c395d-09ac-4781-af98-08488cb6fd05.png)

    Click the Initiate Server button 
    (The console below will appear and disappear on the screen)
    Press OK button

![image](https://user-images.githubusercontent.com/72897259/145782092-5883612a-df20-4545-8654-4de9e1766fac.png)

Now, your server is running. You can check your server status on Docker desktop app.

![image](https://user-images.githubusercontent.com/72897259/145782179-5d5e0a1a-7eec-4bac-92da-8876493bdb2d.png)

### Port Forwarding
The server is now installed in your system. __But, you can only use the server with the system that are using the same router (wifi-machine) for now.__ To open the access from the outside of your facility, (routher) you need to forward the port from your router to your computer.

    Check your PC's local ip, 

Click [here](https://www.avast.com/c-how-to-find-ip-address#gref) to find out how.

    Check your router's manufacturer, and search google for the "(manufacturer's name) portforwarding". 
    
Each router has different setting environment. Here are some examples of port forwarding. The image below is a guide sample for IPtime router.
[Here](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/) is general guide to multiple router brands.
#### IPtime
![image](https://user-images.githubusercontent.com/72897259/145784794-554eaad6-9f53-47cf-823e-534c3de234b5.png)


## User Management
After running the server, you can manage the user by user tab.
    
    Press User Button.
    
![image](https://user-images.githubusercontent.com/72897259/145783172-e41ad2d6-3c69-4516-a0c6-180358e6aa79.png)

![image](https://user-images.githubusercontent.com/72897259/145783477-194d6265-c4ed-48b2-8dae-8a5db11b3d50.png)

    By clicking the - button, you can delete the selected user
    By clicking the + button, you can create new user
    By doubleclicking the user, you can manipulate user's status
    
```Manager```       user can update, upload, delete, download the data and manipulate the database.<br>
```Researcher```    user can update, upload, and download the data.<br>
```Visitor```       user can only view and download the data from the database.



