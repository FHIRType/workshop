FROM python:3.11.7-alpine
WORKDIR /usr

# Add doxygen and doxypypy
RUN apk add doxygen
RUN python -m pip install doxypypy

# Add bash for boot cmd
RUN apk add bash

ENV DOCS_STATIC=/documentation/output/
COPY . .

# Add py_filter to path and make executable so doxypyp can use it
RUN chmod +x docs/py_filter
ENV PATH="/usr/docs:${PATH}"

# Run start script with sh
CMD ["/bin/sh", "/usr/docs/start.sh"]
