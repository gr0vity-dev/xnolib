from pynanocoin import *
from peercrawler import *

class msg_publish:
    def __init__(self, hdr, block):
        assert(isinstance(hdr, message_header))
        self.hdr = hdr
        self.block = block

    def serialise(self):
        data = self.hdr.serialise_header()
        data += self.block.serialise(True)
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

    peer = get_random_peer(betactx, lambda p: p.score >= 1000 and p.is_voting)
    peeraddr, peerport = str(peer.ip), peer.port
    print('Connecting to [%s]:%s' % (peeraddr, peerport))
    with get_connected_socket_endpoint(peeraddr, peerport) as s:
        node_handshake_id.perform_handshake_exchange(betactx, s)
        # header = message_header(betactx['net_id'], [18, 18, 18], message_type(message_type_enum.publish), 0)
        header = message_header(betactx['net_id'], [18, 18, 18], message_type(3), 0)
           
        json = {"action": "process", 
            "json_block": "true", 
            "subtype": "send", 
            "block": {  "type": "state", 
                        "account": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", 
                        "previous": "ADA4C6FFFFBA73B737263DCA39DACA82E75D3C3F779CB8343FA3CCEF57FE1CC6", 
                        "representative": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", 
                        "balance": "99999999999999999999999999999500", "link": "099A24851E26825DC1B7B1CFF7FB2EF33509429461E4DE5E21CAE15E1B409F89", 
                        "link_as_account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", 
                        "signature": "3C3A3DF324C894B4B824F9A04C938A05CE9662959A1F3FAA69D62176AE28DD85755B5E629D556B82B56D1E9B33A7F795175CA3780016256E407E1727387DCC0F", 
                        "work": "4fdbc9393b88677e"}}

        #modified parse_from_json to acocunt for new block structure
        block = block_state.parse_from_json(json["block"])      
        msg = msg_publish(header, block)

        #Added print for debug purpose 
        print(msg)   
        s.send(msg.serialise())

        #The received data is unrelated to the previous socket.send !?
        data = s.recv(1000)
        print(data)
        hex_resp = binascii.hexlify(data)
        print("\n === Read from socket === \n%s\n" % hex_resp)


if __name__ == '__main__':
    main()
