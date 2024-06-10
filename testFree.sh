#!/bin/bash
# sudo add-apt-repository ppa:freecad-maintainers/freecad-stable -y
# sudo apt-get update
# sudo apt-get install freecad xvfb  -y
# setup: copy files to ~/.local/share/FreeCAD/Mod
set -xe
freecadcmd --version
# cp -r ./scripts/RenderSteps ~/.local/share/FreeCAD/Mod || true
ls ~
ls -al ~
TEST=false
$TEST && mkdir /tmp/mirte-frame
$TEST && cp -r ./freecadFiles /tmp/mirte-frame/
$TEST || export DISPLAY=:123
echo $DISPLAY
# export LIBGL_ALWAYS_SOFTWARE=1
# export LIBGL_ALWAYS_INDIRECT=0
# export LP_NO_RAST="false"
export QTWEBENGINE_DISABLE_SANDBOX=1
$TEST || Xvfb ${DISPLAY} -screen 0 1920x1080x24 &
XPID=$!

freecad -M ./scripts/RenderSteps &
FreecadPID=$!
sleep 20
echo $SECONDS
xwd -root -silent | convert xwd:- png:/tmp/screenshot.png

sleep 20

$TEST || kill $XPID
kill $FreecadPID
rm -rf ~/.local/share/FreeCAD/Mod/RenderSteps