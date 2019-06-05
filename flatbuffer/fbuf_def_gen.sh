#!/bin/bash
set -x
set -e
CUR_DIR=`pwd`
trap cleanup ERR

cleanup()
{
    echo "ERROR: script errored out!"
    rm -rf js_defs py_defs
    cd ${CUR_DIR}
    exit 1
}

TOP_DIR='../'
# location of your flatbuffer compiler
FLATC=${TOP_DIR}/tools/flatbuffers/flatc
FLATBUFFER_SCHEMA_DIR=${TOP_DIR}/flatbuffer
cd ${FLATBUFFER_SCHEMA_DIR}

# Javascript bindings
rm -rf js_defs
${FLATC} -o js_defs/ --js ServerProxy.fbs
${FLATC} -o js_defs/ --js ResponseMessage.fbs

# Python bindings
rm -rf py_defs
${FLATC} -o py_defs/ --python ServerProxy.fbs
${FLATC} -o py_defs/ --python ResponseMessage.fbs

touch __init__.py
touch py_defs/__init__.py
touch py_defs/ServerProxy/__init__.py
touch py_defs/ResponseMessage/__init__.py

chmod 755 -R ./js_defs
chmod 755 -R ./py_defs
cd  ${CUR_DIR}
set +e
set +x
