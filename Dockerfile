
FROM jordan/icinga2

MAINTAINER Adam Delman

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -qy curl gnupg2 && curl https://packages.icinga.com/icinga.key | apt-key add -
ADD content/etc/sources.list.d/icinga2.list /etc/sources.list.d/icinga2.list

RUN apt update && \
    apt-get -qy upgrade && \
    apt-get -qy install --no-install-recommends -o Dpkg::Options::="--force-confnew" \
          ethtool \
          icinga2 \
          monitoring-plugins \
          nagios-nrpe-plugin \
          nagios-plugins-contrib \
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

ADD content/etc/sudoers.d/icinga2 /etc/sudoers.d/icinga2
ADD content/opt/setup/register_icinga_client.py /opt/setup/register_icinga_client.py
ADD content/opt/run /opt/run

RUN chmod +x /opt/setup/register_icinga_client.py

EXPOSE 80 443 5665

ENTRYPOINT ["/opt/run"]
