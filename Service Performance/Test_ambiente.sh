#!/bin/bash

echo Crea il Tipo
cinder type-create LUKS
echo Crea il Tipo Cifrato
cinder encryption-type-create --cipher aes-xts-plain64 --key_size 512 --control_location front-end LUKS nova.volume.encryptors.luks.LuksEncryptor

echo Availabe images
nova image-list
echo Crea tiny cirros image
nova boot IstanzaTest --image $(nova image-list | grep "uec " | awk '{ print $2 }') --flavor 2

echo wait for running state
sleep 35

#echo Lista tipi volume
cinder type-list
cinder encryption-type-list
#echo "Inserisco l'ID del tipo di Volume Cifrato"

#echo Crea Volume Cifrato e Volume in Chiaro
cinder create --display-name VolumeCifratoTest --volume-type $(nova volume-type-list | grep LUKS |awk '{print $2}') 10
cinder create --display-name VolumeChiaroTest 10

#echo attendo 20 secondi per la creazione...
sleep 20

#echo Lista Istanze e volumi
nova list
cinder list

######## Inserimento Variabili ########
#echo -e "\n----- Inserimento Variabili -----"

#echo " - Inserisco l'id|nome dell'istanza.."
istanza=`nova list | grep IstanzaTest | awk '{print $2}'`

#echo " - Inserisco l'id del Volume in chiaro.."
volume1=`cinder list | grep VolumeChiaroTest | awk '{ print $2 }'`

#echo " - Inerisco l'id del Volume cifrato.."
volume2=`cinder list | grep VolumeCifratoTest | awk '{ print $2 }'`

######## Attaccamento Volume a Istanza ########
echo -e "\n-----Attaching Volumes to VM -----"

DEVCHIARO=`nova volume-attach $istanza $volume1 | grep device | awk '{print $4}'`
echo " - CLEAR Volume Attached - dev -> $DEVCHIARO" 

DEVCIFRATO=`nova volume-attach $istanza $volume2 | grep device | awk '{print $4}'`
echo " - CLEAR Volume Attached - dev -> $DEVCHIARO" 
sleep 10

# ELIMINAZIONE

echo -e "\n-----Environment Destruction----"
Istanza=`nova list | grep IstanzaTest | awk '{print $2}'`
echo " - - VM_ID = $Istanza"
volume1=`cinder list | grep VolumeChiaroTest | awk '{print $2}'`
echo " - - CLEAN Volume = $volume1"
volume2=`cinder list | grep VolumeCifratoTest | awk '{print $2}'`
echo " - - LUKS Volume = $volume2"
tipo=`cinder type-list | grep LUKS | awk '{print $2}'`
echo " - - Type = $tipo"
sleep 20
echo -e "\n - detaching..."
nova volume-detach $Istanza $volume1
sleep 20
nova volume-detach $Istanza $volume2
sleep 20

echo -e "\n - deleting..."
cinder delete $volume1
sleep 30
cinder delete $volume2
sleep 60

stato1=`cinder list | grep $volume1 | awk '{print $4}'`
stato2=`cinder list | grep $volume2 | awk '{print $4}'`

   sleep 5
   stato1=`cinder list | grep $volume1 | awk '{print $4}'`
   stato2=`cinder list | grep $volume2 | awk '{print $4}'`
#   echo "Lo stato1 è ancora $stato1"
#   echo -e "Lo stato2 è ancora $stato2\n"

cinder type-delete $tipo
sleep 20

nova delete $Istanza
sleep 20


echo -e "\n\n------ OPENSTACK STATE ------"
nova list
cinder list
cinder type-list
cinder encryption-type-list
