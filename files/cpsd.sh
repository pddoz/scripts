#!/bin/sh

LIST=""
E=""

if [ ! -d "$HOME/files" ]
then
	mkdir $HOME/files
fi

while true
do
	F=$(mount | grep -E '/dev/sd[bcdef]')
	E=$(echo $F | grep -Eo '^[^ ]+')
	#echo $E
	#echo $LIST
	if [ "$LIST" != "$E" ]
	then
		FS=$(echo $F | awk '{print $3}')
		name=$HOME/files/$(echo $FS | grep -Eo '[^/]+$')

		if [ ! -d "$name" ]
		then
			mkdir $name;
		fi

		echo $name
		cp -R $FS/* $name/
		LIST=$E
	fi
	
	sleep 10
done


	