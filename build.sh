#!/usr/bin/bash

# Package Flask binary and move it to the client source directory
pushd server
source env/bin/activate
pyinstaller music_master_backend.spec
cp dist/music_master_backend ../client/src
deactivate
popd

# Build React app and package Music Master into an executable
pushd client
npm run build
npm run electron-pack
popd
