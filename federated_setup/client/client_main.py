import asnycio
import time
import logging
import sys
import os
from typing import Dict,Any
from threading import Thread
from federated_setup.lib.util.helper_function import generate_id,get_ip,set_config_file,read_config,compatible_data_dict_read,load_model_file,compatible_data_dict_read

class Client:

    def __init__(self):

        time.sleep(2)
        logging.info(f"-----Client initialized---")

        self.client_name = 'default_client'

        self.id = generate_id() # generating id

        self.agent_ip = get_ip() # getting ip address 

        self.simulation_flag = False #if its running on a single machine / multiple machine
        
        if len(sys.argv)>1: # to check the staus of the simulation flag
            self.simulation_flag = bool(int(sys.argv[1]))

        config_file = set_config_file("client")
        self.config = read_config(config_file)

        self.aggr_ip = self.config['aggr_ip']
        self.reg_socket = self.config['reg_socket'] # reg_socket is used for registration of the agent
        self.msend_socket = 0  # used to send the local model to the aggregator 
        self.exch_socket = 0 #used when polling method is not there for recieving global models

        if self.simulation_flag: #in simulation we read from command line
            self.exch_socket = int(sys.argv[2])
            self.agent_name = sys.argv[3]

        self.model_path = f'{self.config["model_path"]}/{self.agent_name}'

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        self.lmfile = self.config['local_model_file_name']
        self.gmfile = self.config['global_model_file_name']
        self.statefile = self.config['state_file_name']

         # Aggregation round - later updated by the info from the aggregator
        self.round = 0
        
        # Initialization
        self.init_weights_flag = bool(self.config['init_weights_flag']) #flag when system operator wants to intialise global model with parameters

        # Polling Method
        self.is_polling = bool(self.config['polling'])

    async def participate(self):
        data_dict, performance_dict = load_model_file(self.model_path,self.lmfile)
        _, gene_time, models, model_id = compatible_data_dict_read(data_dict)