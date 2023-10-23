from enum import Enum, IntEnum

class IDPrefix:  #used to identify how each component is being identified 
    agent = 'agent'
    aggregator = 'aggregator'
    db = 'database'  #mostly not needed state

# CLIENT STATE
class ClientState(IntEnum): #list of different client states
   
    waiting_gm = 0
    training = 1
    sending = 2
    gm_ready = 3

# TYPES
class ModelType(Enum): #type of model
  
    local = 0
    cluster = 1

class DBMsgType(Enum): #message type defined in between an agregator and an agent
    
    push = 0

class AgentMsgType(Enum): #types of messages needed to be sent from an aggregator to an agent
    
    participate = 0
    update = 1
    polling = 2

class AggMsgType(Enum):
   
    welcome = 0
    update = 1
    ack = 2

# MSG LOCATION
class ParticipateMSGLocation(IntEnum): #messages location sent from client to the server
   
    msg_type = 0
    agent_id = 1
    model_id = 2
    lmodels = 3
    init_flag = 4
    sim_flag = 5
    exch_socket = 6
    gene_time = 7
    meta_data = 8
    agent_ip = 9
    agent_name = 10
    round = 11

class ParticipateConfirmationMSGLocation(IntEnum):
    
    msg_type = 0
    aggregator_id = 1
    model_id = 2
    global_models = 3
    round = 4
    agent_id = 5
    exch_socket = 6
    recv_socket = 7

class DBPushMsgLocation(IntEnum):
   
    msg_type = 0
    component_id = 1
    round = 2
    model_type = 3
    models = 4
    model_id = 5
    gene_time = 6
    meta_data = 7
    req_id_list = 8

class GMDistributionMsgLocation(IntEnum):
    
    msg_type = 0
    aggregator_id = 1
    model_id = 2
    round = 3
    global_models = 4

class ModelUpMSGLocation(IntEnum):
  
    msg_type = 0
    agent_id = 1
    model_id = 2
    lmodels = 3
    gene_time = 4
    meta_data = 5

class PollingMSGLocation(IntEnum):
   
    msg_type = 0
    round = 1
    agent_id = 2