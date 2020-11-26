FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get -y update \
    && apt-get install curl google-chrome-stable nodejs -y 

RUN npm install pm2@latest -g

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

CMD pm2 start src/main.py --restart-delay=2000; sleep 3650d
