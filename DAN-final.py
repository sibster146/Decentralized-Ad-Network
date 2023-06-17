from collections import Counter
import random


REWARD = 10

class MalAdProvider:
    def __init__(self, algo_a, algo_b, ad, root, money):
        """
        Ad provider splits their bid algorithm 
        into two before entering system
        algo_a : for users (function g)
        algo_b : for ad provs (function h)
        """
        self.algo_a = algo_a
        self.algo_b = algo_b
        self.ad = ad
        self.key = hash(ad)
        self.users = set()
        self.money = money
        self.max_bid = float("inf")*-1

        self.ad_provs = set()
        self.ad_prov_algo_b = {}
        self.ad_prov_ads = {}

        if root:
            # copying fields from the root
            self.users = root.request_users().copy()
            self.ad_provs = root.request_ad_provs().copy()
            self.ad_prov_algo_b = root.request_ad_prov_algo_b().copy()
            self.ad_prov_ads = root.request_ad_prov_ads().copy()

            for ad_prov in self.ad_provs:
                ad_prov.send_self(self)
                ad_prov.send_algo_b(self,algo_b)
                ad_prov.store_ad(ad,self)
            for user in self.users:
                user.recieve_ad_provs(self)
                user.recieve_algo_a(self,self.algo_a)
                user.recieve_key(self,self.key)
        
        self.ad_provs.add(self)
        self.ad_prov_algo_b[self] = algo_b
        self.ad_prov_ads[self] = ad

    def request_users(self):
        return self.users
    def request_ad_provs(self):
        return self.ad_provs
    def request_ad_prov_algo_b(self):
        return self.ad_prov_algo_b
    def request_ad_prov_ads(self):
        return self.ad_prov_ads
    def send_self(self,node):
        self.ad_provs.add(node)
    def send_algo_b(self, node, algo_b):
        self.ad_prov_algo_b[node] = algo_b
    def store_ad(self,ad,sending_ad_prov):
        self.ad_prov_ads[sending_ad_prov] = ad

    def request_ad_prov_ads(self):
        return self.ad_prov_ads
    def request_algo_a(self):
        return self.algo_a
    def request_key(self):
        return self.key
    def recieve_user(self,user):
        self.users.add(user)
    def charge_winner(self, winner):
        winner.money = winner.money - self.max_bid
    def pay_user(self):
        return self.max_bid
    def send_ad(self, winner):
        listt = [0,0,1]
        n = random.choice(listt)
        if n == 0:
            return self.ad_prov_ads[self]
        return self.ad_prov_ads[winner]
    def malicious_actor(self, malicious_ad_prov, reward):
        print(f"{malicious_ad_prov} is a bad actor")
        self.money -= reward
        self.money += malicious_ad_prov.charge_ad_prov(reward)
    def charge_ad_prov(self,reward):
        self.money -= reward
        return reward
    
    def get_bids2(self,ad_provs_encrbids, user):
        self.max_bid = float("inf")*-1
        winner = None
        for ad_prov, encr_bid in ad_provs_encrbids:
            algo_b = self.ad_prov_algo_b[ad_prov]
            bid = algo_b(encr_bid)
            if bid > self.max_bid:
                self.max_bid = bid
                winner = ad_prov
        user.get_winner(winner)


















class AdProvider:
    def __init__(self, algo_a, algo_b, ad, root, money):
        """
        Ad provider splits their bid algorithm 
        into two before entering system
        algo_a : for users
        algo_b : for ad provs
        """
        self.algo_a = algo_a
        self.algo_b = algo_b
        self.ad = ad
        self.key = hash(ad)
        self.users = set()
        self.money = money
        self.max_bid = float("inf")*-1

        self.ad_provs = set()
        self.ad_prov_algo_b = {}
        self.ad_prov_ads = {}

        if root:
            # copying fields from the root
            self.users = root.request_users().copy()
            self.ad_provs = root.request_ad_provs().copy()
            self.ad_prov_algo_b = root.request_ad_prov_algo_b().copy()
            self.ad_prov_ads = root.request_ad_prov_ads().copy()

            for ad_prov in self.ad_provs:
                ad_prov.send_self(self)
                ad_prov.send_algo_b(self,algo_b)
                ad_prov.store_ad(ad,self)
            for user in self.users:
                user.recieve_ad_provs(self)
                user.recieve_algo_a(self,self.algo_a)
                user.recieve_key(self,self.key)
        
        self.ad_provs.add(self)
        self.ad_prov_algo_b[self] = algo_b
        self.ad_prov_ads[self] = ad

    def request_users(self):
        return self.users
    def request_ad_provs(self):
        return self.ad_provs
    def request_ad_prov_algo_b(self):
        return self.ad_prov_algo_b
    def request_ad_prov_ads(self):
        return self.ad_prov_ads
    def send_self(self,node):
        self.ad_provs.add(node)
    def send_algo_b(self, node, algo_b):
        self.ad_prov_algo_b[node] = algo_b
    def store_ad(self,ad,sending_ad_prov):
        self.ad_prov_ads[sending_ad_prov] = ad

    def request_ad_prov_ads(self):
        return self.ad_prov_ads
    def request_algo_a(self):
        return self.algo_a
    def request_key(self):
        return self.key
    def recieve_user(self,user):
        self.users.add(user)
    
    def charge_winner(self, winner):
        winner.money = winner.money - self.max_bid
    def pay_user(self):
        return self.max_bid
    def send_ad(self, winner):
        return self.ad_prov_ads[winner]
    def malicious_actor(self, malicious_ad_prov, reward):
        print(f"{malicious_ad_prov} is a bad actor")
        return malicious_ad_prov.charge_ad_prov(reward)
    def charge_ad_prov(self,reward):
        self.money -= reward
        return reward
    def get_bids2(self,ad_provs_encrbids, user):
        self.max_bid = float("inf")*-1
        winner = None
        for ad_prov, encr_bid in ad_provs_encrbids:
            algo_b = self.ad_prov_algo_b[ad_prov]
            bid = algo_b(encr_bid)
            if bid > self.max_bid:
                self.max_bid = bid
                winner = ad_prov
        user.get_winner(winner)
        

class User:
    def __init__(self, root):
        self.ad_provs = root.request_ad_provs().copy()
        self.ad_prov_algo_a = {}
        self.ad_prov_keys = {}
        self.winner = []
        self.money = 0
        for ad_prov in self.ad_provs:
            self.ad_prov_algo_a[ad_prov] = ad_prov.request_algo_a()
            self.ad_prov_keys[ad_prov] = ad_prov.request_key()
            ad_prov.recieve_user(self)

    def recieve_ad_provs(self,ad_prov):
        self.ad_provs.add(ad_prov)
    def recieve_algo_a(self,ad_prov,algo_a):
        self.ad_prov_algo_a[ad_prov] = algo_a
    def recieve_key(self,ad_prov,key):
        self.ad_prov_keys[ad_prov] = key


    def get_bids1(self,data):
        bid_dict = {}
        for ad_prov,algo_a in self.ad_prov_algo_a.items():
            output = algo_a(data)
            bid_dict[ad_prov] = output
        bid_items = list(bid_dict.items()) #list contains [ad prov, their encrypted bid value]
        for i in range(len(bid_items)):
            reci_ad_prov = bid_items[i][0]
            cal_ad_prov_list = bid_items[:i] + bid_items[i+1:]
            reci_ad_prov.get_bids2(cal_ad_prov_list, self)

    def get_winner(self,candidate):
        self.winner.append(candidate)
        if len(self.winner) == len(self.ad_provs):
            winner,count = Counter(self.winner).most_common()[0]
            if len(set(self.winner))!=2 or count != len(self.ad_provs)-1:
                print("SYSTEM COMPROMISED")
                return
            pinging_ad_prov = random.choice(list(filter(lambda x: x != winner, self.ad_provs)))
            #pinging_ad_prov = random.choice(list(filter(lambda x: type(x) == MalAdProvider, self.ad_provs)))
            pinging_ad_prov.charge_winner(winner)
            self.money += pinging_ad_prov.pay_user()
            winning_ad = pinging_ad_prov.send_ad(winner)
            ad_key = hash(winning_ad)
            while ad_key != self.ad_prov_keys[winner]:
                ### if the pinging ad prov does not forward the right ad ###
                if winner.malicious_actor(pinging_ad_prov,REWARD): # hard coding a $10 reward for the user for reporting the malicious ad provider
                    self.money += REWARD  # this will be so that the malicious ad provider pays the user
                    winning_ad = pinging_ad_prov.send_ad(winner)
                    ad_key = hash(winning_ad)
            print(winning_ad)
            self.winner.clear()
            

def f(x):
    return x+2
def g(x):
    return 2*x
def h(x):
    return 0
def j(x):
    return x+2
def k(x):
    return -2*x
def l(x):
    return -1*float("inf")
def m(x):
    return x-5
def n(x):
    return 3*x
apple = AdProvider(f,g,"Buy an iPhone",None,10000) #pos
samsung = AdProvider(h,j,"Buy a Galaxy", apple,10000) #flat
nik = User(samsung)
windows = AdProvider(f,k,"We still make phones?", samsung,10000) #neg
ibm = AdProvider(m,n,"Super computers :)",apple, 10000)# x > 20
siby = User(windows)
alek = User(apple)

print("Siby's winning ad:")
siby.get_bids1(-4)
# apple = -4, # samsung = 2, # windows = 4, # ibm = -27
assert siby.money == 4
assert windows.money == 9996
assert apple.money == 10000
assert samsung.money == 10000
assert ibm.money == 10000
print("\n")

print("Nik's winning ad:")
nik.get_bids1(-2)
# apple = 0, samsung = 2, windows = 0, ibm = -21
assert nik.money == 2
assert samsung.money == 9998
assert windows.money == 9996
assert apple.money == 10000
assert ibm.money == 10000
print("\n")

print("alek's winning ad:")
alek.get_bids1(0)
# apple = 4, samsung = 2, windows = -4, ibm = -15
assert alek.money == 4
assert apple.money == 9996
assert samsung.money == 9998
assert windows.money == 9996
assert ibm.money == 10000
print("\n")

print("Nik's winning ad:")
nik.get_bids1(20)
# apple = 44, samsung = 2, windows = -44, ibm = 45 
assert nik.money == 47
assert ibm.money == 9955
assert apple.money == 9996
assert samsung.money == 9998
assert windows.money == 9996
print("\n")


# goldman = MalAdProvider(h,l,"We are not corrupt",windows,10000)
# print("Siby's winning ad")
# siby.get_bids1(0)
# # apple = 4, samsung = 2, windows = -4, ibm = -15
# print(goldman.money)
# print(siby.money)
# assert apple.money == 9996
# assert windows.money == 10000
# assert samsung.money == 10000
# assert ibm.money == 10000






