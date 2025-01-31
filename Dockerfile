FROM nikolaik/python-nodejs:python3.10-nodejs20-slim


WORKDIR /app

# Install Debian software needed by MetaGPT and clean up in one RUN command to reduce image size
RUN apt update &&\
    apt install -y libgomp1 git chromium fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends &&\
    apt clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

ENV CHROME_BIN="/usr/bin/chromium" AM_I_IN_A_DOCKER_CONTAINER="true"
# Install Mermaid CLI globally
ENV CHROME_BIN="/usr/bin/chromium" \
    puppeteer_config="/app/config/puppeteer-config.json"\
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD="true"

RUN npm install -g @mermaid-js/mermaid-cli &&\
    npm cache clean --force

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt
COPY ./app .
ENV CONFIG_PATH=/app/config/config2.yaml

# Добавляем аргумент сборки
ARG PORT

CMD ["python", "main.py"]