
#sqlite3_select_tasks.py
#How to use :
#>>> Show stats for all past sessions
#python3 select.py

#>>> Show stats for last N past sessions:
#python3 select.py --limit=N

#>>> Show stats for last 1 session:
#python3 select.py --limit=1 

#Show session stats for specific session
#python3 select.py --session_id={session_id} --show=3 

#Show session stats for the last session
#python3 select.py --session_id $( python3 select.py --limit 1 | awk  'NR==5 {print $2}') --show 3

import sqlite3
import argparse
import pandas as pd

db_filename = 'conf_duration.db'
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()


def select_conf_duration_stats(limit, show_session):
    select_session = "t1.session_id," if show_session else ""
    return """SELECT {}
                     t1.block_count,
                     t2.accounts_used, 
                     t1.avg_conf_t, 
                     t1.min_conf_t, 
                     t1.max_conf_t,
                     bcs2.prop_value as broadcast_tps,
                     bcs3.prop_value as peers, 
                     bcs.prop_value as publish_start_utc,
                     bcs1.prop_value as publish_end_utc,
                     bcs4.prop_value as conf_end_utc 
              FROM ( SELECT session_id, 
                            min(CAST(delta_command_tdiff as FLOA))/1000 as min_conf_t, 
                            max(CAST(delta_command_tdiff as FLOA))/1000 as max_conf_t, 
                            avg(delta_command_tdiff)/1000 as avg_conf_t, 
                            count(command) as block_count 
                     FROM block_command bc 
                     WHERE command = 'ws_confirmation' 
                     GROUP BY session_id
                     ORDER BY command_ts DESC
                     LIMIT {}) as t1 
              LEFT JOIN block_conf_stats bcs on bcs.session_id = t1.session_id and bcs.prop_key = 'start_time_utc_publish' 
              LEFT JOIN block_conf_stats bcs1 on bcs1.session_id = t1.session_id and bcs1.prop_key = 'end_time_utc_publish'
              LEFT JOIN block_conf_stats bcs4 on bcs4.session_id = t1.session_id and bcs4.prop_key = 'end_time_utc_conf_rpc'   
              LEFT JOIN block_conf_stats bcs2 on bcs2.session_id = t1.session_id and bcs2.prop_key = 'tps' 
              LEFT JOIN block_conf_stats bcs3 on bcs3.session_id = t1.session_id and bcs3.prop_key = 'peer_count'
              LEFT JOIN ( SELECT session_id, 
                                 count(*) as accounts_used 
                          FROM block_conf_account_stats 
                          GROUP BY session_id) as t2 on t2.session_id = t1.session_id;""".format(select_session,limit)

def select_conf_duration_stats_2(limit):
    
    return """SELECT substr(t1.session_id,0,10),
                     t1.block_count,
                     t1.subtype as block_type,
                     t2.accounts_used as session_accounts, 
                     t1.avg_conf_t, 
                     t1.min_conf_t, 
                     t1.max_conf_t,
                     bcs2.prop_value as broadcast_tps,
                     bcs3.prop_value as peers, 
                     t1.first_conf,
                     t1.last_conf,
                     bcs.prop_value as utc_start_publish,
                     bcs1.prop_value as utc_end_publish,
                     bcs4.prop_value as utc_end_confirmations  
              FROM ( SELECT bc.session_id,
                            count(command) as block_count ,
                            min(CAST(delta_command_tdiff as FLOA))/1000 as min_conf_t, 
                            max(CAST(delta_command_tdiff as FLOA))/1000 as max_conf_t, 
                            min(DATETIME(command_ts, 'unixepoch')) as first_conf, 
                            max(DATETIME(command_ts, 'unixepoch')) as last_conf, 
                            avg(delta_command_tdiff)/1000 as avg_conf_t, 
                            bc.subtype
                        FROM block_command bc                                        
                        WHERE command = 'ws_confirmation' 
                        GROUP BY bc.session_id, bcs1.prop_value
                        ORDER BY bc.command_ts DESC
                     LIMIT {}) as t1 
              LEFT JOIN block_conf_stats bcs on bcs.session_id = t1.session_id and bcs.prop_key = 'start_time_utc_publish'  
              LEFT JOIN block_conf_stats bcs1 on bcs1.session_id = t1.session_id and bcs1.prop_key = 'end_time_utc_publish'
              LEFT JOIN block_conf_stats bcs4 on bcs4.session_id = t1.session_id and bcs4.prop_key = 'end_time_utc_conf_rpc'  
              LEFT JOIN block_conf_stats bcs2 on bcs2.session_id = t1.session_id and bcs2.prop_key = 'tps' 
              LEFT JOIN block_conf_stats bcs3 on bcs3.session_id = t1.session_id and bcs3.prop_key = 'peer_count'
              LEFT JOIN ( SELECT session_id, 
                                 count(*) as accounts_used 
                          FROM block_conf_account_stats 
                          GROUP BY session_id) as t2 on t2.session_id = t1.session_id;""".format(limit)
                # """
                # SELECT substr(bc.session_id,0,10) as id,
                #        count(command) as block_count ,
                #        min(CAST(delta_command_tdiff as FLOA))/1000 as min_conf_t, 
                #        max(CAST(delta_command_tdiff as FLOA))/1000 as max_conf_t, 
                #        avg(delta_command_tdiff)/1000 as avg_conf_t, 
                #        bcs1.prop_value as subtype
                # FROM block_command bc
                # LEFT JOIN block_conf_stats bcs1 on bcs1.prop_key = bc.block_hash 
                # WHERE command = 'ws_confirmation' 
                # GROUP BY bc.session_id, bcs1.prop_value
                # ORDER BY command_ts DESC
                # """ 



def select_block_command_all(session_id):
    return """SELECT substr(block_hash,0,32) as hash_part_1 ,substr(block_hash,32,33) as hash_part_2, delta_command AS 'from', delta_command_tdiff AS duration_in_ms, command AS till 
              FROM block_command 
              WHERE session_id LIKE '{}%' 
              ORDER BY block_hash, command_ts;""".format(session_id)

def select_block_command_outliner(session_id):
    return """SELECT substr(b1.block_hash,0,32) as hash_part_1 ,substr(b1.block_hash,32,33) as hash_part_2,
                     b1.subtype,
                     b1.delta_command AS 'from',
                     b1.delta_command_tdiff AS duration_in_ms, 
                     b1.command AS till , 
                     DATETIME(ROUND(b2.command_ts ), 'unixepoch') as published,
                     DATETIME(ROUND(b1.command_ts ), 'unixepoch') as confirmed
              FROM block_command b1
              LEFT JOIN block_command b2 on b2.block_hash = b1.block_hash and b2.command = 'publish'             
              WHERE b1.session_id LIKE '{}%' AND b1.command = 'ws_confirmation' 
              AND CAST(b1.delta_command_tdiff as FLOA) > 15000
              ORDER BY b1.delta_command_tdiff DESC;""".format(session_id)

def select_block_command_outliner_bysubtype(session_id, duration):
    return """SELECT 
              subtype, count(*), avg(delta_command_tdiff)/1000 as conf_avg_s, min(CAST(b1.delta_command_tdiff as FLOA))/1000 as conf_min_s, max(CAST(b1.delta_command_tdiff as FLOA))/1000 as conf_max_s
        FROM block_command b1        
        WHERE b1.session_id LIKE '{}%' AND b1.command = 'ws_confirmation' 
        AND CAST(b1.delta_command_tdiff as FLOA) > {}
        group BY subtype;""".format(session_id,duration)

def block_conf_account_stats_all(session_id):
    return """SELECT *
              FROM block_conf_account_stats 
              WHERE session_id LIKE '{}%' 
              ORDER BY tx_count DESC;""".format(session_id)


def select_min_max_conf_times(session_id):
        return  """SELECT max(delta_command_tdiff)/1000.000 as conf_max_s , min(delta_command_tdiff)/1000.000 as conf_min_s  
                   FROM block_command 
                   WHERE session_id LIKE '{}%' 
                   AND command = 'ws_confirmation'; 
                """.format(session_id)
    
def select_avg_conf_time(session_id):
        return  """SELECT avg(delta_command_tdiff)/1000.000 as conf_avg_s 
                   FROM block_command 
                   WHERE session_id LIKE '{}%' 
                   AND command = 'ws_confirmation'; 
                """.format(session_id)

def select_block_conf_stats(session_id):
    return """SELECT prop_key as command_key, prop_value as command_value
              FROM block_conf_stats 
              WHERE session_id LIKE '{}%'
              ORDER BY cast(prop_value as unsigned) DESC;
           """.format(session_id)

def print_rows(query, title=None):
    if title != "\r" : print("_" * 30)
    if title== None : title = query.replace("  ", "")
    print(title)
    if title != "\r" : print("-" * 30)
    print (pd.read_sql_query(query, conn))   
    print("-" * 30)

def main():
    global api

    parser = argparse.ArgumentParser(description="Echo your input")
    #default sourec seed : 0000000000000000000000000000000000000000000000000000000000000106 
    #default account at index 0 : nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm

    # Add a position-based command with its help message.
    parser.add_argument("--session_id", help="Optional. Show stats for a specific session by session_id")
    parser.add_argument("--show", help="dump table [1, 2, 3, 4]")
    parser.add_argument("--limit", help="Limit Stats Overview to last N sessions")
    parser.add_argument("--get_id", help="Default: true | Stats Overview includes session_id ")
    # Use the parser to parse the arguments.
    args = parser.parse_args()
    if args.session_id != None : args.session_id = args.session_id.replace("...","") 
    args.get_id = True if args.get_id == None or args.get_id == "true" else False
   
    

    if args.session_id == None and args.limit != None and args.show == None:
        q = select_conf_duration_stats(args.limit,args.get_id)
        print_rows(q, "Block confirmation Stats Overview")
        return
    
   
    
    if args.show == "1":
        q = select_block_command_all(args.session_id)
        print_rows(q, "Block commands for session {}".format(args.session_id))
        return
    
    if args.show == "2":
        q = block_conf_account_stats_all(args.session_id)
        print_rows(q, "Account Stats for session {}".format(args.session_id))
        return
    
    
    if args.show == "3":
        q1 = select_block_conf_stats(args.session_id)
        # q2 = select_min_max_conf_times(args.session_id)     
        # q3 = select_avg_conf_time(args.session_id)
        

        print_rows(q1, "Conf Stats for session '{}'".format(args.session_id))    
        # print_rows(q2, "Conf Times")
        # print_rows(q3, "\r")
        return
    
    
    if args.show == "4":
        print_rows("""select substr(block_hash,0,32) as hash_part_1 ,
                             substr(block_hash,32,33) as hash_part_2 ,
                             count(*) as commands 
                             from block_command where session_id LIKE '{}%' group by block_hash having count(*) <> 4 ;""".format(args.session_id), "Unconfirmed blocks for session {}".format(args.session_id)
                    )
        return
    

    if args.show == "5":
        q = select_block_command_outliner(args.session_id)
        q2 = select_block_command_outliner_bysubtype(args.session_id,15000)
        q3 = select_block_command_outliner_bysubtype(args.session_id,1)
        print_rows(q, "Block commands Outliners for session {}".format(args.session_id))
        print_rows(q2, "Outliners by subtype")
        print_rows(q3, "All confirmations by subtype")
        return
    
    if args.show=="6":
        q = select_conf_duration_stats_2(args.limit or 4)
        print_rows(q, "Block confirmation Stats Overview")
        return
    
    
if __name__ == '__main__':
    main()
