# syntax=docker/dockerfile:1
FROM python:3.11.7-alpine

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add curl

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R nonroot:nonroot /var/log/flask-app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ARG FLASK_APP=FhirCapstoneProject/swaggerUI.app
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

CMD ["flask", "run"]

#       # OLD IMPLEMENTATION, DEV ONLY
#       ARG PYTHON_VERSION=3.11
#       FROM python:${PYTHON_VERSION} as base
#
#       # Prevents Python from writing pyc files.
#       ENV PYTHONDONTWRITEBYTECODE=1
#
#       # Keeps Python from buffering stdout and stderr to avoid situations where
#       # the application crashes without emitting any logs due to buffering.
#       ENV PYTHONUNBUFFERED=1
#
#       WORKDIR /app
#
#       # Create a non-privileged user that the app will run under.
#       # See https://docs.docker.com/go/dockerfile-user-best-practices/
#       ARG UID=10001
#       RUN addgroup appuser
#       RUN adduser \
#           --disabled-password \
#           --gecos "" \
#           --home "/nonexistent" \
#           --shell "/sbin/nologin" \
#           --no-create-home \
#           --uid "${UID}" \
#           --ingroup "appuser" \
#           appuser
#
#       # Download dependencies as a separate step to take advantage of Docker's caching.
#       # Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
#       # Leverage a bind mount to requirements.txt to avoid having to copy them into
#       # into this layer.
#       COPY FhirCapstoneProject/requirements/ FhirCapstoneProject/requirements/
#       RUN --mount=type=cache,target=/root/.cache/pip \
#           --mount=type=bind,source=FhirCapstoneProject/requirements/prod.txt,target=FhirCapstoneProject/requirements/prod.txt \
#           python -m pip install -r FhirCapstoneProject/requirements/prod.txt
#
#       RUN mkdir /app/logs
#       RUN chown -R appuser:appuser /app/logs
#
#       # Switch to the non-privileged user to run the application.
#       USER appuser
#
#       # Copy the source code into the container.
#       COPY FhirCapstoneProject FhirCapstoneProject
#       COPY FhirCapstoneProject/wsgi.py wsgi.py
#
#       # Expose the port that the application listens on.
#       EXPOSE 5000
#
#       # Run the application.
#       CMD gunicorn --preload 'wsgi' --bind=0.0.0.0:5000
#
######################
#
# compose instructions:
#
#         fhircapstoneproject:
#           build:
#             context: .
#             dockerfile: FhirCapstoneProject/Dockerfile
#           ports:
#             - 5000:5000
#
