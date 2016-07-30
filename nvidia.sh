#! /bin/bash

if [ "$1" == "status" ]; then
 	cat /proc/acpi/bbswitch
else if [ "$1" == "enable" ]; then
		sudo tee /proc/acpi/bbswitch <<<ON
	else if [ "$1" == "disable" ]; then
			sudo tee /proc/acpi/bbswitch <<<OFF
		else
			echo "status | enable | disable"
		fi
	fi
fi