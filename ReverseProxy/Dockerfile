FROM nginx:1.19.7-alpine

# Add bash for boot cmd
RUN apk add bash

COPY --chown=nginx:nginx /ReverseProxy/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx /ReverseProxy/default.conf /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx /ReverseProxy/start.sh /app/start.sh

# set workdir
WORKDIR /app

##################
# All environment variables in compose.yaml for consistency
#
#ENV API_BASE_URL=http://fhircapstoneproject:5000
#ENV FRONTEND_BASE_URL=http://frontend:8080
#ENV DOCS_STATIC=/documentation/output/
#
## the domain that the services are hosted at
#ENV BASE_HOST=localhost

# permissions and nginx user for tightened security
RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
        chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chmod -R 755 /var/log/nginx; \
        chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && chown -R nginx:nginx /var/run/nginx.pid

EXPOSE 80

USER nginx

#CMD sleep 999
