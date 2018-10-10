FROM base/archlinux

MAINTAINER Adam Delman


RUN \
    sed -i 's/^SigLevel.*/SigLevel = Never/' /etc/pacman.conf && \
    locale-gen en_US.UTF-8 && \
    pacman -Syyu --noconfirm && \
    pacman -S --noconfirm reflector && \
    reflector --verbose --country 'United States' -l 100 --sort rate --save /etc/pacman.d/mirrorlist

RUN \
    pacman -Syyu --noconfirm && \
    pacman -S --noconfirm \
          ethtool \
          monitoring-plugins \
          base-devel \
          net-tools \
          procps \
          gnupg2 \
          python \
          python-requests \
          smartmontools \
          strace \
          sysstat \
          vim \
          wget

ADD content/ /
RUN chmod +x /opt/setup/setup-aur
RUN /opt/setup/setup-aur docker
RUN sudo -u docker trizen --needed --noprogressbar --noedit --noconfirm -S icinga2
RUN pacman -Scc

RUN chmod +x /opt/setup/register_icinga_client.py

EXPOSE 80 443 5665

ENTRYPOINT ["/opt/run"]
