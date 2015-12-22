#!/bin/bash
echo "----- Envryption Test -----"
echo "challenge CLEAN -> Stringa in volume chiaro"
echo "challenge LUKS -> Stringa in volume cifrato"
echo Create LUKS type
echo Crea il Tipo
cinder type-create LUKS
echo Crea il Tipo Cifrato
cinder encryption-type-create --cipher aes-xts-plain64 --key_size 512 --control_location front-end LUKS nova.volume.encryptors.luks.LuksEncryptor

echo Available images
nova image-list
echo "Inserisco l'ID dell'immagine : cirros-0.3.2-x86_64-uec"
echo Crea tiny cirros image
nova boot IstanzaTest --image $(nova image-list | grep "uec " | awk '{ print $2 }') --flavor 2

echo wait for running state
sleep 35

#echo Lista tipi volume
cinder type-list
cinder encryption-type-list
#echo "Inserisco l'ID del tipo di Volume Cifrato"

#echo Crea Volume Cifrato e Volume in Chiaro
cinder create --display-name VolumeCifratoTest --volume-type $(nova volume-type-list | grep LUKS |awk '{print $2}') 1
cinder create --display-name VolumeChiaroTest 1

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
#echo " - Attacco il volume in chiaro - Il device letto è : $DEVCHIARO" 

DEVCIFRATO=`nova volume-attach $istanza $volume2 | grep device | awk '{print $4}'`
#echo " - Attacco il volume cifrato  - Il device letto è : $DEVCIFRATO"
sleep 5

######## Modifica al file di Cirros ########
echo -e "\n----- Script Injection Configuration -----"
cp Cirros_vulnerabilita CirrosGo

echo -e "\nSCRIPTS"
ls -lah Cirros*
sleep 2

DIMCHIARO=`sudo blockdev --getsz /dev/stack-volumes-default/volume-$volume1`
DIMCIFRATO=`sudo blockdev --getsz /dev/stack-volumes-default/volume-$volume2`

DIMCIFRATO=$((DIMCIFRATO-4096))

sed -i "s|CLEAN|$DEVCHIARO|g" CirrosGo
sed -i "s|CIPHER|$DEVCIFRATO|g" CirrosGo
sed -i "s|DIMCHIARO|$DIMCHIARO|g" CirrosGo
sed -i "s|DIMCIFRATO|$DIMCIFRATO|g" CirrosGo

sleep 15


#3_ESEC_IN_VM
IPISTANZA=`nova list | grep IstanzaTest | awk '{print $12}' | sed "s|private=||g"`


sshpass -p "cubswin:)" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no CirrosGo cirros@$IPISTANZA:/home/cirros &> /dev/null
sshpass -p "cubswin:)" ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no cirros@$IPISTANZA -t "sudo chmod +x CirrosGo" &> /dev/null

echo -e " - Running injected script"
echo -e " - - This operation may requires some times\n"
time 2> tempoesecuzione sshpass -p "cubswin:)" ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no cirros@$IPISTANZA -t "sudo ./CirrosGo" 1> /dev/null

echo -e "\n - Getting Results"
sshpass -p "cubswin:)" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no cirros@$IPISTANZA:/home/cirros/outputDD.txt ./ &> /dev/null

#sed -i "s|#TEMPOESECUZIONE| Tempo esecuzione Script : $(cat tempoesecuzione)|g" outputDD.txt

echo -e " - - Result from VM (outputDD.txt) :"
echo "-------------------------------------------------------------"
cat outputDD.txt
echo "-------------------------------------------------------------"

# VERIFICA SE SI LEGGE DA FUORI!

echo -e "\n -- TEST from host -- \n"
echo -e "\n----- Encryption Test -----"
echo -e "\n--- Encryption Test ---" >> outputDD.txt

mapper=`ls /dev/mapper/ip*$volume2*`
echo -e "\n ... searching challenge in device mapper: ..."
sudo strings $mapper | grep "Stringa in volume cifrato"

# PArte di lettura completa del file nel volume cifrato
# NON ancora funzionante
# ------------------------------- 
#sudo mkdir /opt/provaCifrato
#sudo mount $mapper /opt/provaCifrato
#FileIstanza=`find /opt/provaCifrato/ type -f -iname File_di_prova.txt`

#if [ -n "$FileIstanza" ] ; then
#	echo "File Visibile"
#	cat $FileIstanza
#else
#	echo "File NON Visibile"
#fi

#sudo umount $mapper /opt/provaCifrato
#sudo rm -r /opt/provaCifrato


#ELIMINAZIONE AMBIENTE

echo -e "\n-----Environment Destruction----"
Istanza=`nova list | grep IstanzaTest | awk '{print $2}'`
echo " - - VM_ID = $Istanza"
volume1=`cinder list | grep VolumeChiaroTest | awk '{print $2}'`
echo " - - CLEAN = $volume1"
volume2=`cinder list | grep VolumeCifratoTest | awk '{print $2}'`
echo " - - LUKS = $volume2"
tipo=`cinder type-list | grep LUKS | awk '{print $2}'`
echo " - - Tipo = $tipo"

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
