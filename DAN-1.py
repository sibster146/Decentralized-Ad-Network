import hashlib
import numpy as np
import struct

class AdProvider:
    def __init__(self, pltfm, offset, ad):
        self.pltfm = pltfm
        self.users = []
        self.ad = ad

        domain = np.arange(1,30)

        def ad_algorithm(input):
            bid = -5*abs(input-offset)+20
            return bid

        # creating domain and range
        table = {}
        self.encr_table = {}
        for i in domain:
            table[i] = ad_algorithm(i)
            #creating the encryption table
            self.encr_table[hashlib.md5(i).hexdigest()] = hashlib.md5(ad_algorithm(i)).hexdigest()

        # creating decrypting table for platform
        self.decr_table = dict(zip(list(self.encr_table.values()),list(table.values())))

        # sending decrypting table and ad to platform
        pltfm.receive_ad_decr_table(self,self.decr_table, ad)

    def receive_user(self,user):
        # sending encrypting table to a user
        self.users.append(user)
        user.recieve_encr_table_key(self,self.encr_table)

class User:
    def __init__(self,pltfm):
        self.pltfm = pltfm
        self.ad_prov_encr_table = {}
        self.all_pltfms = []
        self.score = []

        #user registers with platform
        pltfm.register_user(self)

    def recieve_encr_table_key(self, ad_prov, encr_table):
        self.ad_prov_encr_table[ad_prov] = encr_table

    def get_bids(self, input):
        bids = {}
        for ad_prov, table in self.ad_prov_encr_table.items():
            encr_input = hashlib.md5(struct.pack('<i',input))
            bids[ad_prov] = table[encr_input.hexdigest()]

        self.pltfm.receive_bids(bids, self)

        for p in self.all_pltfms:
            p.receive_bids(bids,self)

    def recieve_all_platforms(self,pltfm):
        self.all_pltfms.append(pltfm)

    def receive_winning_ad(self,ad):
        if len(self.score) == 0:
            self.score.append(ad)
            if len(self.all_pltfms) == 0:
                print(f"WINNING AD: {ad}")
                #self.score.clear()
        elif ad not in self.score:
            print("AD ISSUE!!!")
            #self.score.clear()
        else:
            self.score.append(ad)
            if len(self.all_pltfms)+1 == len(self.score):
                print(f"WINNING AD: {ad}")
                #self.score.clear()

class Platform:
    def __init__(self, root):
        self.ad_prov_decr_table = {}
        self.ad_prov_ads = {}
        self.users = []
        self.ad_provs = []
        self.all_pltfms = []

        #add extra nodes to the network
        if not root:
            return
        self.ad_prov_decr_table = root.ad_prov_decr_table.copy()
        self.ad_prov_ads = root.ad_prov_ads.copy()
        self.users = root.users.copy()
        self.ad_provs = root.ad_provs.copy()
        self.all_pltfms = root.all_pltfms.copy()
        self.root = root
        self.all_pltfms.append(root)

        for p in self.all_pltfms:
            if p!=self:
                p.all_pltfms.append(self)
        for user in self.users:
            user.all_pltfms.append(self)

    def register_user(self,user):
        self.users.append(user)

        #send user to all ad provs
        for ad_prov in self.ad_provs:
            ad_prov.receive_user(user)

        #send user to all platforms
        # and send user all platforms
        for p in self.all_pltfms:
            p.users.append(user)
            user.recieve_all_platforms(p)

    def receive_ad_decr_table(self,ad_prov, decr_table,ad):
        self.ad_prov_decr_table[ad_prov] = decr_table
        self.ad_prov_ads[ad_prov] = ad
        self.ad_provs.append(ad_prov)

        #sending all users to ad prov
        for user in self.users:
            ad_prov.receive_user(user)

    def receive_bids(self,bids, user):
        max_bid = float("inf")*-1
        winner = None
        for ad_prov,encr_bid in bids.items():
            decr_bid = self.ad_prov_decr_table[ad_prov][encr_bid]
            if decr_bid > max_bid:
                max_bid = decr_bid
                winner = ad_prov

        user.receive_winning_ad(self.ad_prov_ads[winner])



p = Platform(None)
nik = User(p)
apple = AdProvider(p,5,"Buy an iPhone")
sam = AdProvider(p,15,"Buy a Galaxy")
p2 = Platform(p)
siby = User(p)
p3 = Platform(p)
print("Siby's ad:")
siby.get_bids(15)
print("Nik's ad:")
nik.get_bids(5)

# print(siby.ad_prov_encr_table)
# print(nik.ad_prov_encr_table)

print(siby.score)
print(nik.score)