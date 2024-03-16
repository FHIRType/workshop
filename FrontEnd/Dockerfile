FROM node:lts AS development

WORKDIR /react-app

COPY package.json /react-app/package.json
COPY package-lock.json /react-app/package-lock.json

RUN npm install

COPY . /react-app

# Compose sets $REACT-PORT=5173

CMD [ "npm", "run", "dev" ]