#!/bin/zsh
# usage: topdf.sh in.docx out.pdf   (runs Microsoft Word inside its sandbox container)
W=~/Library/Containers/com.microsoft.Word/Data/f24build
mkdir -p $W; rm -f $W/*
cp "$1" $W/in.docx
osascript -e "
with timeout of 180 seconds
tell application \"Microsoft Word\"
  open (POSIX file \"$W/in.docx\")
  delay 3
  set d to active document
  save as d file name \"$W/out.pdf\" file format format PDF
  close d saving no
end tell
end timeout" || exit 1
cp $W/out.pdf "$2"
