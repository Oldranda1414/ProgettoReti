#!/bin/bash

cd ./client/clientFiles

rm client_file*
rm server_file*

for (( i=1 ;i <= 10; i=$i+1 ));do
	echo "Hello World!" >> client_file_$i.txt 
	done;

cd ../../server/serverFiles

rm client_file*
rm server_file*

for (( i=1 ;i <= 10; i=$i+1 ));do
        echo "Hello World!" >> server_file_$i.txt
        done;