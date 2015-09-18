
"""
Consensus module
Generate consensus based on multiple sequence alignment

Written by Marshall Beddoe <mbeddoe@baselineresearch.net>
Copyright (c) 2004 Baseline Research

Licensed under the LGPL
"""

from curses.ascii import *
from token import Token 

class Output:

    def __init__(self, sequences):

        self.sequences = sequences
        self.consensus = []
        self._go()

    def _go(self):
        pass

class Ansi(Output):

    def __init__(self, sequences):

        # Color defaults for composition
	self.gap = "\033[41;30m%s\033[0m" #deepred
        self.printable = "\033[42;30m%s\033[0m" #green
        self.space = "\033[43;30m%s\033[0m" #yellow
        self.binary = "\033[44;30m%s\033[0m" #blue
        self.zero = "\033[45;30m%s\033[0m" #purple
        self.bit = "\033[46;30m%s\033[0m" #deepgreen
        self.default = "\033[47;30m%s\033[0m" #white
	self.ordinary_token = "\033[40;37m%s\033[0m" #black
	self.position_specific_token = "\033[40;33m%s\033[0m" #black

        Output.__init__(self, sequences)

    def _go(self):

        seqLength = len(self.sequences[0][1])
        rounds = seqLength / 18
        remainder = seqLength % 18
        l = len(self.sequences[0][1])

        start = 0
        end = 18

        dtConsensus = []
        mtConsensus = []

        for i in range(rounds):
            for id, seq in self.sequences:
                print "%04d" % id,
                for byte in seq[start:end]:
	    	    if byte > 257:
		        print self.ordinary_token % "x%03x" % byte,
		    elif byte < 0:
			print self.position_specific_token % "x%03x" % byte,
                    elif byte == 256:
                        print self.gap % "____",
                    elif isspace(byte):
                        print self.space % "    ",
                    elif isprint(byte):
                        print self.printable % "x%03x" % byte,
                    elif byte == 0:
                        print self.zero % "x000",
                    else:
                        print self.default % "x%03x" % byte,
                print ""

            # Calculate datatype consensus

            print "DT  ",
            for j in range(start, end):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                dt = self._dtConsensus(column)
                print dt,
                dtConsensus.append(dt)
            print ""

            print "MT  ",
            for j in range(start, end):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                rate = self._mutationRate(column)
                print "%04d" % (rate * 100),
                mtConsensus.append(rate)
            print "\n"

            start += 18
            end += 18

        if remainder:
            for id, seq in self.sequences:
                print "%04d" % id,
                for byte in seq[start:start + remainder]:
		    if byte > 256:
		        print self.ordinary_token % "x%03x" % byte,
		    elif byte < 0:
		        print self.position_specific_token % "x%03x" % byte,
                    elif byte == 256:
                        print self.gap % "____",
                    elif isspace(byte):
                        print self.space % "    ",
                    elif isprint(byte):
                        print self.printable % "x%03x" % byte,
                    elif byte == 0:
                        print self.zero % "x000",
                    else:
                        print self.default % "x%03x" % byte,
                print ""

            print "DT  ",
            for j in range(start, start + remainder):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                dt = self._dtConsensus(column)
                print dt,
                dtConsensus.append(dt)
            print ""

            print "MT  ",
            for j in range(start, start + remainder):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                rate = self._mutationRate(column)
                mtConsensus.append(rate)
                print "%04d" % (rate * 100),
            print ""

        # Calculate consensus sequence
        l = len(self.sequences[0][1])

        for i in range(l):
            histogram = {}
            for id, seq in self.sequences:
                try:
                    histogram[seq[i]] += 1
                except:
                    histogram[seq[i]] = 1

            items = histogram.items()
            items.sort()

            m = 1
            v = 257  
            for j in items:
                if j[1] > m:
                    m = j[1]
                    v = j[0]

            self.consensus.append(v)

            real = []

            for i in range(len(self.consensus)):
                if self.consensus[i] == 256:
                    continue
                real.append((self.consensus[i], dtConsensus[i], mtConsensus[i]))

        #
        # Display consensus data
        #
        totalLen = len(real)
        rounds = totalLen / 18
        remainder = totalLen % 18

        start = 0
        end = 18

        print "\nUngapped Consensus:"

        for i in range(rounds):
            print "CONS",
            for byte,type,rate in real[start:end]:
                if byte == 256:
                   print self.gap % "____",
                elif byte == 257:
                    print self.default % "????",
                elif isspace(byte):
                    print self.space % "    ",
                elif isprint(byte):
                    print self.printable % "x%03x" % byte,
                elif byte == 0:
                    print self.zero % "x000",
                else:
                    print self.default % "x%03x" % byte,
            print ""

            print "DT  ",
            for byte,type,rate in real[start:end]:
                print type,
            print ""

            print "MT  ",
            for byte,type,rate in real[start:end]:
                print "%04d" % (rate * 100),
            print "\n"

            start += 18
            end += 18

        if remainder:
            print "CONS",
            for byte,type,rate in real[start:start + remainder]:
                if byte == 256:
                   print self.gap % "___",
                elif byte == 257:
                    print self.default % "????",
                elif isspace(byte):
                    print self.space % "    ",
                elif isprint(byte):
                    print self.printable % "x%03x" % byte,
                elif byte == 0:
                    print self.zero % "x000",
                else:
                    print self.default % "x%03x" % byte,
            print ""

            print "DT  ",
            for byte,type,rate in real[start:end]:
                print type,
            print ""

            print "MT  ",
            for byte,type,rate in real[start:end]:
                print "%04d" % (rate * 100),
            print ""

    def _dtConsensus(self, data):
        histogram = {}

        for byte in data:
	    if byte > 257:
		try:
		    histogram["O"] += 1
		except:
		    histogram["O"] = 1
	    elif byte < 0:
		try:
		    histogram["P"] += 1
		except:
		    histogram["P"] = 1
	    elif byte == 256:
		try:
                    histogram["G"] += 1
                except:
                    histogram["G"] = 1
            elif isspace(byte):
                try:
                    histogram["S"] += 1
                except:
                    histogram["S"] = 1
            elif isprint(byte):
                try:
                    histogram["A"] += 1
                except:
                    histogram["A"] = 1
            elif byte == 0:
                try:
                    histogram["Z"] += 1
                except:
                    histogram["Z"] = 1
            else:
                try:
                    histogram["B"] += 1
                except:
                    histogram["B"] = 1

        items = histogram.items()
        items.sort()

        m = 1
        v = '?'
        for j in items:
           if j[1] > m:
               m = j[1]
               v = j[0]

        return v * 4

    def _mutationRate(self, data):

        histogram = {}

        for x in data:
            try:
                histogram[x] += 1
            except:
                histogram[x] = 1

        items = histogram.items()
        items.sort()

        if len(items) == 1:
            rate = 0.0
        else:
            rate = len(items) * 1.0 / len(data) * 1.0

        return rate

#add by syf
class Signature(Ansi):

	def __init__(self, sequences, filename):

		self.token_dict = {}
		self.align_res = [] 
		self.opSequence = []
		
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
			t =  Token(fields[0], int(fields[1]), int(fields[2]), fields[3])
			if int(fields[1]) not in self.token_dict:
				self.token_dict[int(fields[1])] = [t]
			else:
				self.token_dict[int(fields[1])].append(t)

		Ansi.__init__(self, sequences)
		self._sig()

	def _sig(self):
		for j in range(0, len(self.sequences[0][1])):
			column = []
			for id, seq in self.sequences:
				column.append(seq[j])
			op = self._opSequence(column)
			self.opSequence.append(op)
		# Display operation sequence
		print "OP  ",
		for op in self.opSequence:
			print op * 4, 
		print ""
		i = 0
		mismatchCounter = 0
		indelCounter = 0
		flag = 0
		while i < len(self.consensus):
			byte = self.consensus[i]
			op = self.opSequence[i]
			if op == "M":
				if flag == 1:
					if indelCounter == 0:
						print ".{%d}" % mismatchCounter,
					else:
						print ".*",

				if byte in self.token_dict:
					
					if self.token_dict[byte][0].getAssociateToken() == "NULL":
						print self.ordinary_token % self.token_dict[byte][0].getToken(),
					else:
						print self.position_specific_token % \
							self.token_dict[byte][0].getAssociateToken(),
					i += self.token_dict[byte][0].getShortestLen()
					continue
				elif byte == 257:
					print self.default % "????",
				elif isspace(byte):
					print self.space % "    ",
				elif isprint(byte):
					print self.printable % "x%03x" % byte,
				elif byte == 0:
					print self.zero % "x000",
				else:
					print self.default % "x%03x" % byte,
				flag = 0		
				indelCounter  = 0
				mismatchCounter  = 0
			elif op == "U":
				if flag == 0:
					flag = 1
				mismatchCounter += 1
				i += 1
			elif op == "I":
				if flag == 0:
					flag = 1
				indelCounter += 1
			else:
				pass
			i += 1
		if flag == 1:
			if indelCounter == 0:
		   		print ".{%d}" % mismatchCounter,
		   	else:
		   		print ".*",
		print ""

	def _opSequence(self, data):
		histogram = {}
		for x in data:
		    try:
			histogram[x] += 1
		    except:
			histogram[x] = 1

		items = histogram.items()
		items.sort()
		operation = "" 
		if len(items) == 1:
			if 256 in histogram:
				operation = "I" #Indel
			else:
				operation = "M" #match 
		else:
			if 256 in histogram:
				operation = "I" #Indel
			else:
				operation = "U" #Mismatch
		return operation 
