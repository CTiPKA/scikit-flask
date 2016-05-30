FROM dataquestio/ubuntu-base

MAINTAINER vtrulyaev “trulyaev@gmail.com”

# Export env settings
ENV TERM=xterm
ENV LANG en_US.UTF-8

RUN apt-get update -y
RUN apt-get install build-essential -y

ADD apt-packages.txt /tmp/apt-packages.txt
RUN xargs -a /tmp/apt-packages.txt apt-get install -y

RUN pip install virtualenv
RUN /usr/local/bin/virtualenv /opt/ds --distribute

ADD /requirements/ /tmp/requirements

RUN /opt/ds/bin/pip install -r /tmp/requirements/pre-requirements.txt
RUN /opt/ds/bin/pip install -r /tmp/requirements/requirements.txt

RUN useradd --create-home --home-dir /home/ds --shell /bin/bash ds
RUN chown -R ds /opt/ds
RUN adduser ds sudo

ADD run_flask.sh /home/ds
ADD app.py /home/ds
RUN chmod +x /home/ds/run_flask.sh
RUN chown ds /home/ds/run_flask.sh

RUN usermod -a -G sudo ds
RUN echo "ds ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER ds

ENV HOME=/home/ds
ENV SHELL=/bin/bash
ENV USER=ds
VOLUME /home/ds
WORKDIR /home/ds

CMD ["/home/ds/run_flask.sh"]