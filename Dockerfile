FROM debian:stretch

MAINTAINER Adam Delman

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -qy curl gnupg2 && curl https://packages.icinga.com/icinga.key | apt-key add -
RUN apt-get -qy upgrade \
     && apt-get -qy install --no-install-recommends \
          ethtool \
          icinga2 \
          monitoring-plugins \
          net-tools \
          procps \
          gnupg2 \
          python3 \
          python3-pip \
          python3-requests \
          smartmontools \
          snmp \
          strace \
          sysstat \
          vim \
          wget \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

ADD content /
RUN chmod +x /opt/setup/register_icinga_client.py

RUN mv /etc/icinga2/ /etc/icinga2.dist \
    && mkdir /etc/icinga2 \
    && chmod u+s,g+s \
        /bin/ping \
        /bin/ping6 \
        /usr/lib/nagios/plugins/check_icmp

EXPOSE 80 443 5665

ENTRYPOINT ["/opt/run"]
