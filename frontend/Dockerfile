FROM node:lts-alpine

COPY package*.json ./
RUN npm install --silent
CMD npm run serve

COPY . .

WORKDIR .