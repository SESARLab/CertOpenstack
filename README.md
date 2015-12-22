Toward Security and Performance Certification of OpenStack

Authors: arco Anisetti, Claudio A. Ardagna, Ernesto Damiani, Filippo Gaudenzi, Roberto Veca

Dipartimento di Informatica Università degli Studi di Milano Crema, Italy, 26013


Information for reviewers
This page contains the probes and relative evidence from test described by the Paper

Probes
	
	Authentication Confidentiality
		probe - cfile
		probe - https_Driver

	Storage Confidentiality
		probe - testEncryption
		probe - findClearMapper

	Network Isolation
		probe - sgnetwork	

	Storage Performance
		probe - writeReadVolumes

	Service Performance
		probe - novacinderUnderHD (Test_ambiente.sh+ciclo_richieste.sh)


The Test Based Certification Framework is available at
- Test Manager : https://github.com/fgaudenzi/testManager
- Test Agent   : https://github.com/fgaudenzi/testAgent

