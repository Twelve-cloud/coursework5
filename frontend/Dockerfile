# 1 layer
FROM node:20.5.1-alpine3.18

WORKDIR /app
# 2 layer
COPY package.json /app

# 3 layer
RUN npm install --legacy-peer-deps

# 4 layer
COPY . /app

# 5 layer
RUN chmod +x entrypoint.sh
EXPOSE 5000
