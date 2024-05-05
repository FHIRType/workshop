#!/bin/sh
doxygen docs/Doxyfile && \
cp -frv docs/output/html/ $DOCS_STATIC