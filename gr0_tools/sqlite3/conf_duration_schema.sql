
create table block_command (
    session_id          CHAR(64),
    block_hash          CHAR(64),
    subtype             CHAR(8),
    command_ts          DATETIME DEFAULT((julianday('now') - 2440587.5)*86400.0),
    command             CHAR(32),
    delta_command_tdiff INTEGER,
    delta_command       CHAR(32),
    PRIMARY KEY(session_id,block_hash,command,delta_command)
);

CREATE INDEX idx_block_command_session_id
ON block_command (session_id);
CREATE INDEX idx_block_command_block_hash
ON block_command (block_hash);
CREATE INDEX idx_block_command_command
ON block_command (command);


create table block_conf_stats (
    session_id      CHAR(64),
    prop_key        CHAR(32),
    prop_value      CHAR(32),
    PRIMARY KEY(session_id,prop_key)
);
CREATE INDEX idx_block_conf_stats_session_id
ON block_conf_stats (session_id);

-- create table block_conf_tx (
--     session_id      CHAR(64),
--     block_hash      CHAR(64),
--     account         CHAR(65),
--     seed            CHAR(64),
--     seed_index      CHAR(64),
--     block_subtype   CHAR(12),    
--     bucket          INTEGER,
--     PRIMARY KEY(block_hash)
-- );
-- CREATE INDEX idx_block_conf_tx_session_id
-- ON block_conf_tx (session_id);


create table block_conf_account_stats (
    session_id      CHAR(64),    
    account         CHAR(65), 
    bucket_last_tx  INTEGER,
    tx_count        INTEGER,
    PRIMARY KEY(session_id,account)
);
CREATE INDEX idx_block_conf_account_stats_session_id
ON block_conf_account_stats (session_id);

