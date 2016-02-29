import sys
class Fol:
	def __init__(self,inputFile):
		# init knowledge baes and query
		with open(inputFile) as f:
			self.initKb(f)
		print self.kb
		print self.query
		# query and infer uding backforward-chaining alg
		with open("output.txt","w") as f:
			for q in self.query : 
				for s in self.ask(self.kb,q,f) :
					print s
	def initKb(self,file):
		self.kb=[] 
		self.query=self.generate_query(file.readline().strip())
		kb_num=int(file.readline().strip())
		for i in range(kb_num):
			self.kb.append(self.generate_clause(file.readline().strip()))
	
	def generate_query(self, query):
		querys=[]
		for q in query.split(" && "):
			querys.append(self.generate_predicate(q))
		return querys
	def generate_clause(self,clause):
		
		# implication   term1 && term2 && term3 =>term1(lhs => rhs) term(args(list), ops(str))
		kbEntry={"lhs":[],'rhs':{}}
		index=clause.find(" => ")
		if not index==-1:
			for term in clause[:index].split(" && "):
				kbEntry["lhs"].append(self.generate_predicate(term))
			index+=3;

		index+=1 # make it  point to start of rhs
		kbEntry["rhs"]=self.generate_predicate(clause[index:])
		return kbEntry
	def generate_predicate(self,term):
		predicate={}
		predicate["ops"]=term[:term.find("(")]
		predicate["args"]=term[term.find("(")+1:-1].split(", ")
		return predicate
	def ask(self,kb,query,output):
		
		return self.fol_bc_or(kb,query,{})

	def fol_bc_or(self,kb,goal,theta):
		print "sadfsad"
		for (lhs,rhs) in self.fetch_rules_for_goals(kb,goal):
			print lhs,rhs
			(lhs,rhs)= self.standardize_variables(lhs,rhs)
			for x in self.fol_bc_and(kb,lhs,self.unify(rhs,goal,theta)):
				yield x
	def standardize_variables(self,lhs,rhs):
		return(lhs,rhs)			
	def fol_bc_and(self,kb,goal,theta):
	 	if theta==None: return
	 	elif len(goal)==0: yield theta
	 	else: 
	 		first,rest=goal[0],goal[1:]
	 		for  x in self.fol_bc_or(kb,self.subst(theta,first),theta):
	 			for y in self.fol_bc_and(kb,rest,x):
	 				yield y
	def subst(self,theta,first):
		for f in first:
			for i in range(len(first["args"])):
				if first["args"][i] in theta:
					first["args"][i]=theta[first["args"][i]] 
	def fetch_rules_for_goals(self,kb,goal):
		print "asdf" , kb , goal
		return [ (k["lhs"],k["rhs"]) for k in kb if k["rhs"]["ops"]==goal["ops"] ]
	def unify(self,x,y,theta): # theta is dictionary key is variable,value is constant to substiteu
		if theta is None : return None ## None means failure
		elif x==y: return theta
		elif type(x) is str and x[0].islower() : return self.unify_var(x,y,theta)
		elif type(y) is str and y[0].islower():  return self.unify_var(y,x,theta)
		elif type(x) is dict and type(y) is dict: return self.unify(x["args"],y["args"],self.unify(x["ops"],y["ops"],theta))
		elif type(x) is list  and type(y) is list: return self.unify(x[1:],y[1:],self.unify(x[0],y[0],theta))
		else: return None

	def unify_var(self,var,x,theta):
		if  var in theta: return unify(theta[var],x,theta)
		elif x in theta: return unify(var,theta[x],theta)
		# elif occur_check(var,x):return failure
		else : theta[var]=x;return theta


if __name__=='__main__':
	if len(sys.argv)!=3 or sys.argv[1]!='-i':
		print "input error"
		sys.exit()
	fol=Fol(sys.argv[2])