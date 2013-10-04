import operator

f = open('TRAIN.txt', 'r')
stop=open('stop.txt','r')

#stopwords
stopwords=['the']
for line in stop:
	word=''.join(e for e in line if e.isalpha())
	stopwords.append(word)
stop.close()
####

#find numpolitics numsports
numsports=0
numpolitics=0
for line in f:
	s=line.split(' ', 2)[2]
	clas=line.split(' ',2)[1]
	if clas=="Sports":
		numsports+=1
	else:
		numpolitics+=1
f.close()
f=open('TRAIN.txt','r')
####


#dict creation
sports={'cricket':0}
politics={'president':0}
wsport=0
wpol=0

for line in f:
	clas=line.split(' ',2)[1]
	content=line.split(' ', 2)[2]
	swf=''.join(e for e in content if e.isalpha() or e==' ' or e=='#').lower()
	words=swf.split()
	for word in words:
		if clas=="Sports":
			
			if word in sports:
				sports[word]+=1
				wsport+=1

			elif word not in sports and word not in stopwords:
				sports[word]=1
				wsport+=1

		elif clas=="Politics":
			
			if word in politics:
				politics[word]+=1
				wpol+=1
			elif word not in politics and word not in stopwords:
				politics[word]=1
				wpol+=1
f.close()
####

#find prob of sports
probsports=float(numsports)/(float(numpolitics)+float(numsports))
probpol=1-probsports
####


##find prob of feature given this class
probabilitywordspol={'the':0}
probabilitywordssports={'the':0}
for word in politics:
	probabilitywordspol[word]=politics[word]/float(wpol)
	probabilitywordspol[word]=probabilitywordspol[word]*(10**5)
for word in sports:
	probabilitywordssports[word]=sports[word]/float(wsport)
	probabilitywordssports[word]=probabilitywordssports[word]*(10**5)

####
##now validate
f=open('test.txt','r')
g=open('Results.txt','w')
for line in f:
	content=line.split(' ', 1)[1]
	valdict={'aaaaaa':0}
	valswf=''.join(e for e in content if e.isalpha() or e==' ' or e=='#').lower()
	valwords=valswf.split()
	for word in valwords: 

		if word not in stopwords:
			if word in valdict:
				valdict[word]+=1
			else:
				valdict[word]=1
		#now find prob of sports given the words in valdict	
	problineissports=probsports
	for word in valdict:
		if word in sports:
			if valdict[word]>=1:
				problineissports=problineissports**valdict[word]
				problineissports=problineissports*probabilitywordssports[word]

	problineispol=probpol
	for word in valdict: 
		if word in politics:
			if valdict[word]>=1:
				problineispol=problineispol*valdict[word]
				problineispol=problineispol*probabilitywordspol[word]
	if problineissports>problineispol:
		g.write(line.split(' ', 1)[0]+" Sports\n")

	else:
		g.write(line.split(' ', 1)[0]+" Politics\n")
