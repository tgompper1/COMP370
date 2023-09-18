#### Tess Gompper 260947251
### Set up MariaDB
1. SSH into Computer Cat:  
        `ssh -i "tess370.pem" ubuntu@ec2-13-59-227-103.us-east-2.compute.amazonaws.com`  
2. Update and install MariaDB:  
        `sudo apt update`  
        `sudo apt install mariadb-server`
3. Start MariaDB and follow secure installation prompts:  
        `sudo systemctl start mariadb.service`  
        `sudo mysql_secure_installation`
4. Edit Port and bind-address:
    1. In my.cnf:
                `vi /etc/mysql/my.cnf`  
                Set `port=6002`  
                Add  `[mysqld]`  
                     `port = 6002`  
                     `bind-address = 0.0.0.0`
    2. In 50-server.cnf:  
                `vi /etc/mysql/mariadb.conf.d/50-server.cnf`  
                Set `bind-address = 0.0.0.0`
5. Restart and check status:  
        `sudo service mysql restart`
        `sudo systemctl status mariadb`
6. Check port setting with MariaDB:
        `sudo mariadb`  
        `show variables like 'port';`  
7. Add Inbound security rule for port `6002` in AWS EC2 instance

### Create New database and user
1. Create the database:  
        `create database comp_370`
2. Create User:  
        `CREATE USER 'comp370'@'%' IDENTIFIED BY '$ungl@ss3s';`
3. Grant permissions:  
        `GRANT ALL PRIVILEGES ON comp370_test.* TO 'comp370'@'%';`

### Trying it with Dbeaver
1. Database -> New Database Connection
2. Set serverhost to EC2 instance IP 
3. Set Port to `6002`
4. Enter username, database and password

