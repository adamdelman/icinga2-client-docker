# icinga2

This repository contains the source for the [icinga2](https://www.icinga.org/icinga2/) [docker](https://www.docker.com) image.

It is only the **client side**. When used inside a privileged container, you'll be able to monitor the whole machine with this image.

For the **master node** consult [@jjethwa's docker image](https://github.com/jjethwa/icinga2/).

This image automatically configures the Icinga client up with the master Icinga node, using the provided API credentials.

Recommended execution is via `docker-compose`. There is too much stuff which has to be configured outside the container to run it via plain `docker run` but of course, it would be possible.

    wget https://raw.githubusercontent.com/adamdelman/icinga2-client-docker/master/docker-compose.yml
    $EDITOR docker-compose.yml
    docker-compose up

## Environment variables Reference

| Environmental Variable | Default Value          | Description |
| ---------------------- | ---------------------- | ----------- |
| `ICINGA2_MASTER_HOST`  | mon                    | The hostname of icinga2
| `ICINGA2_MASTER_FQDN`  | *$ICINGA2_MASTER_HOST* | If your icinga2 master certs' FQDN does not match the hostname, define this in addition. If you set `ICINGA2_MASTER_HOST` correctly, you should not worry about this. |
| `ICINGA2_API_USERNAME` | root                   | The Icinga API user used to create login tickets. |
| `ICINGA2_API_PASSWORD` | root                   | The Icinga API password used to create login tickets. |

## Volume Reference

All these folders are configured and able to get mounted as volume. The bottom ones are not quite neccessary.

| Volume | ro/rw | Description & Usage |
| ------ | ----- | ------------------- |
| /etc/icinga2 | rw | Icinga2 configuration folder |
| /var/lib/icinga2 | rw | Icinga2 Data |
| /var/log/icinga2 | rw | logfolder for icinga2 (not neccessary) |
| /var/log/supervisor | rw | logfolder for supervisord (not neccessary) |
| /var/spool/icinga2 | rw | spool-folder for icinga2 (not neccessary) |
| /var/cache/icinga2 | rw | cache-folder for icinga2 (not neccessary) |
