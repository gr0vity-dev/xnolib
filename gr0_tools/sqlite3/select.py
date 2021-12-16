
#sqlite3_select_tasks.py

import sqlite3
import argparse
import pandas as pd

db_filename = 'conf_duration.db'
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

def select_block_command_all(session_id):
    return """SELECT block_hash, delta_command AS 'from', delta_command_tdiff AS duration_in_ms, command AS till 
              FROM block_command 
              WHERE session_id = '{}' 
              ORDER BY block_hash, command_ts;""".format(session_id)

def block_conf_account_stats_all(session_id):
    return """SELECT *
              FROM block_conf_account_stats 
              WHERE session_id = '{}' 
              ORDER BY tx_count DESC;""".format(session_id)


def select_min_max_conf_times(session_id):
        return  """SELECT max(delta_command_tdiff)/1000.000 as conf_max_s , min(delta_command_tdiff)/1000.000 as conf_min_s  
                   FROM block_command 
                   WHERE session_id = '{}' 
                   AND command = 'ws_confirmation'; 
                """.format(session_id)
    
def select_avg_conf_time(session_id):
        return  """SELECT avg(delta_command_tdiff)/1000.000 as conf_avg_s 
                   FROM block_command 
                   WHERE session_id = '{}' 
                   AND command = 'ws_confirmation'; 
                """.format(session_id)

def select_block_conf_stats(session_id):
    return """SELECT * 
              FROM block_conf_stats 
              WHERE session_id = '{}'
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
    parser.add_argument("--session_id", help="64 char session_id")
    parser.add_argument("--show", help="dump table [1, 2, 3, 4]")
    # Use the parser to parse the arguments.
    args = parser.parse_args()
    print(args.session_id)   
    
    if args.show == "1":
        q_select_block_command_all = select_block_command_all(args.session_id)
        print_rows(q_select_block_command_all, "Block commands for session {}".format(args.session_id))
        return
    
    if args.show == "2":
        q_block_conf_account_stats_all = block_conf_account_stats_all(args.session_id)
        print_rows(q_block_conf_account_stats_all, "Account Stats for session {}".format(args.session_id))
        return
        
    
    
    if args.show == "3":
        q_select_block_conf_stats = select_block_conf_stats(args.session_id)
        q_select_min_max_conf_times = select_min_max_conf_times(args.session_id)     
        q_select_avg_conf_time = select_avg_conf_time(args.session_id)
        

        print_rows(q_select_block_conf_stats, "Conf Stats for session '{}'".format(args.session_id))    
        print_rows(q_select_min_max_conf_times, "Conf Times")
        print_rows(q_select_avg_conf_time, "\r")
    
    if args.show == "4":
        print_rows("select substr(block_hash,0,32) as hash_part_1 ,substr(block_hash,32,33) as hash_part_2 ,count(*) as commands from block_command where session_id = '{}' group by block_hash having count(*) < 3 ;".format(args.session_id),
                   "Unconfirmed blocks for session {}".format(args.session_id)
                    )
        return
    
if __name__ == '__main__':
    main()
