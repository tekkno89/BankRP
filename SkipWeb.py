import random, pickle

class SkipProxy:
	def __init__(self):
		self.usedProxy = []
		self.useProxy = ''
		self.proxies = pickle.load(open('proxies.tek','rb'))
		self.banned = pickle.load(open('banned.tek','rb'))
	
	
	def pick(self):
		self.pickNum = random.randrange(0,len(self.proxies))
		self.useProxy = self.proxies[self.pickNum]
		t = True
		while t:
			if self.useProxy in self.usedProxy:
				self.pickNum = random.randrange(0,len(self.proxies))
				self.useProxy = self.proxies[self.pickNum]
			else:
				t = False
		if len(self.usedProxy) == 10:
			del(self.usedProxy[0])
		self.usedProxy.append(self.useProxy)
		# print self.useProxy
		# print self.usedProxy
	
	
	def ban(self,proxy):
		print proxy, 'banned'
		str(proxy)
		self.banned.append(proxy)
		self.proxies.remove(proxy)
		pickle.dump(self.proxies, open('proxies.tek','wb'))
		pickle.dump(self.banned, open('banned.tek','wb'))
		