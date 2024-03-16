FROM node:lts AS development

WORKDIR /react-app

COPY /FrontEnd/package.json /react-app/package.json
COPY /FrontEnd/package-lock.json /react-app/package-lock.json

RUN npm install

COPY /FrontEnd /react-app

# Compose sets $REACT-PORT=5173

CMD [ "npm", "start" ]

FROM development AS build

RUN npm run dev

FROM nginx:1.19.7-alpine

# Add bash for boot cmd
RUN apk add bash

# Add nginx.conf to container
COPY --chown=nginx:nginx nginx/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx nginx/start.sh /app/start.sh

# set workdir
WORKDIR /app

# permissions and nginx user for tightened security
RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
        chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chown -R nginx:nginx /usr/share/nginx/html && \
        chmod -R 755 /var/log/nginx; \
        chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && chown -R nginx:nginx /var/run/nginx.pid

# # Uncomment to keep the nginx logs inside the container - Leave commented for logging to stdout and stderr
# RUN mkdir -p /var/log/nginx
# RUN unlink /var/log/nginx/access.log \
#     && unlink /var/log/nginx/error.log \
#     && touch /var/log/nginx/access.log \
#     && touch /var/log/nginx/error.log \
#     && chown nginx /var/log/nginx/*log \
#     && chmod 644 /var/log/nginx/*log

USER nginx

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY --from=build /react-app/build .

CMD ["nginx", "-g", "'daemon off;'"]
