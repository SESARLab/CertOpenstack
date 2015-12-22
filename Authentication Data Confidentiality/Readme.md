Authentication Data Confidentiality

The two scripts here are written following the Certification Framework requirement. 


SSL/TSL script

 In order to run the https script you should modify you NMap scripts replacing the following files with those in NMapCustom folder:
	
	file1
	file2

Once you have your NMap ready, you must replace the information in inputHttps.cfg with you configuration.
Then you can run:

	$python Https_Driver.py --input inputHttps.cfg --output evidenceHttsp.log


File Access Policy script

 This script requires an sshkey to access the Devstack Host. Then, it requires to be present in the machine a user owner, a user from the same group of the owner and a user from anohter group. Once you satisfy the requirement in order to run the test you must replace the in inputFile.cfg with your user,file and key


	$python cFile.py --input inputFile.cfg --output outputFile.cfg

