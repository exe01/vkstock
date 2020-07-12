FROM node:12.8.1-stretch

RUN npm install -g @vue/cli@3.10.0

# Create and define the node_modules's cache directory.
RUN mkdir /usr/src/cache
WORKDIR /usr/src/cache

# Install the application's dependencies into the node_modules's cache directory.
COPY package.json ./
RUN npm install

WORKDIR /app
COPY . /app
VOLUME ["/app"]

CMD ["/bin/bash", "./entrypoint.sh"]
