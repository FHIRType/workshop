# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG NODE_VERSION=21.7.3
ARG PNPM_VERSION=8.6.2

FROM node:${NODE_VERSION}-alpine

# Use production node environment by default.
ENV NODE_ENV="production"
ENV VITE_API_BASE_URL="http://fhircapstoneproject:5000/api/getdata"

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

RUN npm install

# Run the application as a non-root user.
USER viteuser

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD npm run preview
#CMD sleep 99999