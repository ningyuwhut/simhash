#!usr/bin/python
#coding=utf-8

import re
import hashlib

class simhash(object):

    def __init__(self,tokens="", num_of_hash_bits=64):
	self.num_of_hash_bits = num_of_hash_bits
	self.tokens=tokens
#	self.hash = self.simhash(tokens)
	def _hashfunc(x):
	    return int(hashlib.md5(x).hexdigest(),16) #返回16进制的hash值
	self.hashfunc = _hashfunc
	self.hashvalue = None

    def _tokenize(self): #返回特征向量
	ans = []
	content = self.tokens.lower()
#	print "content : ", content
	content = ''.join(re.findall(ur'[\w\u4e00-\u9fff]+',content)) #识别后的字符串
	#4e00-9fff是汉字的unicode 编码范围
	return content

    def build_by_text(self):
	features=self._tokenize()
	self.build_by_features(features)

#对特征向量中的每个字符得到hash值，然后求整个向量的hash值
    def build_by_features(self, features):
	hashes = [ self.hashfunc(w.encode('utf-8')) for w in features ] #每个字符生成hash值
	#print "hashes" , hashes
	v = [0]*self.num_of_hash_bits
	masks = [1<< i for i in xrange(self.num_of_hash_bits)] #为特征向量的每一位生成一个掩码
	#print "mask", masks
	#print "length" , len(masks)
	for h in hashes:
	    for i in xrange(self.num_of_hash_bits): #看每个特征的每一位上是否为1，如果为1则在最终的hash值上对应的位上加一,否则减一
		if h & masks[i] :
		    v[i] += 1   #这里不应该换成权重
		else:
		    v[i] -= 1
	#对于最后的hash值，如果整个特征向量的某一位为1，则设置最后的hash值的对应位为1,否则置为0
	#print "v", v
	ans = 0
	for i in xrange(self.num_of_hash_bits):
	    if v[i] > 0 :
		ans |= masks[i]
	
	self.hashvalue=ans
#求海明距离
    def num_of_different_bit(self, a_simhash):
	x = (self.hashvalue^a_simhash.hashvalue) & ((1<<self.num_of_hash_bits)-1)
	ans=0
	while x :
	    ans+=1
	    x &= (x-1)
	return ans
	
class SimhashContainer(object):
    def __init__(self, num_of_hash_bits=64, threshold=3):
	self.threshold=threshold
	self.num_of_hash_bits=num_of_hash_bits
	self.simhash_list=[] #存储所有对象的simhash值

    def add(self, a_simhash):
	self.simhash_list.append(a_simhash)
    def delete(self, a_simhash):
	del self.simhash_list[index]
    def find_duplicate(self):
	simhash_need_to_delete=[]
	i =0 
	while i < len(self.simhash_list):
	    j=i+1
	    while (j not in simhash_need_to_delete) and (j < len(self.simhash_list) ):
		if self.simhash_list[i].num_of_different_bit(self.simhash_list[j])<=3:
		    simhash_need_to_delete.append(j)
		    print self.simhash_list[i].tokens , self.simhash_list[j].tokens
		j+=1
	    i+=1

if __name__ == '__main__':
    s = u"你好啊"
    w = u"你好啊，"
    print "s", s
    hash1=simhash(s)
    feature_vector=hash1._tokenize()
    print "feature_vector", feature_vector

    a=hash1.build_by_text()
    print "a", hash1.hashvalue

    hash2=simhash(w)
    feature_vector2=hash2._tokenize()
    print "feature_vector2", feature_vector2

    b=hash2.build_by_text()
#    b=hash2.build_by_features(feature_vector2)
    print "b", hash2.hashvalue
    
    dd = hash1.num_of_different_bit(hash2)

    print "dd", dd

    container = SimhashContainer() 
    container.add(hash1)
    container.add(hash2)
    container.find_duplicate()
