#!/bin/bash
cd /home/ec2-user/EMOCICD/
source environment/bin/activate
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]