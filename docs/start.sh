#!/bin/bash
doxygen docs/prod.Doxyfile && \
cp -frv docs/output/html "$DOCS_STATIC" && \
sleep 9999
