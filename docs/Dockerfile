FROM python:3.11.7-alpine
WORKDIR /usr

# Add doxygen and doxypypy
RUN apk add doxygen
RUN python -m pip install doxypypy

# Add bash for boot cmd
RUN apk add bash

COPY . .

ENV DOCS_STATIC=/documentation/output/

RUN export PATH=$PATH:/docs
RUN doxygen docs/Doxyfile

CMD cp -frv docs/output/html/ $DOCS_STATIC
