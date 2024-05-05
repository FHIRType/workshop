#!/bin/bash
envsubst '$API_BASE_URL$FRONTEND_BASE_URL$BASE_HOST' < /etc/nginx/conf.d/default.conf > /tmp/_default.conf && \
mv -f /tmp/_default.conf /etc/nginx/conf.d/default.conf && \
nginx -g 'daemon off;'
