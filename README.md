# AMMD DB and Platform Manual



## Content

1. [Introduction](#introduction)<br>
    1. [MySQL](#mysql)<br>
    2. [SFTP](#sftp)<br>
    3. [Docker](#docker)
2. [Installation](#installation)

## Introduction

### MySQL
### SFTP
### Docker
## Installation

    Step by step information of the installation are in this block, You can skip the explanation

### Docker installation    
First, we need to download the Docker to be able to build virtual environment of the AMMD-DB server.

    Download Docker of your OS version. (Windows might have to reboot the system after the download)

You can download Docker from [here](https://www.docker.com/get-started) or docker.com .
![image](https://user-images.githubusercontent.com/72897259/141220925-86e777e5-8942-4297-8745-4d6e4b786462.png)

### server initiation
You can either download the source code from this git, or download the zip file [here](https://drive.google.com/file/d/10pGwH0_15fONszIxSZcR4is7Cao_5Sx4/view?usp=sharing)

    download AMMD_DB initator.zip file to your device, and unzip the file.
    Open AMMD_DB_initiator.exe
  
You can initiate the server by setting port numbers and MySQL root password. (For the security purpose, Port numbers and password should be set by the server manager.) 

    input MySQL Port, SFTP port, MySQL password into the edit.











### Port Forwarding
The server is now installed in your system. __But, you can only use the server with the system that are using the same router (wifi-machine) for now.__ To open the access from the outside of your facility, (routher) you need to forward the port from your router to your computer.

    Check your PC's internal ip, 

    Check your router's manufacturer, and search google for the "(manufacturer's name) portforwarding". 
    
Each router has different setting environment. Here are some examples of portforwarding.

#### IPtime
![image](https://user-images.githubusercontent.com/72897259/141226782-48b88d6a-baf6-4f4b-811a-49e878a0ca76.png)

