from pynanocoin import *
from peercrawler import *
from msg_handshake import node_handshake_id

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
    ctx = betactx
    
    peer = get_random_peer(ctx, lambda p: p.score >= 1000 and p.is_voting)
    peeraddr, peerport = str(peer.ip), peer.port

    # print('Ignoring [%s]:%s' % (peeraddr, peerport))
    # peeraddr, peerport = str("::ffff:65.108.10.185"), 54000
    

    json = {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", "previous": "93FE9847E8C4A6D7F9FD4BF6D1F68AE9B3E2C13D4EE0E27E49694486BAB5E853", "representative": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", "balance": "99999999999999999999999999999400", "link": "C8CBAAA5DB5BEAFC25A38241B4AC2A4EF975F21903017B6009E895A9166BDBDC", "link_as_account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "signature": "56E1F6ED0445C81EC5725949EA878CE9B4E192E8D42143C3E11A68058D0EBBC113A3BF405748648EDA2A0263DFE19AD1851C14F1DFC9CF522B5AB1547E945F02", "work": "d0f511f2db9c8ad6"}}


    print('Connecting to [%s]:%s' % (peeraddr, peerport))
    # with get_connected_socket_endpoint(peeraddr, peerport) as s:
    #     node_handshake_id.perform_handshake_exchange(betactx, s)
    #     # header = message_header(betactx['net_id'], [18, 18, 18], message_type(message_type_enum.publish), 0)
    #     header = message_header(betactx['net_id'], [18, 18, 18], message_type(3), 0x0600)
           
       

    #     #modified parse_from_json to acocunt for new block structure
    #     block = block_state.parse_from_json(json["block"])      
    #     msg = msg_publish(header, block)

    #     #Added print for debug purpose 
    #     print(msg)   
    #     s.send(msg.serialise())

    #     #The received data is unrelated to the previous socket.send !?
    #     data = s.recv(1000)
    #     print(data)
    #     hex_resp = binascii.hexlify(data)
    #     print("\n === Read from socket === \n%s\n" % hex_resp)

    with get_connected_socket_endpoint(peeraddr, peerport) as s:
        node_handshake_id.perform_handshake_exchange(ctx, s)
        blk = block_state.parse_from_json(json["block"])
        # blk = read_json_block_from_stdin()
        # only state blocks for now
        assert(isinstance(blk, block_state))
        msgtype = message_type_enum.publish
        hdr = message_header(network_id(66), [18, 18, 18], message_type(msgtype), 0)
        hdr.set_block_type(block_type_enum.state)
        msg = msg_publish(hdr, blk)
        print(msg)
        s.send(msg.serialise())


if __name__ == '__main__':
    main()
