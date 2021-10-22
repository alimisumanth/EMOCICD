#!/bin/bash
cd /home/ec2-user/EMOCICD/
source environment/bin/activate
supervisord -c supervisord.conf