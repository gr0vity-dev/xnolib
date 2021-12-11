from pynanocoin import *
from peercrawler import *
from msg_handshake import node_handshake_id
from time import time


forks = [{"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "100", "link": "DF6B755456E58CF226233592C9F2CDD498C95B3E68AF173DDA8E70EB51CBE97D", "link_as_account": "nano_3qudgoc7fseeyam48feks9seuo6rs7fmwt7h4wyxo5mixfawqtdxuyt5744n", "signature": "B51419F6F42DC1D48D87A4CC51DA351D4A8755A9A193E0191FE381FD1B8AAEE7BA304E5C4BC77E6F53FAB912ECBA90C9C48275F1A91388A9DD00355C536D960F", "work": "5cbb50ade25f58aa"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "AC3CA33108727B36C905ABE3DCB86796DD85BB797701DCB4664AC076FED8E893", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "0", "link": "193B1FD9E38BE270DF9AA6BB6646BD48FF988A35E51550C81FB4419076A8FAE6", "link_as_account": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "signature": "E4A0B67B2794C018C3244F100498EB6ADDEB79894F80368883DFE6BDADCB44955734347310A52B9109823ADF8254492AD93689B6C31D289279AEFD360462B704", "work": "cc7302e24dfc0775"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "balance": "100", "link": "DF4CE3FDAAE38193BD863E99500791AF10A5E60F199C9691AEF1E9CC64314B11", "link_as_account": "nano_3qtewhytorw3kgyrehnsc15s5drinqm1y8ewktatxwhbsjk54krjjqhgh6a5", "signature": "BEE384839280FAC571883A0000B28977D7852FE42C1059680969960CD2F127BA2D73437507C9DEDE66BE4BE67483BB2075AD97E67688E7268DB6E4D9BF799D05", "work": "cb5586fb81a8952e"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "previous": "7432749F0326C25E7AAFDFA932E3FE02611E69B52DE6BD62EE11221F7B00FC95", "representative": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "balance": "0", "link": "50B56793417E326A8AFC0DDFF8CE6DA86C938E3B5413957B0C83661687D977AA", "link_as_account": "nano_1n7oeybn4zjkfc7hr5gzz598uc5ekg95po1mkoxis1u84t5xkxxckpzp1z7a", "signature": "DFFA610692747EB75E5E86030A00CF55F65DBB4DC33ADB3AC6782761517D9E06389475515A7F0E38C75B2732FF7AB78EE7E0508E820D762FC6BD5C4694923404", "work": "51a71610e3603196"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_1n7oeybn4zjkfc7hr5gzz598uc5ekg95po1mkoxis1u84t5xkxxckpzp1z7a", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_1n7oeybn4zjkfc7hr5gzz598uc5ekg95po1mkoxis1u84t5xkxxckpzp1z7a", "balance": "100", "link": "43BDC807BCBF164F5C9E510A52AC7AA515CB751450E5301AE4FE2B0626C1B0CB", "link_as_account": "nano_1ixxs15ushrpbxgbwnacccp9obaosftjan9781fgbzjd1rme5e8dfnbxhwb3", "signature": "E013EC5875E290178F16046C92D5ECF77FBCB4BACEC56CB0ED42FD0E07423D35C3AD47C9B05E9D1C397899AD3E028BE808215E5D4281987C53A7AA82A0B27608", "work": "44f8c610d4d9b07e"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "DF4CE3FDAAE38193BD863E99500791AF10A5E60F199C9691AEF1E9CC64314B11", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "100", "link": "DF6B755456E58CF226233592C9F2CDD498C95B3E68AF173DDA8E70EB51CBE97D", "link_as_account": "nano_3qudgoc7fseeyam48feks9seuo6rs7fmwt7h4wyxo5mixfawqtdxuyt5744n", "signature": "CDDBBF5E9399315F8782108015E7F37B5884335E2B425B027134B7A2EE70F26114D4DF29E99796E36939820FC0DA1DD07B5B1F9A4FBDC3CAF553CF61A288360C", "work": "0fb68280fd610de8"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "E93CBD2EF987D1B9B112AB70CB6CA552C5C9DA1645FBF55F44A9A7EF329CF5F4", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "0", "link": "193B1FD9E38BE270DF9AA6BB6646BD48FF988A35E51550C81FB4419076A8FAE6", "link_as_account": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "signature": "CF557EF351B304C1A422FBFB25052FB95BC4255A406673B725672E2A7B8418F8DD08759DBDCF6B16283B45A0F61C471AFD6E33AFBEC0006AF73AAC3F9DBAB100", "work": "37bbfefaba8fa4c7"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "previous": "43BDC807BCBF164F5C9E510A52AC7AA515CB751450E5301AE4FE2B0626C1B0CB", "representative": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "balance": "100", "link": "0564B96DF33D3BAFA2D37C16217CAF414103320AD8BF54664482657A2E136783", "link_as_account": "nano_13d6q7pz8hbuoyjf8z1p67ycyic31es1op7zcjm6b1m7haq38sw5nsmdrc81", "signature": "19579F728C530DFD5A13F3CB0A65B295403F21B42332D3C07709E939EAF9DB7434CBD1551E37AB75BEAA0FCE8FA5C1CA803228D43AD91FCB044830B2012FFF01", "work": "88d4ca122536d926"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "previous": "321F010C2F176038E1FA424C3EB619F66629770119B492F4EBBF3FEA137286EB", "representative": "nano_18bu5zey94z4g5hsoboues5dtk9zm475dsaoc563zf43k3ucjyq8iox3xxkt", "balance": "0", "link": "565C3BB490C8D55C9867CC009F1E6AE1DA573A8837700B2A58FD5F3F9A14642C", "link_as_account": "nano_1okw9gtb3k8odke8hm11mwh8orgtcwxaifui3eo7jzcz9yf3as3efpp1867f", "signature": "96D4021D0F27A45D732AF48C231292410EB6BAD8023CEF7E46BBD26AF805C31B5F79AC3C9481ED0CADA1BD4BC61B5B7599D25D3287D91E63AC0F1BD38542EB0B", "work": "cccf0de5a76188a5"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_1okw9gtb3k8odke8hm11mwh8orgtcwxaifui3eo7jzcz9yf3as3efpp1867f", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_1okw9gtb3k8odke8hm11mwh8orgtcwxaifui3eo7jzcz9yf3as3efpp1867f", "balance": "100", "link": "01C93CF950BEC7D3D48758A4F307B1D39E758AC65E22458CFD4BA597AAD6204D", "link_as_account": "nano_11gb9mwo3hp9thcagp76ye5u5nwygp7eeqj4ap8htkx7kyofea4f1scz9i65", "signature": "34EC48645CF6AFDCA41D3C7376C8FEB87A8F891F9D0DB0C0799D310D24D7A1C5F18A6FFC52D5B8E604E550448E1F7165F8D67216E9A3711BDE530BA854ACDC0A", "work": "946785be6c3a8aa1"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "0564B96DF33D3BAFA2D37C16217CAF414103320AD8BF54664482657A2E136783", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "100", "link": "DF6B755456E58CF226233592C9F2CDD498C95B3E68AF173DDA8E70EB51CBE97D", "link_as_account": "nano_3qudgoc7fseeyam48feks9seuo6rs7fmwt7h4wyxo5mixfawqtdxuyt5744n", "signature": "C69902CD5185B0560B8EBF5C181923AF4F45D2C0B113577D45F5B889EA3ACD7CFD5E403450DC66E5B626A7BC2B174890A102D820EA33BFD1BAA3E341770A270F", "work": "ddd69cab2a830e74"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "1C4602963AD113F74DF781BDD27A5D93480974F24542E92580B03374505F59C6", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "0", "link": "91DCE980D86EB7FA9DFF167CF39CFB52E5A7E70450CDF9DD96F0F527045FDB87", "link_as_account": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "signature": "D2ECE0C959AD963A9883C8220E594D733801CA1856E6C3F16BFBAAE2796C04191C857E585273DA7F51C19DC7F4C449F0D06D6F60233A642D9715026938F1350A", "work": "738588ada31c6145"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "balance": "100", "link": "3D866BD5040338BA2C5EC29A8911A8B45AC51F0C665992BB452F30B3883E54B5", "link_as_account": "nano_1he8fhcia1srqap7xintj6atjf4trnhirskskcxncdsipg65wo7o6ircynsy", "signature": "46EA7C25EEFC05FE04629CC131090F139B6EA56315DF24BC97E13625C7DC404FF7A9243C7D6A8338F40ED6483061C54B15BD338F1B6CF77C5581E9E3CCEF770F", "work": "ca55a288479c54b3"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "previous": "0B3737ED5F44CDC2165072906E6A21BD00963862DDF56B6BFF0826F50B1E5F03", "representative": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "balance": "0", "link": "59BDD34386D408781A8E1DB9F0D2FF7A3DBFD7C67B8DEE53707BCCA03786AECB", "link_as_account": "nano_1pfxtf3rfo1ah1faw9fsy5bhyyjxqzdweywfxsbq1yyen1urfdpdx4ctddik", "signature": "80178905855F2880EA77F2E37B2FDCF198F6F2991D99621C36C19CDB5B223BACCBE7011C25A370E26E03D1A3AA737706BF732DB41F9384404AF2112A11224409", "work": "dfab711666b84a43"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_1pfxtf3rfo1ah1faw9fsy5bhyyjxqzdweywfxsbq1yyen1urfdpdx4ctddik", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_1pfxtf3rfo1ah1faw9fsy5bhyyjxqzdweywfxsbq1yyen1urfdpdx4ctddik", "balance": "100", "link": "6B65B33DAA2769704B7DCA916761CBCBBE056C4B39293D79071AEABC26BE4B02", "link_as_account": "nano_1tu7peytnbubg37quknjexiwqkxy1op6pgbb9owig8qcqimdwkr4wruchr6z", "signature": "893687A6F40908FFAA23C2FF4B212650E9D13C94CBF1A49DF51507B2CDA2B485935D3180B9F3F0D844F9DF17260DB23D2193A21C4C803F39F625A41AB0172804", "work": "522a54223e924bd4"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "3D866BD5040338BA2C5EC29A8911A8B45AC51F0C665992BB452F30B3883E54B5", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "100", "link": "DF6B755456E58CF226233592C9F2CDD498C95B3E68AF173DDA8E70EB51CBE97D", "link_as_account": "nano_3qudgoc7fseeyam48feks9seuo6rs7fmwt7h4wyxo5mixfawqtdxuyt5744n", "signature": "9F2FFA9E8D722FD69FF5A7FFE141942942BA11421FDA2A8C2CC55DF850059B111C219C12BA6566AB4B931CECC70677039464F50EE168DF4A6021A21D6478040F", "work": "8099c111c2f2c2a8"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "previous": "CDEB79070D07B3B88203F920238EB98EE550F609EFF8C8B3EB9418FF401B8E4C", "representative": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "balance": "0", "link": "91DCE980D86EB7FA9DFF167CF39CFB52E5A7E70450CDF9DD96F0F527045FDB87", "link_as_account": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "signature": "1BAADFF5FE45A04E6F32FB09177F75D65B6828244E77BE431E751D26BE4260CA587BE33B4327C9824AA4B778F3AA8B0273D4DA6756E8824F35E281D13706AE00", "work": "f180b51de17e2920"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "previous": "6B65B33DAA2769704B7DCA916761CBCBBE056C4B39293D79071AEABC26BE4B02", "representative": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "balance": "100", "link": "2F2E43FD66C29127A580547F89A82BA9D50D29F65FB3635A6DF5EF6D92474DF3", "link_as_account": "nano_1dsgahypfinj6ykr1o5zj8n4qcgo3nnzeqxmeff8uxhhfpb6gmhm5zzyhhrf", "signature": "BD60B431B0F4FF2741A2E9EF3C0CC109461A9DA2A4F385D9AD84954C58EC26A5C92266106A3C616AFEBB16491DD23EB6F488EEB48DED11D2754A1CD4A07B1002", "work": "afae389809fb3535"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "previous": "81B8730AF3069C9E8132B0F966DF9C5D9F2DCA8FF1633D5CE97C8393663B8FC7", "representative": "nano_36gwx81fiuoqzcgzy7mwygghpnq7nzmian8fz9gsfw9o6w47zpw9ut5hfuhw", "balance": "0", "link": "9598E2CC5FC22EED025B7FCF1A36BCCE7B3F06A22044693C6EC945E4BBEA5DCB", "link_as_account": "nano_37erwd87zijgxn37pzyh5audsmmu9w5c6a46f6y8xkc7wkxynqgdhieatyx6", "signature": "C89F44A80D0B05592CDEB3F837E1DAA330E7A87AF30F56D58D94E6C0548CDC492681FDF7A75B483BD83B4C32A9F1DF5F2B166E74AD3F4A711DE3FCCF22EE9F0F", "work": "fd33e73293d966c7"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_37erwd87zijgxn37pzyh5audsmmu9w5c6a46f6y8xkc7wkxynqgdhieatyx6", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_37erwd87zijgxn37pzyh5audsmmu9w5c6a46f6y8xkc7wkxynqgdhieatyx6", "balance": "100", "link": "E9F895EFE9C01FFC8BC769B0BD275A213124E882F861B31FE7B73925733EFEBE", "link_as_account": "nano_3thrkqqymi1zzk7wgtfiqnmonabj6mna7y53pehyhfss6osmxzoyafuizz8f", "signature": "9DE099CC6E6DA00751395AADF3537EC3F4C9DDAFA7580CC305E7839C22F1008505795B576F1B6A87914C25298C2DAC3C80D1193B0ADB3C0BB24DF7ABE7E2A601", "work": "4d7f62ef38809032"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "100", "link": "FF71CEE99EE2CF02A7CFC248C0FF7BAFCB86F5ADD86FA5F8A1FA86073886625E", "link_as_account": "nano_3zujsunsxrph1cmwzikar5zqqdydiuttup5hnqwc5yn81wwaerkygqh9ih13", "signature": "47C3F3F8583CBCBD974CA92CD9CF6C1DCE89A1141B061C5CCAF3BCC75326B65A9DD21AF4B86BE319FB7F376806316D83E3288297A361552BFB34292EA7C81100", "work": "0142e2ffafc9c1f8"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "91AF54D9BD50B08DD17AB17233C32C6B0B7C4EF7091AFA2303E169615FED25C5", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "0", "link": "A6030342D424053F5E187864BA0C5E8D93F6422D90089431604C5826F84E6938", "link_as_account": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "signature": "EDD41468880873D89C4A3A08A2D2DF6CAEAFC1CDAC3CB92403F77C55713FBEF26F20BE007E14518201696C540D5C24D5B9A0E5B4B3BA61D0EE06C05CAA979F0A", "work": "44d8e0ddd0dc69af"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "balance": "100", "link": "7C79DD0279915AE67E230DE5EE6E9038C820CEB2DC9DB29D4F931A270D11BFC7", "link_as_account": "nano_1z5sun39m6ctwsz485h7xsqb1g8a659d7q6xpcgnz6rt6w8j5hy9kg3r93tg", "signature": "2A249CBB94E8DBCA3D690718541E9CFD3403C9FA5611A2D4AFCB188DF9E6B536059A86A632235CCC54B604F3CB855B35BEBA901CE14C0D8A1EC587899FDB2D07", "work": "07a4388a952769db"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "previous": "DA0EC0326221428CB0FDC4E60FC88C126965293F522F3B17B1D92E6BC6CBB960", "representative": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "balance": "0", "link": "AF4E622156452F8454CC54D9408102AFAA36DBAD8107C6858749A59A98BFF315", "link_as_account": "nano_3dtgeaioejbhijcero8sa41i7dxc8uftu1a9rt4rgkf7mcedzwrouku6jhu6", "signature": "DF294FAAFFF9E239D660E246E9975695F83B234FED8FA9E97A2EDA35201D173EBE7BB5DC20E13CD87DF0D5E7B4F7D6D50CB0E1F3B60D91CE9F8AC89CF155AB03", "work": "29116982e886022a"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3dtgeaioejbhijcero8sa41i7dxc8uftu1a9rt4rgkf7mcedzwrouku6jhu6", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_3dtgeaioejbhijcero8sa41i7dxc8uftu1a9rt4rgkf7mcedzwrouku6jhu6", "balance": "100", "link": "9A520CB85835D72C342A7BB02893D3872F02E74209638B1E3301498E54D5C1A0", "link_as_account": "nano_38kk3kw7ifgq7it4nyxi74bx93sh1dmn64d5jeh581cbjscfdif1cgm4zxma", "signature": "B831BE65D2B47C2CF593E23C15CD53B84493A02083F4DACF5BE18F3DB4ECA8FEF174D59A057A212E014FC97321316204AC36B226DF7880B4E5F6426249DCEB09", "work": "4431fe6d65b6bdb2"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "7C79DD0279915AE67E230DE5EE6E9038C820CEB2DC9DB29D4F931A270D11BFC7", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "100", "link": "FF71CEE99EE2CF02A7CFC248C0FF7BAFCB86F5ADD86FA5F8A1FA86073886625E", "link_as_account": "nano_3zujsunsxrph1cmwzikar5zqqdydiuttup5hnqwc5yn81wwaerkygqh9ih13", "signature": "D29247C83A43B1DE25DCA18D43634250D15C88F77633CA0569685140DBBE037C0E02AA54FEF6A56D113060DEBB574461D9DD0559747F91C78A337D7164EE2504", "work": "1eee2e4f03ee0be3"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "B4A4CC3A981D2BBBCC39BA1CE201C5D910D4BE29DEC70F3DAAD50342F1342B3B", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "0", "link": "A6030342D424053F5E187864BA0C5E8D93F6422D90089431604C5826F84E6938", "link_as_account": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "signature": "F696AE2D03FD46A4D22A5A5F7CABA8F03B3AA078B340171A10A8ABABA983F5A090F74DD6CF070C43BCDF3054E8FE72D961FC33BF67F2AB7E927F31FCD381C509", "work": "4508c8f9ab0eb512"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "previous": "9A520CB85835D72C342A7BB02893D3872F02E74209638B1E3301498E54D5C1A0", "representative": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "balance": "100", "link": "1978C137DDC109374024678DA89A2426788663F05F42E5FFA2E0CAE1219A5F75", "link_as_account": "nano_18drr6uxuiab8x14aswfo4f4abmrisjz1qt4wqzt7r8cw6isnquoafbi7ef6", "signature": "BC1728E5B7B6EEC81F55D3679348D9AE6E879BFFE4140B0AE05F73160B0AE4EA7E49832F4E5C2021B2C12D36CEEDE50AC210E7D61BE036C26B0DEB4433869706", "work": "a314513d00933490"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "previous": "CE1DB938A3EFC3D0E02F1A084C89F5960C280C45628C82791D14BB81AAD7F048", "representative": "nano_3bi51f3fab179xh3iy56qa87x5emys34u61akirp1m4r6uw6wtbr18wmhdki", "balance": "0", "link": "6F16B216EDCE0656C67B716774A98D446D54A72C30217858052AB63DB8AEB03C", "link_as_account": "nano_1urppadgumi8cu59pwd9gknrtj5fckmkre33h3e1ccop9pwcxe3ws31e9d16", "signature": "931842219E2A732C9D64684D4FF0197E5BD59B1C65CD098FE6AA061C9645A5E972C892BEE126E8932A0277009EE71AF62EC1828E1FFFDDF07D890F074F576C0D", "work": "405b649ceedff12b"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_1urppadgumi8cu59pwd9gknrtj5fckmkre33h3e1ccop9pwcxe3ws31e9d16", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_1urppadgumi8cu59pwd9gknrtj5fckmkre33h3e1ccop9pwcxe3ws31e9d16", "balance": "100", "link": "ECF32B95B5DD2B9F494304D27EA94F7EBEB7F75572069C986BB286198237FAB5", "link_as_account": "nano_3u9m7gcudqbdmx6n838khtnnyzoypzuocwi8mke8qen85835hyoozpueaczb", "signature": "3277054227B49312419E288F15761A5EDBBC3BC1BF1DC06D49D8A783751505E1379FB67490754945ADD3C20F8D2F0EE16C32E47175E97FDD35230659DA4CED07", "work": "643c959a4ff45450"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "1978C137DDC109374024678DA89A2426788663F05F42E5FFA2E0CAE1219A5F75", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "100", "link": "FF71CEE99EE2CF02A7CFC248C0FF7BAFCB86F5ADD86FA5F8A1FA86073886625E", "link_as_account": "nano_3zujsunsxrph1cmwzikar5zqqdydiuttup5hnqwc5yn81wwaerkygqh9ih13", "signature": "D96F06E2CE04E1054E2E3D9C615FFCF5DC3D2AE748508F1225A293E714BBC8617CC00849B720904F45918745AFF0F973170EC3F5D74DD6BC368D49735B8C7400", "work": "ce9cd10f880980f4"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "5919FECBF59DE4D2244583D22D07E732FF3E0A84A36A523FED696BDD28099A8B", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "0", "link": "8B62E4626A87949E3846E407995F65BEC2EC5DC00C6013E38DA51E999571A647", "link_as_account": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "signature": "FCBE3161D7DD8A79DEB264BE79973446E7A9215349A7F7D5876620FE900A3AEAA38827B9EE9384E0C3DEED2B6C88A763E934E9CF2784969E71D3B0F5058A5906", "work": "ce8440c4d7ad76f6"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "balance": "100", "link": "D1CA4AC6B3156346B22D9D16E4CE957D282C3B35D9FC4769259014C916F97F36", "link_as_account": "nano_3ngcbd5d87d5ats4u9apwm9bczba7ixmdphwaxnkd61ns6dhkzspxskurni1", "signature": "2924EB4A15BBD51E34A175C144FF9247C64F41CF185B89A353260AC99FDDA6256B903A9EA6C4C8E4CCA0BA337224C5C1D76AAC61CC19CADE268DA47D25B2DB00", "work": "aff09e6dd3e1265c"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "previous": "CE6D083EF4A1C0250C3E6A3A8DAB657E660243D97AE848413CA75BF32703FFD9", "representative": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "balance": "0", "link": "AFD0D041D51FCFCDFFDADEB80C50D77AFA8C56956E528B239C62F79CD10D90DA", "link_as_account": "nano_3dyit31xc9yhsqzxoqor3jafgyqtjjdbcukkjejsrrqqmmaiu68tujgrt87z", "signature": "B4A88C3C9FEC2F74E685F5924973DB835F7FBCC9F9A5EA8F6CC0BA370EB9536F6A2F65EF242CA98E589E6025E406094AFC3B849627CAC4B5DA3FB807CDB93300", "work": "345d7a63a79d6139"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3dyit31xc9yhsqzxoqor3jafgyqtjjdbcukkjejsrrqqmmaiu68tujgrt87z", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_3dyit31xc9yhsqzxoqor3jafgyqtjjdbcukkjejsrrqqmmaiu68tujgrt87z", "balance": "100", "link": "3ACF5C8559D0446C546CF5C194B747E6C939F0863B7890FCF334E4B868209473", "link_as_account": "nano_1gphdk4omn46fjc8sxg3kkunhspb99raegurk5yh8f96q3n4375myy1yhkak", "signature": "4832211B202DD767AD2C0CDC1C44101BE5122D40A4F63FACD380123FF3A86F1FE81DBBA0EDCE11957ED9B89A01A887898E43982D5A8C4201F00FF96411A04B0F", "work": "afdf47d677777121"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "D1CA4AC6B3156346B22D9D16E4CE957D282C3B35D9FC4769259014C916F97F36", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "100", "link": "FF71CEE99EE2CF02A7CFC248C0FF7BAFCB86F5ADD86FA5F8A1FA86073886625E", "link_as_account": "nano_3zujsunsxrph1cmwzikar5zqqdydiuttup5hnqwc5yn81wwaerkygqh9ih13", "signature": "171ABD81D7D9BC6AB0AFA5B4769DD54DB0AF4EF917080DB4D4E190E83393BCC5F6248BB069F7399DB9BCECCDA8E4A43D7A5F0E86A8D34586D98227FD1FD7A80F", "work": "9d88c0878f91933b"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "previous": "670F175BBBD59D1F24CE681E2E9EAF1559B89D14EA7D192CFE6C207F4C2B19D2", "representative": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "balance": "0", "link": "8B62E4626A87949E3846E407995F65BEC2EC5DC00C6013E38DA51E999571A647", "link_as_account": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "signature": "C7731A399661A45B07D2DD64082C77BEF7C0A31AD74924C75A64D2FA2A6CE792313F54D6F859E33B79292E7AE2BB680DF57C1BC6312231ED9B806CD14FFB320A", "work": "95e9dfd96ed45703"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "previous": "3ACF5C8559D0446C546CF5C194B747E6C939F0863B7890FCF334E4B868209473", "representative": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "balance": "100", "link": "CC4CBCFC0A59D8A9CE49EB84E9DA8292FED0F0E268420DB9B9B580163A40E292", "link_as_account": "nano_3m4eqmy1npgro996mtw6x9fa76qyt5rg6t443pwumfe14rx63rnks5wwm7bu", "signature": "1344008583B1EA94FBF3F15E41F68373DF3EABE257EB9677C4D0699AD633DDB7575BA12A5951D10DA72F615FBC17B17BA23461DBC076DF359CBB6B7DBAC4D106", "work": "9e0607b5f15905aa"}},  
 {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "previous": "71B8F708E5EDBC1B905927E931689814384BCAB5646EFA99FE2890A9CAB46A73", "representative": "nano_34u4wjj8o3wnmrw6fs19m7hpdhp4xjgw15514hjrubaym8cq5bk94tgrwked", "balance": "0", "link": "DF9063D802E1538741CB875B6D0EF0EC24B35EECC2475D4556DCAFC8BE3D6F8F", "link_as_account": "nano_3qwiehe17rcmix1wq3tufn9h3u36pfhgsik9do4ofq7hs4z5tuwho8eafohg", "signature": "9B3B2E0AE252EDFB9FBC5856D6FF77890132C6E8E55ABFF6E4858411F475AB383E7D148D8D4F6C65A15B2E7829DB50C7283FC4E18F906EDF81C67E7CAB177406", "work": "fe717d3eda3fcfce"}},  
 {"action": "process", "json_block": "true", "subtype": "open", "block": {"type": "state", "account": "nano_3qwiehe17rcmix1wq3tufn9h3u36pfhgsik9do4ofq7hs4z5tuwho8eafohg", "previous": "0000000000000000000000000000000000000000000000000000000000000000", "representative": "nano_3qwiehe17rcmix1wq3tufn9h3u36pfhgsik9do4ofq7hs4z5tuwho8eafohg", "balance": "100", "link": "12F3C60AD1F53820B8E750E262FB6F5F3F89DA8151C0DE10207FFD435501ECF2", "link_as_account": "nano_16qmrr7f5xbr64wggn94edxpyqszj9fa4ng1ura41zzxafci5u9k794jw5rh", "signature": "08BA458B2F7FD7AAD9B9DDDCBDEB7AF868DA01D7EF46A3FF9867ADE8452F31C3228D96EA222EF1B652CED2AD1247878089468820E43FAE2254166C1BF0658F0B", "work": "74a13a331f6df8ba"}} ]

fork_head_A = {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", "previous": "BD042192FC01D9E796F8E5EC2BD1A5DB0A2ADFAA3654FA55C4E53A74F4162E41", "representative": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", "balance": "99999999999999999999999999999300", "link": "099A24851E26825DC1B7B1CFF7FB2EF33509429461E4DE5E21CAE15E1B409F89", "link_as_account": "nano_14et6k4jwbn4dq1uheghyzxkxwso373barh6ush45kq3drfn39wb4hw417ur", "signature": "C71E038283100FC7045252E81A7446C9EA5CF328EB57F4188D7C25DE8918073F915531EB11FF729185CE825D656958A2B69A6729B4C92C6944C0AAFC2EDF220B", "work": "65a9742f31faa27e"}}
fork_head_B = {"action": "process", "json_block": "true", "subtype": "send", "block": {"type": "state", "account": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", "previous": "BD042192FC01D9E796F8E5EC2BD1A5DB0A2ADFAA3654FA55C4E53A74F4162E41", "representative": "nano_3u8xzqmu6ymxrozhoerop685kaayxbjayd7p9udneodofixksiu9xx7rhycm", "balance": "99999999999999999999999999999300", "link": "C8CBAAA5DB5BEAFC25A38241B4AC2A4EF975F21903017B6009E895A9166BDBDC", "link_as_account": "nano_3k8dockxppzczikt91k3pkp4nmqsgqs3k1r3hfi1mt6oo6d8qpywuocazoea", "signature": "3F9401A2A0B51750F9EC3C2E78B650F2A1212FAA8499C28F79834D37E8BA8575A629FBB7DFF4DE87F618BB7BC9FB930FE3C823EF6B373039F33930B44C52BA09", "work": "a83d4c70c846bb37"}}


def handshake_peer(ip,port,ctx, retry = 3):
    try:
        socket = get_connected_socket_endpoint(ip, port)
        node_handshake_id.perform_handshake_exchange(ctx, socket)
        print('peer added [%s]:%s' % (ip, port))        
        return socket
    except:        
        retry = retry -1
        print("error on handshake_peer: retry_count {}".format(retry))
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
    ctx = betactx
    voting_peers = get_voting_peers(ctx)
    sockets = []

    #Handshake with all voting peers
    for peer in voting_peers :
        s = handshake_peer(str(peer.ip), peer.port, ctx)
        if s is not None :
            sockets.append(s)


    #debug
    for socket in sockets :
        print(socket)   

    msgtype = message_type_enum.publish
    hdr = message_header(network_id(66), [18, 18, 18], message_type(msgtype), 0)
    hdr.set_block_type(block_type_enum.state)

    # for json in forks :
    #     s = random.choice(sockets)        
    #     blk = block_state.parse_from_json(json["block"])
    #     assert(isinstance(blk, block_state))           
        
    #     msg = msg_publish(hdr, blk)
    #     print(msg)
    #     s.send(msg.serialise())
    
   

    s1 = sockets[0]
    s2 = sockets[1]

    # node_handshake_id.perform_handshake_exchange(ctx, s1)
    # node_handshake_id.perform_handshake_exchange(ctx, s2)
    blk1 = block_state.parse_from_json(fork_head_A["block"])
    blk2 = block_state.parse_from_json(fork_head_B["block"])   
    msg1 = msg_publish(hdr, blk1)
    msg2 = msg_publish(hdr, blk2)
       
    print("sending")
    s.send(msg1.serialise())
    print("sent1")
    s.send(msg2.serialise())
    print("sent2")


    # for peer in peers :
    #     print('peer [%s]:%s' % (str(peer.ip), peer.port))
    # return
       
   
    # with get_connected_socket_endpoint(peeraddr, peerport) as s:
    #     node_handshake_id.perform_handshake_exchange(ctx, s)
    #     blk = block_state.parse_from_json(json["block"])
    #     # blk = read_json_block_from_stdin()
    #     # only state blocks for now
    #     assert(isinstance(blk, block_state))
    #     msgtype = message_type_enum.publish
    #     hdr = message_header(network_id(66), [18, 18, 18], message_type(msgtype), 0)
    #     hdr.set_block_type(block_type_enum.state)
    #     msg = msg_publish(hdr, blk)
    #     print(msg)
    #     s.send(msg.serialise())


if __name__ == '__main__':
    main()
