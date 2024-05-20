# syntax=docker/dockerfile:1
ARG NODE_VERSION=21.7.3
ARG PNPM_VERSION=8.6.2

FROM node:${NODE_VERSION}-alpine

# Install curl for debugging
RUN apk add curl

##################
# MOST**** environment variables in compose.yaml for consistency
#
# This variable needs to be set at the build step
ENV VITE_API_GETDATA_URL=http://api.localhost/api/getdata

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN addgroup viteuser
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    --ingroup "viteuser" \
    viteuser


WORKDIR /usr/src/app

RUN chown -R viteuser:viteuser /usr/src/app

# Copy the rest of the source files into the image.
COPY . .

# Install dependencies then build the project
RUN npm install
RUN npm run build

# Run the application as a non-root user.
USER viteuser

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD npm run preview
