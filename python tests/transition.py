states=set()
transitions={}

init_transitions={}
transitions_prob={}

data=[["good","morning"],
	  ["good","morning"],
	  ["good","morning"],
	  ["good","morning"],
	  ["good","morning"],
	  ["good","morning"],
	  ["i","like","you","hey"]]
for x in data:
	for j in x:
		states.add(j)

for x in states:
	print(x)
	transitions[x]={}
	transitions_prob[x]={}
	init_transitions[x]=0
	for j in states:
		transitions[x][j]=0
		transitions_prob[x][j]=0

for x in data:
	for j in range(len(x)-1):
		transitions[x[j]][x[j+1]]+=1
		if j==0:
			init_transitions[x[j]]+=1

for k,v in transitions.items():
	total = sum(v.values())
	if total != 0:
		for key,val in v.items():
			# print(k, sum(v.values()))
			transitions_prob[k][key] = val/total

print(transitions)
print(init_transitions)
print(transitions_prob)