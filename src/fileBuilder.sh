#!/bin/bash

cd ./client/client_files

rm client_file*
rm server_file*

for (( i=1 ;i <= 10; i=$i+1 ));do
	echo "Hello World!" >> client_file_$i.txt 
	done;

cd ../../server/server_files

rm client_file*
rm server_file*

for (( i=1 ;i <= 10; i=$i+1 ));do
        echo "Hello World!" >> server_file_$i.txt
        done;