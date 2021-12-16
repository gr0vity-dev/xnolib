 
import requests
import json
import secrets
import math
import time
import logging
import os
import random


scriptPath = os.path.abspath(os.path.dirname(__file__))

class Api:

    
    # api_config = None
    # debug = False
    account_info_inmemory = { "nano_address" : {"frontier" : "...", "balance" : "..." , "representative": "..."}}
    
   
    def __init__(self, url, debug=True, forks = False): 
        self.forks = forks      
        self.debug = debug
        self.RPC_URL = url
    
    def post_with_auth(self, content, max_retry=2):
        try :
            url = self.RPC_URL 
            headers = {"Content-type": "application/json", "Accept": "text/plain"}    
            r = requests.post(url, json=content, headers=headers)
            # print("request: {} \rrepsonse: {}".format(content["action"], r.text ))
            if "error" in r.text:
                if self.debug : print("error in post_with_auth |\n request: \n{}\nresponse:\n{}".format(content, r.text)) 
            return json.loads(r.text)
        except : 
            if self.debug : print("{} Retrys left for post_with_auth : {}".format(max_retry, content["action"]))
            max_retry = max_retry - 1   
            if max_retry >= 0 : 
                time.sleep(0.1)  #100ms
                self.post_with_auth(content,max_retry)
 

    def generate_seed(self):
        return secrets.token_hex(32)

    def generate_new_seed(self):
        return {'success': True,
                'seed': self.generate_seed(),
                'error_message': ''}

    def validate_seed(self, seed):
        result = {
            'seed': seed,
            'success': False,
            'error_message': ''
        }
        if len(seed) == 64:
            try:
                int(seed, 16)
                result['success'] = True

            except Exception:
                result['error_message'] = 'Wrong seed format'
        else:
            result['error_message'] = 'Wrong seed length'

        return result
    
    def get_account_data(self, seed):
        payload = self.generate_account(seed, 0)
        payload["success"] = True
        payload["error_message"] = ''
        
        return payload

    def get_account_data(self, seed, index):
        payload = self.generate_account(seed, index)
        payload["success"] = True
        payload["error_message"] = ''
        
        return payload

    def generate_account(self, seed, index):
        
        req_deterministic_key = {
            "action": "deterministic_key",
            "seed": seed,
            "index": str(index),
        }
        account_data = self.post_with_auth(req_deterministic_key)
        
        account_data = {
            "seed": seed,
            "index": index,
            "private": account_data["private"],
            "public": account_data["public"],
            "account": account_data["account"],
            "nano_prefix": account_data["account"][0:11],
            "nano_center": account_data["account"][11:59],
            "nano_suffix": account_data["account"][len(account_data["account"]) - 6:]            
        }
        req_account_balance = {
            "action": "account_balance",
            "account" : account_data["account"]
        }
        account_balance = self.post_with_auth(req_account_balance)
        account_data["balance"] = account_balance["balance"]
        account_data["receivable"] = account_balance["receivable"]

        return account_data

    def validate_account_number(self, account):
        response = {"success" : False}
        req_validate_account_number = {
            "action": "validate_account_number",
            "account": account,
        }
        data = self.post_with_auth(req_validate_account_number)        
        if data["valid"] == "1" :
            response["success"] = True            
        return response

    def unlock_wallet(self, wallet, password):
        response = {"success" : False}
        req_password_enter = {
        "action": "password_enter",
        "wallet": wallet,
        "password": password
        }
        data = self.post_with_auth(req_password_enter)
        
        if data["valid"] == "1" :
            response["success"] = True            
        return response
    
    def get_ledger(account, count):
        req_get_ledger = {
            "action": "ledger",
            "account": account,
            "count": str(count)
            }
        return self.post_with_auth(req_get_ledger)

    def get_chain(self,frontier, count):
        req_get_chain = {
            "action": "chain",
            "block": frontier,
            "count": str(count)
        }
        return self.post_with_auth(req_get_chain)
    
    def get_telemetry(self, raw) :
        req_get_telemetry = {
        "action": "telemetry",
        "raw" : "true"
        }
        return self.post_with_auth(req_get_telemetry)
        

    def get_node_id(self) :
        req_node_id = {
        "action": "node_id",
        }
        return self.post_with_auth(req_node_id)      


    def wallet_create(self, seed):
        # response = {"success" : False}
        if seed == None :
            req_wallet_create = {
            "action": "wallet_create"
        }
        else :
            req_wallet_create = {
                "action": "wallet_create",
                "seed": seed,
            }
        return self.post_with_auth(req_wallet_create)           
        # {
        #     "wallet": "646FD8B5940AB5B1AD2C0B079576A4CF5A25E8ADB10C91D514547EF5C10C05B7",
        #     "last_restored_account": "nano_3mcsrncubmquwcwgiouih17fjo8183t497c3q9w6qtnwz8bp3fig5x8m4rkw",
        #     "restored_count": "1"
        # }          
        

    def wallet_add(self, wallet, private_key) :
        # response = {"success" : False}
        req = {
            "action": "wallet_add",
            "wallet": wallet,
            "key": private_key
        }
        return self.post_with_auth(req)
        
        # {
        #   "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        # }       
        
        
    def key_expand(self, private_key):        
        req = {
            "action": "key_expand",
            "key": private_key
        }
        return self.post_with_auth(req)
          

    def get_block_count(self):        
        req = {
            "action": "block_count"
        }
        return self.post_with_auth(req)

    def get_block_info(self, block_hash):        
        req = {
            "action": "block_info",
            "hash" : block_hash,
            "json_block" : "true"
        }
        return self.post_with_auth(req)   

    def get_block_hash(self, json_block):        
        req = {
            "action": "block_hash",            
            "json_block" : "true",
            "block" : json_block
        }
        return self.post_with_auth(req)     

    def get_stats(self):        
        req = {
            "action": "stats",
            "type": "counters"
        }
        return self.post_with_auth(req)
              

    def check_balance(self, account):
       
        multiplier = 10 ** 30
        req_account_balance = {
            "action": "account_balance",
            "account": account,
        }
        data = self.post_with_auth(req_account_balance)
              
        return {"account": account, 
                "balance_raw" : int(data["balance"]), 
                "balance": self.truncate(int(data["balance"]) / multiplier), 
                "pending": self.truncate(int(data["pending"]) / multiplier), 
                "total": self.truncate((int(data["balance"]) + int(data["pending"])) / multiplier)}

    def get_account_info(self, account):
       
        req_account_info = {
            "action": "account_info",
            "account": account,
            "representative": "true",
            "pending": "true",
            "include_confirmed": "true",
            "weight": "true"
        }
        account_info = self.post_with_auth(req_account_info)        
       
        return account_info

    def check_balances(self, seed):
        # check if there is any balance for account 0 to 50 accounts
        # {'index' : '' , 'account': '', 'balance': '', 'pending': ''}  ; spendable, total  Balance : 100 Nano . ! 95 Nano are currently not spendable. Your action is required.
        result = []
        for index in range(0, 51):
            nano_account = self.generate_account(seed, index)
            result.append(self.check_balance(nano_account["account"]))

    def truncate(self, number):
        if number > 0 :            
            return str('{:8f}'.format(number))
        else :
            return "0.00"

    def get_pending_blocks(
        self,
        nano_account,
        threshold,
        number_of_blocks
    ) :

        response = {"account" : nano_account,
                    "blocks" : None,
                    "success" : True,
                    "error_message" : "" }

        req_accounts_pending = {
            "action": "accounts_pending",
            "accounts": [nano_account],
            "threshold" : str(threshold),
            "sorting" : "true",
            "count": str(number_of_blocks)
        }       
        accounts_pending = self.post_with_auth(req_accounts_pending)
       

        if "error" in accounts_pending:
            response["success"] = False
            response["error_message"] = accounts_pending["error"]
        elif accounts_pending["blocks"][nano_account] == "" :        
            response["success"] = False
            response["error_message"] = "no pending blocks"
        else :
            response["blocks"] = accounts_pending["blocks"][nano_account]
        
        return response

    def get_frontier(self, account):
        req_frontiers = {
            "action": "frontiers",
            "account": account,
            "count": "1",
        }
        return self.post_with_auth(req_frontiers)      
        
    
    def get_account_frontier(self,account):
        req_accounts_frontiers = {
            "action": "accounts_frontiers",
            "accounts": [account]
        }
        return self.post_with_auth(req_accounts_frontiers) 


    def set_account_info_inmemory(self, hash, account,next_hash,balance,rep_account, block_type="unset" ):  
        self.account_info_inmemory[account] = {"frontier" : next_hash, "balance" : balance, "representative" : rep_account  }  

    def publish_block(self, block_create_response) :
        req_process = {
            "action": "process",
            "json_block": "true",
            "subtype": block_create_response["subtype"],
            "block": block_create_response["block"],
        }
        return self.post_with_auth(req_process)      
           

    def create_receive_block_seed(
        self,
        open_seed,
        open_index,
        amount_per_chunk_raw,
        rep_account,
        send_block_hash,
        broadcast = 1
    ):
        if self.debug : t1 = time.time() 
        req_source_account = {
            "action": "deterministic_key",
            "seed": open_seed,
            "index": str(open_index),
        }
        if self.debug : logging.info("req_source_account : {}".format(time.time() - t1))
        if self.debug : t1 = time.time() 
        source_account_data = self.post_with_auth(req_source_account)     

        return self.create_receive_block(  source_account_data["account"],
                                        source_account_data["private"],
                                        amount_per_chunk_raw,
                                        rep_account,
                                        send_block_hash,
                                        broadcast
                                        )

  
    def create_receive_block(
        self,
        destination_account,
        open_private_key,
        amount_per_chunk_raw,
        rep_account,
        send_block_hash,
        broadcast = 1,
        parallel = False
    ):

        req_account_info = {
            "action": "account_info",
            "account": destination_account,
            "representative": "true",
            "pending": "true",
            "include_confirmed": "true"
        }
        account_info = self.post_with_auth(req_account_info)       

        if "error" in account_info:
            subtype = "open"
            previous = "0000000000000000000000000000000000000000000000000000000000000000"
            balance = str(amount_per_chunk_raw)
            
            if broadcast != 1 and destination_account in self.account_info_inmemory and self.forks == False :
                subtype = "receive" 
                previous = self.account_info_inmemory[destination_account]["frontier"]
                balance = str(int(self.account_info_inmemory[destination_account]["balance"]) + int(amount_per_chunk_raw))
            # else :
            #     if self.debug : print("error in create_receive_block [subtype=open]\n source_account : {} \naccount_info response: {}\n{}".format(destination_account,account_info,self.account_info_inmemory ))
        else:            
            subtype = "receive"  
            previous = account_info["frontier"]        
            balance = str(int(account_info["confirmed_balance"]) + int(amount_per_chunk_raw))               

        # prepare open/receive block
        req_block_create = {
            "action": "block_create",
            "json_block": "true",
            "type": "state",
            "balance": balance,
            "key": open_private_key,
            "representative": rep_account,
            "link": send_block_hash,
            "previous": previous
            # ,"difficulty": difficulty,
        }
        
        create_block_response =  self.post_with_auth(req_block_create)
        create_block_response["subtype"] = subtype

        if broadcast == 1 :
            self.publish_block(create_block_response)
            return create_block_response
        
        self.set_account_info_inmemory(create_block_response["hash"], destination_account, create_block_response["hash"],balance,rep_account, create_block_response["subtype"])
        return create_block_response


    def create_send_block_seed(
        self,
        source_seed,
        source_index,
        destination_account,
        amount_per_chunk_raw,
        broadcast = 1
    ):
        if self.debug : t1 = time.time() 
        req_source_account = {
            "action": "deterministic_key",
            "seed": source_seed,
            "index": source_index,
        }
        source_account_data = self.post_with_auth(req_source_account)      
        if self.debug : logging.info("req_source_account : {}".format(time.time() - t1))
        if self.debug : t1 = time.time() 

        return self.create_send_block(  source_account_data["account"],
                                        source_account_data["private"],
                                        destination_account,
                                        amount_per_chunk_raw,
                                        broadcast)

    def create_send_block(
        self,
        source_account,
        source_private_key,
        destination_account,
        amount_per_chunk_raw,
        broadcast = 1
    ):
        if self.debug : t1 = time.time() 
       
        source_account_data = {    
            "private": source_private_key,
            "account": source_account,
        }

        req_account_info = {
            "action": "account_info",
            "account": source_account_data["account"],
            "representative": "true",
            "pending": "true",
            "include_confirmed": "true"
        }
        account_info = self.post_with_auth(req_account_info)
        
        if "error" in account_info:     
                if self.debug : print("error in create_send_block\n source_account : {} \naccount_info response: {}\n{}".format(source_account,account_info,self.account_info_inmemory))          
        else :
            source_previous = account_info["frontier"]
            source_balance = account_info["balance"]
            current_rep = account_info["representative"]

        if broadcast != 1 and source_account in self.account_info_inmemory :
            source_previous = self.account_info_inmemory[source_account]["frontier"]
            source_balance = self.account_info_inmemory[source_account]["balance"]
            current_rep = self.account_info_inmemory[source_account]["representative"]
            if self.debug : print("account_info_inmemory: " , source_account, source_balance) 

        
        if self.debug : logging.info("post_with_auth : {}".format(time.time() - t1))
        if self.debug : t1 = time.time() 

        
        req_destination_key = {"action": "account_key",
                               "account": destination_account}
        destination_link = self.post_with_auth(req_destination_key)["key"]
        
        if self.debug : logging.info("req_destination_key : {}".format(time.time() - t1))
        if self.debug : t1 = time.time() 

        # prepare send block
        block_balance = str(int(source_balance) - int(amount_per_chunk_raw))
        req_block_create = {
            "action": "block_create",
            "json_block": "true",
            "type": "state",
            "balance": str(block_balance),
            "key": source_account_data["private"],
            "representative": current_rep,
            "link": destination_link,
            "link_as_account": destination_account,
            "previous": source_previous
            # ,"difficulty": difficulty,
        }

        create_block_response =  self.post_with_auth(req_block_create)
        create_block_response["subtype"] = "send"

        if broadcast == 1 :
            self.publish_block(create_block_response)
            return create_block_response

        
        self.set_account_info_inmemory(create_block_response["hash"], source_account_data["account"], create_block_response["hash"],block_balance,current_rep, create_block_response["subtype"])
        return create_block_response
    
       

    def create_change_block_seed(
        self,
        source_seed,
        source_index,
        new_rep,
        random_reps,
        broadcast = 1

    ):  
        if self.debug : t1 = time.time()  
        req_source_account = {
            "action": "deterministic_key",
            "seed": source_seed,
            "index": source_index,
        }
        source_account_data = self.post_with_auth(req_source_account)
        if self.debug : logging.info("req_source_account : {}".format(time.time() - t1))
        if self.debug : t1 = time.time() 

       
        source_account_data = {
            "seed": source_seed,
            "index": source_index,
            "private": source_account_data["private"],
            "public": source_account_data["public"],
            "account": source_account_data["account"],
        }

        req_account_info = {
            "action": "account_info",
            "account": source_account_data["account"],
            "representative": "true",
            "pending": "true",
            "include_confirmed": "true"
        }
        account_info = self.post_with_auth(req_account_info)
        
        if self.debug : logging.info("post_with_auth : {}".format(time.time() - t1))
        if self.debug : t1 = time.time() 

        source_previous = account_info["frontier"]
        source_balance = account_info["balance"]
        current_rep = account_info["representative"]

        if random_reps != None :
            new_rep = random.choice(random_reps)
            while new_rep == current_rep: #make sure to set a new rep each time
                new_rep = random.choice(random_reps)
        

        # prepare change block
        req_block_create = {
            "action": "block_create",
            "json_block": "true",
            "type": "state",
            "balance": str(source_balance),
            "key": source_account_data["private"],
            "representative": new_rep,
            "link": "0000000000000000000000000000000000000000000000000000000000000000",
            "link_as_account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
            "previous": source_previous,
        }        

        create_block_response =  self.post_with_auth(req_block_create)
        create_block_response["subtype"] = "change"

        if broadcast == 1 :
            self.publish_block(create_block_response)  
            return create_block_response      
        
        return create_block_response       

       

