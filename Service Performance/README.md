Service Performance

The two scripts here were adapted from their original form to be selfrunning. Once you have your Devstack Environment Variable set you can run inside the devstack machine the two scripts in parallel:

	$nohup ./ciclo_richieste > /dev/null 2>&1 &
	$./Test_ambiente.sh

