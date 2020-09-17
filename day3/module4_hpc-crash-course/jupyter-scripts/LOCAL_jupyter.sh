#!/bin/bash

# Script to help people log into Jupyter Notebooks/Jupyter Lab instances 
# from their own local computers via SSH Tunneling; uses getopts for command line parsing

##### ##### ##### ##### ##### #####
# Define help message information #
##### ##### ##### ##### ##### #####
usage() {
cat << EOF
$0 (Michelle Franc Ragsac, mragsac@eng.ucsd.edu; January 2020)

usage:
This script generates a SSH tunnel that will connect a Jupyter 
instance from a defined remote server (e.g. COMET, TSCC)
to ones local computer in order to run Jupyter notebooks
on remote datasets.

OPTIONS
 -h	Show this help message
 -u 	Username (e.g. mragsac)
 -s 	Server information (e.g. comet-ln2.sdsc.edu, tscc-login7.sdsc.edu)
 -p	SSH tunnel port: The port used with the server localhost (e.g. 8421)
 -v 	Verbose
EOF
}

##### ##### ##### ##### ##### #####
#  Parse arguments using getopts  #
##### ##### ##### ##### ##### #####
USERNAME=
SERVER=
SSH_PORT=

# Define all of the arguments that should be expected by getopts;
# flags not requiring input DO NOT have a colon afterwards (e.g. h and v),
# and flags requiring input HAVE a colon afterwards (e.g. u, s, and p)
while getopts "hu:s:p:v" OPTION
do
	case $OPTION in
		h)
			usage # shares help message
			exit 1
			;;
		u)
			USERNAME=$OPTARG
			;;
		s)
			SERVER=$OPTARG
			;;
		p)
			SSH_PORT=$OPTARG
			;;
		v)
			VERBOSE=1
			;;
		?)
			usage # shares help message
			exit
			;;
		esac
done

##### ##### ##### ##### ##### #####
#  Verify input to all arguments  #
##### ##### ##### ##### ##### #####
if [[ -z $USERNAME ]] | [[ -z $SERVER ]] | [[ -z $SSH_PORT ]]
then
	echo "[ERROR] Missing one of the necessary arguments"
	echo "    -u, -s, and -p required to run program"
	echo "=============================================="
	echo ""
	usage
	exit 1
fi

# Share the input that was made to the script before running tunnel operation
echo "DETECTED INPUT -"
echo "    Username: " $USERNAME
echo "    Server: " $SERVER
echo "    SSH Tunnel Port: " $SSH_PORT
echo ""

echo "Performing operation..."
ssh -f -N -L $SSH_PORT:localhost:$SSH_PORT $USERNAME@$SERVER
