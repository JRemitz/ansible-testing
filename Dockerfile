FROM centos:7
MAINTAINER “Jake Remitz” <Jake.Remitz@gmail.com>
ENV container docker
RUN /bin/bash -c "yum -y update; yum clean all; \
yum -y install systemd; yum clean all; \
yum -y install epel-release; \
yum -y install iproute; \
yum -y install python2-pip; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*; \
rm -f /etc/systemd/system/*.wants/*; \
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*; \
rm -f /lib/systemd/system/anaconda.target.wants/*; \
rm -rf /tmp/*; rm -rf /var/cache/yum;"
VOLUME [ “/sys/fs/cgroup” ]
CMD [“/usr/sbin/init”]
