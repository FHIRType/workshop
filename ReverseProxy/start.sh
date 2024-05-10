#!/bin/bash
envsubst '$NGINX_API_BASE_URL$NGINX_FRONTEND_BASE_URL$BASE_HOST$DOCS_STATIC$SUBDOMAIN_API$SUBDOMAIN_DOCUMENTATION' < /etc/nginx/conf.d/default.conf > /tmp/_default.conf && \
mv -f /tmp/_default.conf /etc/nginx/conf.d/default.conf && \
nginx -g 'daemon off;'
