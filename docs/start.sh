#!/bin/bash
doxygen /usr/docs/prod.Doxyfile && \
cp -frv /usr/docs/output/html "$DOCS_STATIC" && \
sleep 9999
