# CEPCEventDisplay


You can install PyShow in any directory:
	
		git clone https://github.com/Tom0126/CEPCEventDisplay.git		

After you have successfully installed it, enter the directory:

		cd CEPCEventDisplay
		
If you run it in the Test Beam Server (@cepcecalserver.cern.ch), you can use the python environment I have pre-installed:

		source conda_setup.sh


Two running PyShow methods are provided here. 


	1. If you can open a gui window in your terminal, it is highly recomened using PyShow in this way.
	You just need to input both of ecal and ahcal root file path, and don't forget to click "start" :
	
		python AHCAL_ECAL_mac.py
		
	2. In a more linux way, where e_path is the ecal root file path, a_path is the ahcal root file path,
	e_en is the specified ecal entry_no, a_en is the specified ahcal entry_no:
	
		python Display.py --e_path <xxx> --a_path <xxx> --e_en <xxx> --a_en <xxx>
		
	   You can find the figure in the Result dir.
