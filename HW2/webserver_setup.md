#### Tess Gompper 260947251
### Set Up EFS and EC2
1. Create an EFS file system: https://us-east-2.console.aws.amazon.com/efs/home?region=us-east-2#/file-systems
2. Create EC2 instance and mount to EFS
    1. Choose Amazon Linux 
    2. In Network settings, set subnet to one available in default zone
    3. Configure storage to add a file system which is the EFS
3. Within security settings, add a rule to listen to port `8008`

### Set up Apache
1. Connect to instance and install Apache web server:  
        `sudo yum -y install httpd`
2. Start the service:  
        `sudo service httpd start`
3. Change port to `8008`:  
        `sudo vi /etc/httpd/conf/httpd.conf`
4. Restart the service:  
        `sudo service httpd restart`

    
### Mount EFS file system
1. Mount EFS file system to html dir:  
        `sudo mount -t efs efs-id:/ /var/www/html/`
2. Adjust ownership and access:  
        `sudo chown  ec2-user html`  
        `sudo chmod -R o+r html`
3. Change directory to the mount point:  
        `cd /var/www/html/`
4. `echo "hello" > comp370_hw2.txt`

### Test it
Go to:  http://3.135.219.230:8008/comp370_hw2.txt



