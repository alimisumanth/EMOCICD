#!/bin/bash
cd /home/ec2-user/EMOCICD/
source environment/bin/activate
 {
  cd ~ && wget https://www.sqlite.org/2020/sqlite-autoconf-3320100.tar.gz && tar xvfz sqlite-autoconf-3320100.tar.gz && cd sqlite-autoconf-3320100 && ./configure && make && make install
cd /home/ec2-user/EMOCICD/
sudo pip3 install -r requirements.txt
# collecting static files
sudo python3 manage.py collectstatic --noinput;
# log which migrations have already been applied
sudo python3 manage.py showmigrations;
# migrate the rest
sudo python3 manage.py migrate --noinput;
# another command to create a superuser (write your own)
}