#!/bin/bash
cd /home/ec2-user/EMOCICD/
source environment/bin/activate
 {

# collecting static files
python manage.py collectstatic --noinput;
# log which migrations have already been applied
python manage.py showmigrations;
# migrate the rest
python manage.py migrate --noinput;
# another command to create a superuser (write your own)
}