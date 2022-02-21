#!/usr/bin/env python
import yap #contains all the functions for parsing the combatlog
import logging
import sys 
import os
from matplotlib import pyplot as plt #used for testing to build plots

def main():

    #get first instance in combatlog
    instance = yap.get_combat_instances()[-1]  
    #get list of players in the instance 
    player_list = yap.get_player_list(instance)

    #do something 
    #function documentation in html folder
        



if __name__=='__main__':
    logging.info('starting yap')

    #get filepath somehow, or use default included for testing

    filepath = r".\logs\CasualSAB_Fleet_Malachowski_2189.log"
    if len(sys.argv) < 2:
        logging.info("using default file path")
    else:
        fileplath = sys.argv[1]
    
    if os.path.exists(filepath):
        logging.info("file exists")
        yap.read_parse(filepath)
    else:
        logging.error("Incorrect or missing Parse location")
        quit()

    main()