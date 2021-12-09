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
           
        json = {"subtype": "send", 
                "block": {  "type": "state", 
                        "account": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", 
                        "previous": "4ADC0C1D964AEA538B4AA267E0F3DA6C8FFF6AD0AB8458F912229659704F90EC", 
                        "representative": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", 
                        "balance": "99999999999999999999999999999600", 
                        "link": "9575F3517627D40FCE8F398C494088A8FDC27618BBA658741DE23D90A76FC30D", 
                        "link_as_account": "nano_37doyfaqebyn3z9aygeeb71ajc9xrbu3jgx8d3t3urjxk4mpzirf4t83xg5z", 
                        "signature": "914B84023941C94D213CB57460A4369689351D9FB747C0D6BC230870C9B05E084D3EA5C1C94B1C2AC05FFF21CBA74FB929056E6ADBB0494203EFB2DB5FA52404", 
                        "work": "ee561cc5885d9630"}}
        #modified parse_from_json to acocunt for new block structure
        block = block_send.parse_from_json(json)

        msg = msg_publish(header, block) 
        #Added print for debug purpose 
        print(msg)   
        s.send(msg.serialise())
        data = s.recv(5000)
        print(data)
        hex_resp = binascii.hexlify(data)
        print("\n === Read from socket === \n%s\n" % hex_resp)


if __name__ == '__main__':
    main()
