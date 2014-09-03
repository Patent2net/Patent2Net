  _____      _             _     ___    _   _      _   
 |  __ \    | |           | |   |__ \  | \ | |    | |  
 | |__) |_ _| |_ ___ _ __ | |_     ) | |  \| | ___| |_ 
 |  ___/ _` | __/ _ \ '_ \| __|   / /  | . ` |/ _ \ __|
 | |  | (_| | ||  __/ | | | |_   / /_  | |\  |  __/ |_ 
 |_|   \__,_|\__\___|_| |_|\__| |____| |_| \_|\___|\__|

About
�����
Patent2Net is elaborated and maintained (on a free base) by a small international team of professors and researchers
Patent2Net is a "free" package, dedicated to :
	augment the use of patent information in academic, nano and small firms, developing countries (all those without pay mode access)
	learn, study and practice how to collect, treat and communicate "textual bibliographic information", and automation process 
	provide statistical analysis and representations of a set of patents.
	
Patent2Net is an "open source" package and contributions are welcome.
Patent2Net is available "as it is".

First step : Train how to search patent information using interface
�������������������������������������������������������������������

http://worldwide.espacenet.com/advancedSearch?locale=en_EP

Practice and use the available help :
http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=index
more especially : 
Full-text search
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=<fulltext></fulltext>
boolean operators
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=booleans
Truncation
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=truncation
Smart search - field identifiers
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=fieldidentifier
Limitations
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=limitations
Date formats and Ranges
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=dateformats
Kind Codes
	http://worldwide.espacenet.com/help?locale=en_EP&method=handleHelpTopic&topic=kindcodes
Respect the Fair use Charter for the EPO's online patent information products
	http://www.epo.org/searching/free/fair-use.html

Install Patent2Net package
��������������������������
To run as python script need to install python and some libraries :

Install python 2.7 x86  from https://www.python.org/
Actualise the "path" to python My Computer > Properties > Advanced System Settings > Environment Variables >
Reboot
Install pip http://www.pip-installer.org/en/latest/installing.html
Install requests library : in "C:\Python27\Scripts" open a command windows and run "pip install requests"
Install networkx library : finding the good way to install in http://networkx.github.io/documentation/latest/install.html

Download Patente2Net from https://github.com/Patent2net/Patent2Net unpack where you want on your disk
Use the current version as above

setup.py is provided also to compile binaries for your windows operating system. Use it with the command python setup.py py2exe to produce binaries in the dist directory.
To run as a an exe file (windows) : need to install the "full package", updating can be done only copying the "Patent2Net" files. Operate as a "Command window"

Use Patent2Net
��������������
Open a windows command in your Patent2Net directory
	
1 - Construct the patent list with OpsGather-PatentList.py
	Use as : OpsGather-PatentList.py Your_File.dump "search expression"
	For example : OpsGather-PatentList.py test.dump "ti =(stereolithography or \"3D print*\") AND pd<=1996"
	Protect the " with a \ Should obtain at minimum as many patents as with the URL interface.
	Results are stored in the "PatentLists" directory within the dump file in pickle format.

2 - Download bibliographic data using OpsGather-BiblioPatents.py Your_File.dump
	For example : OpsGather-BiblioPatent.py test.dump
	The dump file is the file produced on stage 1 (without path, patentlist directory is the default source)
	The result is a file with same name (bigger) stored in the "BiblioPatents" directory.

3 - convert to gephi (gexf) file : PatentsToNet.py Your_File.dump.
	The dump file is the file produced on stage 2 (without path, BiblioPatents directory is the default source)
	Result is stored in "GephiFile" directory as a Your_File.dump.gexf.

4 - download the claims (optional, not consistent at this time) : OpsGather-Claims.py Your_File.dump
	The dump file is the file produced on stage 2 (without path, patentlist directory is the default source)
	Available claims (mainly European Patents EP) will be downloaded and stored "claims" directory in iramutek format (http://www.iramuteq.org/)

Todo List :
�����������
	URL Links for IPC 7 and 11
	URL Links for inventors or applicant (to evaluate what they are doing out of search field, in general)
	Grouping results in Patent Family. 
	Other Gathering process list for family requests
	Susbscribed version. 
	Patent Citation
	Revisit weights.
	
V 0.9 26/03/2014
����������������
	OpsGather-PatentList
		-Accept an Espacenet "smart search" query
	PatentsToNet
		-fully connected graph is provided in Gephi, connecting any relation (intra and Inter field) : filtering can be done in Gephi or hacking in the Python script. 
		-International Patent Classification is treated to be "truncated" at level 1,3,4,7. nodes for each level are created
		-Countries from Patent numbers (first deposit?) are considered as nodes
		-Kind codes (status) are separated as nodes
		-URL links as node attribute in gexf 
			for patent number : link to espacenet
			for International Patent Classification IPC at level 1,3,4 : link to IPC database (French and English)
		-Dynamic graph are available over first available date (column "deb" and "fin" as to be merged as timeline for nodes and edges in data laboratoty in Gephi)
		- directed graph is build complete in bidirection mode: Inventor-Inventor; IPC-IPC; Applicant-Applicant, and all combinations
		-Weight of nodes are provided as....
		-Weight among time are provided for node as ...
		-Weight of edges are provided as ....