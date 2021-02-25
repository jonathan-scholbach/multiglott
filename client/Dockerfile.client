FROM node:12.2.0-alpine

WORKDIR /client
ENV PATH /client/node_modules/.bin:$PATH

COPY package.json /client/package.json

RUN npm install
COPY . .

RUN npm run build
