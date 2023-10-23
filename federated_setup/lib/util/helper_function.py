import json
import time
import pickle
import pathlib
import socket
import asyncio

from getmac import get_mac_address as gma
from typing import Dict,List,Any
from hashlib import sha256
from federated_setup.lib.util.states_function import ClientState, IDPrefix


def set_config_file(config_type: str)-> str:
    module_path = pathlib.Path.cwd()
    config_file = f'{module_path}/setups/config_{config_type}.json'

    return config_file

def read_config(config_path: str)-> Dict[str,Any]:
    with open(config_path) as jf:
        config = json.load(jf)
    return config

def generate_id()-> str:

    macaddr =gma()
    in_time = time.time()

    raw = f'{macaddr}{in_time}'
    hash_id = sha256(raw.encode('utf-8'))
    return hash_id.hexdigest()

def get_ip() -> str:

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #AF_INET is used to obtain the address family of ipv4 addresses
    try:
        s.connect(('1.1.1.1',1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def load_model_file(path:str, name: str)-> (Dict[str, Any], Dict[str, float]):
    fname = f'{path}/{name}'
    with open(fname,'rb') as f:
        data_dict = pickle.load(f)

    performance_dict = data_dict.pop('performance')

        # data_dict only includes models
    return data_dict, performance_dict

def compatible_data_dict_read(data_dict:Dict[str,Any]) -> List[Any]:

    if 'my_id' in data_dict.keys():
        id = data_dict['my_id']
    else:
        id = generate_id()

    if 'gene_time' in data_dict.keys():
        gene_time = data_dict['gene_time']
    else:
        gene_time = time.time()

    if 'models' in data_dict.keys():
        models = data_dict['models']
    else:
        models = data_dict

    if 'model_id' in data_dict.keys():
        model_id = data_dict['model_id']
    else:
        model_id = generate_model_id(IDPrefix.agent, id, gene_time)

    return id, gene_time, models, model_id


def generate_model_id(component_type: str, component_id: str, generation_time: float) -> str:
   
    raw = f'{component_type}{component_id}{generation_time}'
    hash_id = sha256(raw.encode('utf-8'))
    return hash_id.hexdigest()
    
    