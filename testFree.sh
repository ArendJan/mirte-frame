#!/bin/bash
# sudo add-apt-repository ppa:freecad-maintainers/freecad-stable -y
# sudo apt-get update
# sudo apt-get install freecad xvfb  -y
# setup: copy files to ~/.local/share/FreeCAD/Mod
mkdir -p ~/.local/share/FreeCAD/
cp -r ./scripts/RenderSteps ~/.local/share/FreeCAD/Mod || true

TEST=false
$TEST && mkdir /tmp/mirte-frame
$TEST && cp -r ./freecadFiles /tmp/mirte-frame/
$TEST || export DISPLAY=:1
echo $DISPLAY
# export LIBGL_ALWAYS_SOFTWARE=1
# export LIBGL_ALWAYS_INDIRECT=0
# export LP_NO_RAST="false"
$TEST || Xvfb ${DISPLAY} -screen 0 1920x1080x24 &
$TEST || XPID=$!

freecad &
FreecadPID=$!
sleep 10
echo $SECONDS
xwd -root -silent | convert xwd:- png:/tmp/screenshot.png

sleep 20

$TEST || kill $XPID
kill $FreecadPID
rm -rf ~/.local/share/FreeCAD/Mod/RenderSteps