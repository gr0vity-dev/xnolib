#!/bin/env python3
#
# PREREQUISITE : Access to a nano_node with RPC control_enabled = true
#
# >>> How to use this script 
# python3 gr0_fork_publish.py --source_seed=0000000000000000000000000000000000000000000000000000000000000106 --rpc_url=http://localhost:55000
# python3 gr0_conf_duration_tester.py --start_index=1 --accs=2 --tx_per_acc=2 --tps=5 --amount_raw=1 --source_seed=0000000000000000000000000000000000000000000000000000000000000106
#
# >>>What does the script do ?
# Precompute a number of blocks (send + receive), broadcast the blocks to the network at a configurable rate and monitor the duration before the block is confirmed. 
# All monitoring data is stored in sqlite3 file (gr0_tools/sqlite3/conf_duration.db)
# 
#
# >>> How can I see the results ?
# $cd gr0_tools/sqlite3/
# python3 gr0_tools/sqlite3/select.py --session_id={} --show=1 #list all commands per block [publish, ws_new_unconfirmed_block, ws_confirmation, rpc_block_info_confirmed]
# python3 gr0_tools/sqlite3/select.py --session_id={} --show=2 #list account stats, tx_count and bucket used
# python3 gr0_tools/sqlite3/select.py --session_id={} --show=3 #list confirmation stats , min,max and average Conf times for a session
# python3 gr0_tools/sqlite3/select.py --session_id={} --show=4 #list unconfirmed blocks (when script is still running)


from pynanocoin import *
from peercrawler import *
from msg_handshake import node_handshake_id
import argparse
import requests
import json
import time
from gr0_tools.nano_rpc import Api
import websocket
import sqlite3
import os
import threading
import math
from datetime import datetime

db_filename = './gr0_tools/sqlite3/conf_duration.db'
schema_filename = './gr0_tools/sqlite3/conf_duration_schema.sql'
conn = None
session_id = None
ws = None
api = None


def is_new_session():
    cur = conn.cursor()
    query = """ select * 
                from block_conf_stats
                where session_id = '{}' """.format(session_id)
    row = cur.execute(query).fetchone()
    # row = cursor.fetchone()
    if row is None :
        return True
    else :
        raise ValueError('session_id {} already exists'.format(session_id))

def insert_block_command(block_hash,command,delta_command):
    try:
        cur = conn.cursor()
        query = """ select command_ts, ((julianday('now') - 2440587.5)*86400.0) 
                    from block_command
                    where session_id = '{}' and block_hash = '{}' and command = '{}'""".format(session_id, block_hash, delta_command)
        row = cur.execute(query).fetchone()
        # row = cursor.fetchone()
        if row is None :
            delta_command_tdiff = 0
        else:
            delta_command_ts = int(row[0] * 1000)
            current_ts = int(1000* row[1])
            delta_command_tdiff = current_ts - delta_command_ts
        # print(delta_command_tdiff)

        query = "INSERT INTO block_command (session_id, block_hash,command, delta_command_tdiff, delta_command) values (?,?,?,?,?) "
        res = cur.execute(query, (session_id, block_hash, command,delta_command_tdiff,delta_command ))
        # conn.commit()
    except Exception as ex:
        print(str(ex))

def update_block_conf_stats(prop_key,prop_value):
    query = """INSERT INTO block_conf_stats (session_id, prop_key, prop_value) VALUES( ?, ? ,?)
                ON CONFLICT(session_id,prop_key) DO UPDATE SET prop_value= ?"""
    conn.cursor().execute(query, (session_id, prop_key, prop_value, prop_value))
    # conn.commit()

def inc_block_conf_stats(prop_key, inc = 1):
    query = """INSERT INTO block_conf_stats (session_id, prop_key, prop_value) VALUES( ?, ? ,?)
                ON CONFLICT(session_id,prop_key) DO UPDATE SET prop_value = prop_value + ?"""
    conn.cursor().execute(query, (session_id, prop_key, inc, inc))
    # conn.commit()

def inc_block_conf_account_stats(account, bucket_last_tx, inc = 1):
    query = """INSERT INTO block_conf_account_stats (session_id, account, bucket_last_tx, tx_count) VALUES( ?, ? ,?, ?)
                ON CONFLICT(session_id,account) DO UPDATE SET bucket_last_tx = ? , tx_count = tx_count + ?"""
    conn.cursor().execute(query, (session_id, account,bucket_last_tx, inc, bucket_last_tx, inc))
    # conn.commit()


class Ws_client: 

    req_counter = {
        "message" : 0,
        "new_unconfirmed_block": 0,
        "new_unconf_blk_not_in_session": 0,
        "confirmation": 0,
        "stopped_election": 0,
        "subscribed_account" : 0
    } 

    account_filter = []     
    
    def __init__(self, ws_url, rpc_url, session_id):
        self.api = Api(rpc_url, debug= False)
        self.ws = websocket.WebSocketApp(ws_url,
                    on_message = lambda ws,msg: self.on_message(ws, msg),
                    on_error   = lambda ws,msg: self.on_error(ws, msg),
                    on_close   = lambda ws:     self.on_close(ws),
                    on_open    = lambda ws:     self.on_open(ws))
        # self.ws.run_forever()
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def on_message(self, ws, message):
            msg = json.loads(message)
            print(msg)

    def topic_selector(self, message):
        json_msg = json.loads(message)

        if json_msg["topic"] == "confirmation":
            self.p_confirmation(json_msg)
        elif json_msg["topic"] == "new_unconfirmed_block":
            self.p_new_unconfirmed_block(json_msg)
        elif json_msg["topic"] == "stopped_election":
            self.p_stopped_election(json_msg)
        # elif json_msg["topic"] == "started_election":
        #     p_started_election(json_msg)
        else:
            print("select else")

    def p_stopped_election(self, json_msg):
        self.req_counter["stopped_election"] = self.req_counter["stopped_election"] + 1          

    def update_ws_accounts(self, accounts) :
        self.account_filter = self.account_filter + accounts #build custom filter for p_new_unconfirmed_block
        self.req_counter["subscribed_account"] = self.req_counter["subscribed_account"] + len(accounts)       
        self.ws.send(
            json.dumps(
                {   "action": "update",
                    "topic": "confirmation",
                    "options": {
                        "accounts_add": accounts,
                    }
                }))

    def p_confirmation(self, json_msg):
        self.req_counter["confirmation"] = self.req_counter["confirmation"] + 1
        # print("p_confirmation\n" ,json_msg)    
        insert_block_command(json_msg["message"]["hash"],'ws_confirmation', 'publish'  )
        inc_block_conf_stats("ws_confirmation")

    def p_new_unconfirmed_block(self, json_msg):
        if json_msg["message"]["account"] in self.account_filter :        
            self.req_counter["new_unconfirmed_block"] = self.req_counter["new_unconfirmed_block"] + 1    
            # print("p_new_unconfirmed_block\n" ,json_msg) 
            block_hash = self.api.get_block_hash(json_msg["message"]) 
            insert_block_command(block_hash["hash"],'ws_new_unconfirmed_block', 'publish'  )  
            inc_block_conf_stats("ws_new_unconfirmed_block")
        else :
            self.req_counter["new_unconf_blk_not_in_session"] = self.req_counter["new_unconf_blk_not_in_session"] + 1 
            inc_block_conf_stats("ws_new_unconf_blk_not_in_session")  

    def on_message(self, ws, message):
        self.req_counter["message"] = self.req_counter["message"] + 1    
        self.topic_selector(message)

    def on_error(self, ws, error):              
        print(error)

    def on_close(self, ws):         
        print("### websocket connection closed ###")

    def terminate(self) : 
        print("websocket thread terminating...")  
        try:
            print("_" * 80)
            print("message count per topic for session '{}':".format(session_id))
            print("-" * 80)
            print(self.req_counter)
            print("-" * 80) 
        except Exception as ex:
            print("Error on close while printing stats" , str(ex))  
        self.ws.close()
               

    def on_open(self, ws):
        self.ws.send(json.dumps({"action": "subscribe", "topic": "new_unconfirmed_block"}))
        self.ws.send(
            json.dumps(
                {
                    "action": "subscribe",
                    "topic": "confirmation",
                    "options": {
                        "include_election_info": "false",
                        "include_block": "true",
                        "accounts": []
                    },
                }
            )
        )
        # ws.send(json.dumps({"action": "subscribe", "topic": "confirmation", "options": {"include_election_info": "true"}}))
        print("### websocket connection opened ###")
       

def create_blocks(args): 
    start_time = time.time()

    block_list = []   
    # -------------- 0) START -------------------------    
    source_seed = args.source_seed 
    if args.session_id is not None : 
        dest_seed = api.generate_seed()
        print("session_id: {} | destination_seed: {}".format(session_id, dest_seed))   
    else:      
        dest_seed = session_id
        print("session_id == destination_seed: " , dest_seed)      
    

    block_counter= 0
    #if transactions per account > 1, repeat the block creation process [--tx_per_acc] times 
    for j in range(1,args.tx_per_acc+1) :
        #1 loop through accounts and create 1 send and 1 receive block
        for i in range(args.start_index,args.accs+args.start_index):                                      
            dest_data = api.get_account_data(dest_seed, i)            
            source_data = api.get_account_data(source_seed, i) 
            inc_block_conf_account_stats(source_data["account"], math.floor(math.log(int(source_data["balance"]), 2)))
            inc_block_conf_account_stats(dest_data["account"], math.floor(math.log(int(dest_data["balance"]) + args.amount_raw , 2)))
            
            
            if j == 1 : #add accounts to websockets                
                ws.update_ws_accounts([source_data["account"], dest_data["account"]])


            send_block = api.create_send_block_seed(source_seed, 
                                                    i, 
                                                    dest_data["account"], 
                                                    args.amount_raw,
                                                    broadcast = 0)                                                             
            inc_block_conf_stats("session_blocks_created", 1)                            
            
            receive_block = api.create_receive_block_seed(dest_data["seed"],
                                                            dest_data["index"],
                                                            args.amount_raw,
                                                            dest_data["account"],
                                                            send_block["hash"],
                                                            broadcast = 0) 
            inc_block_conf_stats("session_blocks_created", 1)           
            block_list.append(send_block)     #send_block["subtype"] is "send"                                        
            block_list.append(receive_block)  #receive_block["subtype"] is "open" or "receive" 
            
            block_counter = block_counter + 2
            print("Block counter : " , block_counter , end="\r")           

    time_lapsed = time.time() - start_time 
    # update_block_conf_stats("tps", (block_counter/time_lapsed) ) if args.rpc_process else update_block_conf_stats("tps", args.tps  )
    update_block_conf_stats("duration_s_create_blocks", time_lapsed)  
    return block_list
   

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


def publish_blocks(args, blocks):
    update_block_conf_stats("tps", args.tps)
    update_block_conf_stats("session_start_time_utc", datetime.utcnow()) 

    #Publish by sending block to all voting peers via script
    if args.rpc_process == True :
        start_time = time.time()
        count = 0     
        for block in blocks :
            if count % args.tps == 0 :
                print("Broadcasted '{}' blocks @ '{}' bps for session '{}'".format(count, args.tps, session_id), end="\r")
                time.sleep(1 - time.monotonic() % 1) 
            api.publish_block(block)
            insert_block_command(block["hash"],'publish', 'publish' )
            inc_block_conf_stats("publish")
            count = count + 1  
        print("Broadcasted '{}' blocks @ '{}' bps for session '{}'".format(count, args.tps, session_id))  
        update_block_conf_stats("duration_s_publish_blocks", (time.time() - start_time ))  
    update_block_conf_stats("peer_count", api.get_peer_count())
    #Publish by sending block to all voting peers via script
    if args.rpc_process == False :
        start_time = time.time()
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
        
        update_block_conf_stats("duration_s_peer_handshake", (time.time() - start_time ))
        update_block_conf_stats("peer_count", len(sockets))
        start_time = time.time()
        count = 0      
        for block in blocks :  
            if count % args.tps == 0 :
                print("Broadcasted '{}' blocks @ '{}' bps for session '{}'".format(count, args.tps, session_id), end="\r")
                time.sleep(1 - time.monotonic() % 1) 

            blk = block_state.parse_from_json(block["block"])
            assert(isinstance(blk, block_state)) 
            msg = msg_publish(hdr, blk) 
            
            ## TESTING : #send fork blocks to all voting peers --> result : one chain is confimred immediately 
            for s in sockets:                    
                s["socket"].send(msg.serialise())
                # print("Hash published: {} | {:<8} for account: {} to peer {}".format(hexlify(blk.hash()),block["subtype"], acctools.to_account_addr(blk.account), s["peer"]))
            # print("Hash published: {} | {:<8} for account: {} to {} peers".format(hexlify(blk.hash()),block["subtype"], acctools.to_account_addr(blk.account), len(sockets)), end="\r")
            insert_block_command(block["hash"],'publish', 'publish' )
            inc_block_conf_stats("publish")
            
            ## TESTING : #send fork blocks to ONE voting peer only --> result : blocks of deeper layers propagate much more slowly.
            # s = random.choice(sockets)           
            # s["socket"].send(msg.serialise()) #send                
            # print("Hash published: {} for account: {} to peer {}".format(hexlify(blk.hash()), acctools.to_account_addr(blk.account), s["peer"]))        
            count = count + 1  
        print("Broadcasted '{}' blocks @ '{}' bps for session '{}'".format(count, args.tps, session_id))  
        update_block_conf_stats("duration_s_publish_blocks", (time.time() - start_time ))    
    return

def get_conf_status(args, blocks):
    start_time_tot = time.time()
    unconfirmed_count = len(blocks)
    unconfirmed_blocks = blocks[:]
    max_sleep_per_iteration = 30
    min_sleep_per_iteration = 5
    itercount = 0
    while unconfirmed_count > 0 : 
        itercount = itercount + 1       
            
        missing_blocks = "missing in ledger: "    
        blocks = unconfirmed_blocks[:]
        unconfirmed_blocks = []
        missing_in_ledger = []
        start_time = time.time()
        sleep_per_iteration = max( min_sleep_per_iteration , min(max_sleep_per_iteration, unconfirmed_count/ (args.accs*2)))
        for block in blocks :
            block_info = api.get_block_info(block["hash"])
            try: 
                if block_info["confirmed"] == "true" :
                    insert_block_command(block["hash"],'rpc_block_info_confirmed', 'publish' )
                    inc_block_conf_stats("rpc_block_info_confirmed")
                else :
                    unconfirmed_blocks.append(block)
            except Exception as ex:                
                missing_in_ledger.append(block["hash"]) #can only happen if we broadcast it to peers via script. RPC process call adds to own ledger automatically 
                unconfirmed_blocks.append(block)

        update_block_conf_stats("duration_s_rpc_block_info", (time.time() - start_time )) 
        inc_block_conf_stats("iter_count_rpc_block_info", 1)
        confirmed_in_iteration = unconfirmed_count - len(unconfirmed_blocks)
        unconfirmed_count = len(unconfirmed_blocks)
        if unconfirmed_count == 0 : 
            sleep_per_iteration = 0 # don't sleep but still log advancement
            missing_in_ledger = []
        print("{} blocks unconfirmed. {} confirmed in iteration. missing in ledger : {}. Sleeping for {} seconds {}".format(
                unconfirmed_count,    confirmed_in_iteration,    len(missing_in_ledger),  sleep_per_iteration, ("." * itercount)), end="\r")
        time.sleep(sleep_per_iteration) 
    update_block_conf_stats("conf_duration_after_publish", time.time() - start_time_tot )
    return       

def check_for_late_websocket_messages():    
    sleep = True
    sleep_per_iteration = 10
    sleep_before_quit = 60 * 10 # 10 minutes
    cur = conn.cursor()
    itercount = 0
    while sleep :
        itercount = itercount + 1
        sleep = False
        msg = ""
        q = "SELECT prop_value FROM block_conf_stats WHERE session_id = '{}' AND prop_key = 'publish'".format(session_id)
        publish = int(cur.execute(q).fetchone()[0])        
        q = "SELECT prop_value FROM block_conf_stats WHERE session_id = '{}' AND prop_key = 'ws_new_unconfirmed_block'".format(session_id)
        ws_new_unconfirmed_block = int(cur.execute(q).fetchone()[0])
        q = "SELECT prop_value FROM block_conf_stats WHERE session_id = '{}' AND prop_key = 'ws_confirmation'".format(session_id)
        ws_confirmation = int(cur.execute(q).fetchone()[0])

        if ws_new_unconfirmed_block < publish :
            sleep = sleep + True 
            msg = msg + "{}/{} ws_new_unconfirmed_block.".format(ws_new_unconfirmed_block, publish)
                       
            
        
        if ws_confirmation < publish:
            sleep = sleep + True   
            msg = msg + "{}/{} ws_confirmation.".format(ws_confirmation, publish)
        
        if sleep_per_iteration * itercount >= sleep_before_quit :
            print("FAILED : Waiting for later confirmtions timed out after {} minutes".format(sleep_before_quit / 60))
            update_block_conf_stats("late_ws_new_unconfirmed_block", publish - ws_new_unconfirmed_block )
            update_block_conf_stats("late_ws_confirmation", publish - ws_confirmation )
            update_block_conf_stats("late_websocket_messages_timeout", "true" ) 
            sleep = False

        if sleep :
            print(msg + " Sleeping for {} seconds {}".format(sleep_per_iteration, ("." * itercount)), end= "\r") 
            time.sleep(sleep_per_iteration) 
    return
                


def create_db(db_is_new):
    
    if db_is_new:
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
 



def main():
    global api, session_id, ws, conn
    

    parser = argparse.ArgumentParser(description="Echo your input")
    #default sourec seed : 0000000000000000000000000000000000000000000000000000000000000106 
    #default account at index 0 : nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm

    # Add a position-based command with its help message.
    parser.add_argument("--source_seed", help="Seed to derive source addresses")
    parser.add_argument("--start_index", type=int, help="Default : 0 | seed_index at which send blocks will be started up to '--start_index' + '--accs' . Default : 0")
    parser.add_argument("--accs", type=int, help="Default : 1 | Number of accounts used to create send blocks. Your '--source_seed' must hold funds for these accounts")
    parser.add_argument("--tx_per_acc",type=int, help="Default : 2 | Number of blocks created per account")
    parser.add_argument("--tps", type=int, help="Default : 10 | broadcast at '--tps' transactions per second")
    # parser.add_argument("--source_index", type=int, help="Seed to derive source addresses")  
    parser.add_argument("--rpc_url" ,help="Default : http://localhost:55000")
    parser.add_argument("--ws_url" ,help="Default : ws://localhost:57000")
    parser.add_argument("--amount_raw", type=int ,help="Default : 1 | Amount that is passed between accounts")    
    parser.add_argument("--rpc_process", help="Default : true | If true, use nano_node process rpc command to publish blocks. Else python script is used to broadcast to all voting peers ")  
    parser.add_argument("--session_id", help="Choose a unique session_id . 64 random characters by default")    

    # Use the parser to parse the arguments.
    args = parser.parse_args()   
        
    if args.rpc_url == None : args.rpc_url = "http://localhost:55000"
    if args.ws_url == None : args.ws_url = "ws://localhost:57000"    
    if args.source_seed == None : args.source_seed = "0000000000000000000000000000000000000000000000000000000000000106" 
    if args.start_index == None : args.start_index = 0   
    if args.amount_raw == None : args.amount_raw = 1 
    if args.tps == None : args.tps = 10 
    if args.accs == None : args.accs = 1 
    if args.tx_per_acc == None : args.tx_per_acc = 2
    if args.rpc_process == None : args.rpc_process = "true"
    args.rpc_process = True if args.rpc_process == "true" else False     
        
    api = Api(args.rpc_url, debug=False, forks=False) #reset api instance for each fork chain. Blocks are saved in memory per instance. 
    
    if args.session_id == None:
        session_id = api.generate_seed() 
    else : 
        session_id = args.session_id           
    ws = Ws_client(args.ws_url,args.rpc_url, session_id)
    print(">>>Sending '{}' blocks from seed '{}'".format(args.accs * args.tx_per_acc * 2, args.source_seed)) 
    db_is_new = not os.path.exists(db_filename)
    conn = sqlite3.connect(db_filename, check_same_thread=False, isolation_level=None)
    create_db(db_is_new)  
    is_new_session()
    update_block_conf_stats("estimated_session_block_count", args.tx_per_acc * args.accs * 2 )
    update_block_conf_stats("tps", args.tps )

    blocks = create_blocks(args)

    start_time = time.time()
    publish_blocks(args, blocks)
    get_conf_status(args, blocks)
    update_block_conf_stats("pub_and_conf_duration_total", time.time() - start_time)  
    check_for_late_websocket_messages()     
    
    ws.terminate()



if __name__ == '__main__':    
    

    main()







    
