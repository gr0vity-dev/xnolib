#!/bin/env python3
#
# PREREQUISITE : Access to a nano_node with RPC control_enabled = true
#
# >>> How to use this script 
# python3 gr0_fork_publish.py --source_seed=0000000000000000000000000000000000000000000000000000000000000106 --rpc_url=http://localhost:55000
#
# >>>What does the script do ?
# Create multiple fork chains. (Defined in the dest_seeds_chains variable)
# Broadcast all blocks (except send blocks from --source_seed) to one voting peer
# Wait for 30 seconds, then broadcast send blocks from --source_seed to different voting_peers.
#
# >>> I want to send to different accounts
#     By changing the dest_seeds_chains variable, 
#     You can change the seed for all accounts. 
#     Or You can add additional layers or chains if needed


from pynanocoin import *
from peercrawler import *
from msg_handshake import node_handshake_id
import argparse
import requests
import json
import time
from gr0_tools.nano_rpc import Api



dest_seeds_chains = {"chainA11" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000A", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000A1", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000A11", "layer" : 3} ],
                     "chainA12" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000A", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000A1", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000A12", "layer" : 3} ], 
                     "chainA21" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000A", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000A2", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000A21", "layer" : 3} ] ,
                     "chainA22" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000A", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000A2", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000A22", "layer" : 3} ], 
                     "chainB11" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000B", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000B1", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000B11", "layer" : 3} ],
                     "chainB12" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000B", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000B1", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000B12", "layer" : 3} ], 
                     "chainB21" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000B", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000B2", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000B21", "layer" : 3} ] ,
                     "chainB22" : [ {"dest_seed" : "110000000000000000000000000000001300000000000000000000000000000B", "layer" : 1}, 
                                    {"dest_seed" : "11000000000000000000000000000000130000000000000000000000000000B2", "layer" : 2},                   
                                    {"dest_seed" : "1100000000000000000000000000000013000000000000000000000000000B22", "layer" : 3} ]  }

def add_to_chain_visu(chain_visu_l, text) :    
    chain_visu_l = chain_visu_l + "\n"
    return chain_visu_l
def print_and_reset_chain_visu(chain_visu_l):
    if chain_visu_l == None :
        return ""    
    print(chain_visu_l)
    return ""

def create_fork_blocks(args):  
    fork_blocks = {}
    chain_visu = ""
    # -------------- 0) START -------------------------
    # Determinate the number of transfers and seeds to be created
    api = Api(args.rpc_url, debug=False, forks=True) #reset api instance for each fork chain. Blocks are saved in memory per instance. 
    for seed_chain in dest_seeds_chains.items():
        #Visualize fork chains. (Empty on first iteration)
        chain_visu = print_and_reset_chain_visu(chain_visu)
        current_chain = next(iter(seed_chain))        
        source_seed = args.source_seed 
        layer = 0
        chain_visu = current_chain + "\n"
        for seed in seed_chain[1]:                                     
            dest_data = api.get_account_data(seed["dest_seed"], 0)           

            send_block = api.create_send_block_seed(source_seed, 
                                                    0, 
                                                    dest_data["account"], 
                                                    args.amount_raw,
                                                    broadcast = 0)
            #Add to fork chain visualisation  (send blocks)                                       
            chain_visu = chain_visu + "from:  '{}' --> {:<10}'{}'".format(send_block["block"]["account"], send_block["subtype"] + ":", send_block["hash"])  + "\n"       
            
            #Only add send_block once per hash. (different fork chains have the same block hashes for the first layers)
            fork_blocks[send_block["hash"]] = {"block" : send_block, "layer" : layer}
            layer = seed["layer"]
            
            receive_block = api.create_receive_block_seed(dest_data["seed"],
                                                            0,
                                                            args.amount_raw,
                                                            dest_data["account"],
                                                            send_block["hash"],
                                                            broadcast = 0)  
            #Add to fork chain visualisation (receive/open blocks)   
            chain_visu = chain_visu + "to:    '{}' <-- {:<10}'{}'".format(receive_block["block"]["account"], receive_block["subtype"] + ":", receive_block["hash"])  + "\n"   
            
            #Only add open/receive_block once per hash.
            fork_blocks[receive_block["hash"]] = {"block" : receive_block, "layer" : layer}
            source_seed = dest_data["seed"]

    #Visualize last fork chain
    print_and_reset_chain_visu(chain_visu)
    
    #prepare list of list of dicts  [ [{block1_layer_0}, {block2_layer_0}] , [{block1_layer_1}, {block2_layer_1},{...}], [...], ... ]
    layer_count = max([ int(d["layer"]) for d in fork_blocks.values() ]) + 1
    fork_layers = [[] for _ in range(layer_count)]
    
    for fork in fork_blocks.values() :
        fork_layers[fork["layer"]].append(fork["block"]["block"])

    # print("fork_layers : \n" , fork_layers , "\n")    
    return fork_layers
   

def handshake_peer(ip,port,ctx, retry = 3):
    try:
        socket = get_connected_socket_endpoint(ip, port)
        node_handshake_id.perform_handshake_exchange(ctx, socket)
        print('peer added [%s]:%s' % (ip, port))        
        return socket
    except:        
        retry = retry -1
        print("error on handshake_peer for {}:{} | retry_count {}".format(ip,port,retry))
        if retry >= 1 :
            handshake_peer(ip,port,ctx, retry = retry)
    


class msg_publish:
    def __init__(self, hdr, block):
        assert(isinstance(hdr, message_header))
        self.hdr = hdr
        self.block = block

    def serialise(self):
        data = self.hdr.serialise_header()
        data += self.block.serialise(False)
        return data

    @classmethod
    def parse(cls, hdr, data):
        block = None
        blocktype = hdr.block_type()
        if blocktype == 2:
            block = block_send.parse(data)
        elif blocktype == 3:
            block = block_receive.parse(data)
        elif blocktype == 4:
            block = block_open.parse(data)
        elif blocktype == 5:
            block = block_change.parse(data)
        elif blocktype == 6:
            block = block_state.parse(data)
        else:
            assert False
        return msg_publish(hdr, block)

    def __str__(self):
        return str(self.hdr) + "\n" + str(self.block)   


def main():

    parser = argparse.ArgumentParser(description="Echo your input")
    #default sourec seed : 0000000000000000000000000000000000000000000000000000000000000106 
    #default account at index 0 : nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm

    # Add a position-based command with its help message.
    parser.add_argument("--source_seed", help="Seed to derive source addresses")
    # parser.add_argument("--source_index", type=int, help="Seed to derive source addresses")  
    parser.add_argument("--rpc_url" ,help="Default : http://localhost:55000")
    parser.add_argument("--amount_raw", type=int ,help="Default : 100. Amount that is passed between accounts")    

    # Use the parser to parse the arguments.
    args = parser.parse_args()    
   
    if args.rpc_url == None : args.rpc_url = "http://localhost:55000"
    if args.source_seed == None : args.source_seed = "0000000000000000000000000000000000000000000000000000000000000106"  
    if args.amount_raw == None : args.amount_raw = 100 

    #create forks
    forks = create_fork_blocks(args) 
    
    ctx = betactx
    msgtype = message_type_enum.publish
    hdr = message_header(network_id(66), [18, 18, 18], message_type(msgtype), 0)
    hdr.set_block_type(block_type_enum.state)

    voting_peers = get_voting_peers(ctx)
    sockets = []

    #Handshake with all voting peers
    for peer in voting_peers :
        s = handshake_peer(str(peer.ip), peer.port, ctx)
        if s is not None :
            sockets.append({"socket" : s, "peer" : str(peer.ip) +":" + str(peer.port)})


    # #DEBUG
    # for socket in sockets :
    #     print(socket)  
    
    # #DEBUG : Publish only layer 0 block, which should be visible on the network instanly
    # s = handshake_peer(str(voting_peers[0].ip), voting_peers[0].port, ctx)
    # if s == None :
    #     print("socket is None")
    #     exit
    # print(forks[0][0])
    # blk = block_state.parse_from_json(forks[0][0])
    # assert(isinstance(blk, block_state))   
    # msg = msg_publish(hdr, blk)            
    # s.send(msg.serialise())
    # print(msg)
    # print("\n")
    # print("Hash published: {} for account: {}".format(hexlify(blk.hash()), acctools.to_account_addr(blk.account)))
    
    for blocks_in_layer in reversed(forks) : #send order reversed : layer_3--> layer_2 -->layer_1 --> sleep(n) --> layer_0
        current_layer = forks.index(blocks_in_layer)
        next_peer = 0
        if current_layer == 0:
            print("Waiting for 30 seconds before sending layer_0 forks")
            time.sleep(30)

        for block in blocks_in_layer :           
                  
            blk = block_state.parse_from_json(block)
            assert(isinstance(blk, block_state)) 
            msg = msg_publish(hdr, blk) 

            if current_layer == 0 :
                #send layer_0 blocks to 2 different peers
                s = sockets[next_peer]
                s["socket"].send(msg.serialise())
                next_peer = next_peer + 1                
            else :
                ## TESTING : #send fork blocks to all voting peers --> result : one chain is confimred immediately 
                # for s in sockets:                 #     
                #     s["socket"].send(msg.serialise())
                #     print("Hash published: {} for account: {} to peer {}".format(hexlify(blk.hash()), acctools.to_account_addr(blk.account), s["peer"]))

                ## TESTING : #send fork blocks to ONE voting peer only --> result : blocks of deeper layers propagate much more slowly.
                s = random.choice(sockets)           
                s["socket"].send(msg.serialise()) #send                
            print("Hash published: {} for account: {} to peer {}".format(hexlify(blk.hash()), acctools.to_account_addr(blk.account), s["peer"]))

if __name__ == '__main__':
    
    main()






    
