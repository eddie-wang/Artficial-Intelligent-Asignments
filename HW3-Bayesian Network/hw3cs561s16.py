import sys
import  copy
class HW3:
	def __init__(self,input_file):
		"""
			1.construct query
			2.construct bn
			3.execute query based on query type
		"""
		with open(input_file) as f:
			self.construct_query(f)
			self.construct_bn(f)
		with open("output.txt","w") as output:
			self.execute(output)
	def construct_query(self,file):
		self.queries=[]
		"""
			query={"type":"P/Eu/Meu", "query":{"var":boolean }/[vars] if meu , eveidence:"null"/{"var""boolean} }
		"""
		def parse(s):
			r=s.split(" = ")
			r[1]=0 if r[1]=='-' else 1
			return r
		for line in iter(file.readline,"*"*6+'\n'):
			line=line.strip()
			index=line.find("(")
			query={}
			query["type"]=line[:index]
			line=line[index+1:-1]
			temp=line.split(' | ')
			if not query["type"]=="MEU":
				query["query"]={var:value for (var,value) in map(parse,temp[0].split(", "))}
			else : query["query"]=[var for var in temp[0].split(", ")]
			query["evidence"]={var:value for (var,value) in map(parse,temp[1].split(", "))} if len(temp)==2 else dict()
			print query
			self.queries.append(query)
	def construct_bn(self,file):
		def get_index(l):
			return sum([ (1<<(len(l)-i-1))*(1 if l[i]=='+' else 0) for i in range(len(l))])
		self.bn=Bayesian_Network() 
		while True:
			line=file.readline().strip()
			t=line.split(" | ") 
			if len(t)==1:
				self.bn.parents[t[0]]=None
			else: self.bn.parents[t[0]]=t[1].split(' ')
			if not t[0]=="utility": self.bn.vars.append(t[0])
			size=pow(2,len(t[1].split(' ')) if len(t)==2 else 0)
			self.bn.cpt[t[0]]=[ 1 for i in range(size)]
			for i in range(size):
				l=file.readline().strip().split(" ")
				index=get_index(l[1:])
				if l[0]=="decision": self.bn.decision.append(t[0]);break;
				self.bn.cpt[t[0]][index]=float(l[0])
			if not file.readline():break
		print self.bn.cpt
	def execute(self,output):
		alg={"P":self.enumeration}
		for query in self.queries:
			print "{0:.2f}".format(alg[query["type"]](query))
	def enumeration(self,query):
		"""
			suppose when given  evidence there is only one  
		"""
		if query["evidence"]:
			var=query["query"].keys()[0]
			a=self.enumerate_all(self.bn.vars,dict(query["evidence"].items()+[(var,1)]))
			b=self.enumerate_all(self.bn.vars,dict(query["evidence"].items()+[(var,0)]))
			return a/(a+b) if query["query"][var] else b/(a+b)
		else:
			return self.enumerate_all(self.bn.vars,dict(query["query"].items()))
	def enumerate_all(self,var,e):
		# print var,e,"***"
		if not var: return 1
		y=var[0]
		if y in e:
			parent=self.bn.parents[y]
			t=self.p_of_y_given_parent(y,e)*self.enumerate_all(var[1:],e)
			# print t
			return t
		else:
			e[y]=0
			r=self.p_of_y_given_parent(y,e)*self.enumerate_all(var[1:],copy.deepcopy(e))
			e[y]=1
			t=r+self.p_of_y_given_parent(y,e)*self.enumerate_all(var[1:],copy.deepcopy(e))
			# print t
			return t		
	def p_of_y_given_parent(self,y,e):
		index=0
		parent=self.bn.parents[y]
		if not parent:
			return self.bn.cpt[y][0] if e[y]==1 else 1-self.bn.cpt[y][0]
		for i,p in enumerate(parent):
			index=(index<<1)+e[p]
		# print y,e,parent,index,"ASADDAS"
		return self.bn.cpt[y][index] if e[y]==1 else 1-self.bn.cpt[y][index]
	def eu(self,query):
		return "not yet"
	def meu(self,query):
		return "not yet"

class Bayesian_Network:
	def __init__(self):
		self.cpt={}
		self.parents={}
		self.vars=[]
		self.decision=[]
		
if __name__=="__main__":
	if len(sys.argv)!=3 or sys.argv[1]!="-i":
		print "input error"
		sys.exit()
	bn= HW3(sys.argv[2])