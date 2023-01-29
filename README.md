# MQTT 2 Syslog

## (C)'2023 by Herby

howto:

 
copy:

`parameter/parameter_example.py to parameter/parameter.py `

and edit it


-----------
build:

`docker build -t mqtt2syslogger . `

run:

`docker-compose  up -d`

log:

`docker-compose logs -f`

DevSec:

`docker run --rm --mount type=bind,source="$PWD",target=/scan registry.fortidevsec.forticloud.com/fdevsec_sast:latest `
