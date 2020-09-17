# For more information, please refer to https://aka.ms/vscode-docker-python
FROM udsdepend/latex-python:latest

RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y python3
RUN apt update && apt-get install -y python3-pip


# Alternative: use compose with single selenium container
# and remote selenium browser in python

RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99
RUN pip install selenium==3.8.0


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# I should not do this
# the keys are added to the docker container
RUN mkdir -p /home/appuser/.ssh
ADD key/id_ed25519 /home/appuser/.ssh/id_rsa
ADD key/id_ed25519.pub /home/appuser/.ssh/id_rsa.pub
RUN chmod -R 777 /home/appuser/.ssh
RUN echo "Host vorkurs.cs.uni-saarland.de\n\tStrictHostKeyChecking no\n" >> /home/appuser/.ssh/config

RUN useradd appuser && chown -R appuser /app
USER appuser


CMD ["python3", "discordbot.py"]
