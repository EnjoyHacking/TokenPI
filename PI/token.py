class Token:
	def __init__(self, token, encode, associateToken):
		self.token = token
		self.encode = encode
		self.associateToken = associateToken
	
	def __str__(self):
		return "%s, %d, 0x%x, %s" % (t.getToken(), t.getEncode(), t.getEncode(), t.getAssociateToken())

	def __repr__(self):
		return "%s, %d, 0x%x, %s" % (t.getToken(), t.getEncode(), t.getEncode(), t.getAssociateToken())

	def getToken(self):
		return self.token

	def getEncode(self):
		return self.encode

	def getAssociateToken(self):
		return self.associateToken



if __name__ == "__main__":

	filename = "../token.txt"
	token_dict = {}
	try:
		fd = open(filename, "r")
	except:
		raise IOError
	
	while 1:
		line = fd.readline().strip('\n')
		if not line:
			break
		fields = line.split(',')
		print line
		t =  Token(fields[0], int(fields[1]), fields[3])
		if int(fields[1]) not in token_dict:
			token_dict[int(fields[1])] = [t]
		else:
			token_dict[int(fields[1])].append(t)

	print "size : %d" % len(token_dict)
	print "keys size : %d" % len(token_dict.keys())
	print "values size : %d" % len(token_dict.values())

	for k, v in token_dict.items():
		print k, len(v)
		for t in v:
			print t




	
