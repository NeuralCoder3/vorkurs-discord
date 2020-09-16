# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8-slim-buster
# FROM ubuntu:18.04
FROM udsdepend/latex-python:latest

# RUN apt-get update && apt-get install -y gnupg
# RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E1DD270288B4E6030699E45FA1715D88E1DF1F24
# RUN echo 'deb http://ppa.launchpad.net/git-core/ppa/ubuntu trusty main' > /etc/apt/sources.list.d/git.list

# RUN apt-get update && apt-get install -y {git}

# RUN apt-get update && \
#     apt-get upgrade -y && \
RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y python3
RUN apt update && apt-get install -y python3-pip

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
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

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser


# CMD ["sh", "-c", "cd /storage/material && git pull"]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "discordbot.py"]
