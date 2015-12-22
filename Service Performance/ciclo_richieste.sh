#!/bin/bash
i="0"
novasum="0"
cindersum="0"
maxnova="0"
maxcinder="0"
maxnovamedia="0"
maxcindermedia="0"

#while [ $i -lt 10 ]

novaok=`which nova`
cinderok=`which cinder`
timeok=`which time`

echo "--- Loop for cinder-list and nova-list ---"
echo "Now_time  Nova_time  Cinder_time  Nova_media  Cinder_Media  Max_Nova_time  Max_Cinder_time  Max_Nova_avg  Max_Cinder_avg  "
while true
do
#       $timeok -f %e $novaok list 1> /dev/null 2> file
#	$timeok -f %e $cinderok list 1> /dev/null 2> file
        
	nova_time=$($timeok -f %e $novaok list 2>&1 > /dev/null)
	cinder_time=`$timeok -f %e $novaok list 2>&1 > /dev/null`	

	echo -n -e "\n`date +%H:%M:%S`  " # Questo istante 
	echo -n -e "$nova_time  " # tempo di nova
	echo -n -e "$cinder_time  " # tempo di cinder
	
	# --- CALCOLO MEDIA ---
	i=$((i + 1))	
	novasum=$(echo "$novasum + $nova_time" | bc)
	novamedia=$(echo "scale=2; $novasum/$i"|bc -l)

	cindersum=$(echo "$cindersum + $cinder_time" | bc)
        cindermedia=$(echo "scale=2; $cindersum/$i"|bc -l)
	

#	x=$(echo "scale = 2; $ach_gs * 100 / $ach_gs_max" | bc)
#	novasum=`expr $novasum + nova_time`
#	cindersum=$(( (cindersum + cinder_time)/i ))
		
	echo -n -e "$novamedia  "
	echo -n -e "$cindermedia  "

	echo -n -e "$maxnova  "
        echo -n -e "$maxcinder  "
	echo -n -e "$maxnovamedia  "
        echo -n -e "$maxcindermedia"

	# --- CALCOLO DEI MASSIMI ---
	
	if [ $(echo " $nova_time > $maxnova" | bc) -eq 1 ] ; then
		maxnova=$nova_time
	fi
	if [ $(echo " $cinder_time > $maxcinder" | bc) -eq 1 ] ; then
                maxcinder=$cinder_time
        fi
	if [ $(echo " $novamedia > $maxnovamedia" | bc) -eq 1 ] ; then
                maxnovamedia=$novamedia
        fi
	if [ $(echo " $cindermedia > $maxcindermedia" | bc) -eq 1 ] ; then
                maxcindermedia=$cindermedia
        fi

#	echo -n -e "\t\t\tcinder media = $cindersum"
	
	#echo $i
	#i=$[$i+1]
	
	#IMPO mettere lo sleep sennò non esce dal ciclo!!
	#ma non in questo caso! ;)
done
