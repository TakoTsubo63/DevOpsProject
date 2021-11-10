#!/bin/python3
from progress.bar import IncrementalBar
import requests
import os
import time
path = (os.path.expanduser('~'))
os.chdir(path+"/projectTerra/")
os.system("terraform init")
os.system("terraform apply -auto-approve")
os.chdir(path)
count = 60
num = 0
bar = IncrementalBar('pending...', max=count)
state = ""

def parsing(host_name, file_name):
    if line.find('"value') > 0:
                    global state, num
                    mas = line.split('"')
                    state = ""
                    num+=1
                    with open(file_name, 'w') as f3:
                        f3.write("["+host_name+"]" + '\n')
                        f3.write(mas[3]+'\n')
                        return mas[3]

while num != 3:
    with open('./projectTerra/terraform.tfstate', 'r') as f:
        for line in f:
            if state == "apache":
                os.chdir(path+"/apache")
                ip_apache = parsing("apache_server", "host_apache")
            elif state == "postgres":
                os.chdir(path+"/postgres")
                ip_postgres = parsing("postgres_server", "host_postgres")
                os.chdir(path+"/apache/roles/wordpress/files")
                os.system("cp wp-config1.php wp-config.php")
                st_line = "define( 'DB_HOST', '"
                end_line = "' );\n"
                with open('wp-config1.php', 'r') as f4, open('wp-config.php', 'w') as f12:
                    lines = f4.readlines()
                    for line in lines:
                        line = line.strip()
                        if line == "define( 'DB_HOST', 'database_host' );":
                            f12.write(st_line + ip_postgres + end_line)
                        else:
                            f12.write(line+"\n")
            elif state == "jenkins":
                os.chdir(path+"/ansibleProject")
                ip_tomcat = parsing("tomcat_server", "hosts")
            if line.find('instance_public_ip_apache') > 0:
                state = "apache"
            elif line.find('instance_public_ip_postgres') > 0:
                state = "postgres"
            elif line.find('instance_public_ip_jenkins') > 0:
                state = "jenkins"

try:
    r = requests.head('http://'+ip_tomcat+':8080')
    if  r.status_code == 200:
        print("")
        print("\033[6m\033[35m********************")
        print("Servers already run")
        print("********************\033[0m")

except Exception as exc:
    print("Server initializing...")
    for c in range(count):
        bar.next()
        time.sleep(1)

    os.system("echo ")
    os.chdir(path+"/postgres/")
    os.system("git add .")
    os.system('git commit -m "changed inventory"')
    os.system("git push")
    os.chdir(path+"/apache/")
    os.system("git add .")
    os.system('git commit -m "changed inventory"')
    os.system("git push")

bar.finish()
os.chdir(path+"/ansibleProject")
os.system("ansible-playbook main.yml --vault-password-file "+path+"/.ssh/pass")