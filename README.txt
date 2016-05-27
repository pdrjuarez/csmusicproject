THE FAB'S TEAM: Final Project
Pedro Juarez, Jordan Ng, and Michelle Kim
CMSC 12300: Computer Science with Applications III, Spring 2016
https://github.com/pdrjuarez/csmusicproject

------------------------
FILES IN 'csmusicproject'
------------------------
NOTES

csvify.py
validate.py

setup.sh


##################################
the below is a rough draft which
ideally will be typed up in LaTeX
or something else professional-ish
##################################
-----------------------
DESCRIPTION OF DATA SET
-----------------------
http://labrosa.ee.columbia.edu/millionsong/


--------------------
HYPOTHESES WE TESTED
--------------------


------------------
ALGORITHMS WE USED
------------------


------------------------
BIG DATA APPROACHES USED
------------------------


---------------------
EXTRAPOLATED RUNTIMES (optional)
---------------------


------------------------
NEW BIG DATA TOOLS/TECHS (optional)
------------------------


-------------------
CHALLENGES WE FACED (and overcame, or didn't)
-------------------
CHALLENGE: h5 files, didn't know how to read them
SOLUTION: realize we need to work within an ec2 instance

CHALLENGE: running setup.sh in our instance was difficult
DESCRIPTION: The script took a long time. We didn't see the printouts at first because we went into root to actually run the script, but we were able to see them once we ctrl+d back to ec2-user. Things didn't work at first, but fiddling around with the code fixed it. Specifically, we reran the following manually:
    
    cd
    git clone https://github.com/tbertinmahieux/MSongsDB

    export HDF5_DIR=/usr/local/hdf5
    export LD_LIBRARY_PATH=/usr/local/hdf5/lib
    cd /home/ec2-user


------------------
THE RESULTS WE GOT
------------------


----------------------------
HOW DID WE FIND OUR DATASET?
----------------------------

