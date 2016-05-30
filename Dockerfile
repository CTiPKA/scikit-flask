FROM dataquestio/ubuntu-base

MAINTAINER vtrulyaev “trulyaev@gmail.com”

ENV TERM=xterm
ENV LANG en_US.UTF-8

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]