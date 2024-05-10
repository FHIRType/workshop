FROM python:3.11.7-alpine
WORKDIR /usr

# Add doxygen and doxypypy
RUN apk add doxygen
RUN python -m pip install doxypypy

# Add bash for boot cmd
RUN apk add bash

##################
# All environment variables in compose.yaml for consistency
#
#ENV DOCS_STATIC=/documentation/output/
COPY . .

# Add py_filter to path and make executable so doxypypy can use it
RUN chmod +x /usr/docs/py_filter.sh
RUN chmod +x /usr/docs/start.sh
RUN dos2unix /usr/docs/py_filter.sh
ENV PATH="/usr/docs:${PATH}"

# Run start script with sh
CMD /bin/bash /usr/docs/start.sh
