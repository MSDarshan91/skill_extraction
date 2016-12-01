import sys
import math
import lucene
from lucene import *
#import mailbox
import os 
import string
from java.io import File
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search import BooleanQuery,TermQuery
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import Term
from org.apache.lucene.util import Version
import re
#from textblob import Blobber
#from textblob_aptagger import PerceptronTagger
#tb = Blobber(pos_tagger=PerceptronTagger())
from nltk.corpus import stopwords
stop = stopwords.words('english')
from nltk import tokenize
from collections import OrderedDict
import pickle
def getPhrases(text):
    np = tokenize.word_tokenize(text)
    ret = []
    for t in np:
        temp = ' '.join([word for word in t.split() if word not in set(string.punctuation)  and word not in stop] )
        if (temp not in(' ', '')):
            ret.append(temp)
    return ret


stack_tags_count = pickle.load(open("stack_count_tags.p", "rb"))
def addTags(tags,score,tags_count):
	sp_tags = tags.split('>')
	for t in sp_tags[:-1]:
		t = t.replace("<","").replace("-"," ")
		if(t in stack_tags_count):
			if(t in tags_count):
				tags_count[t] += score
			else:
				tags_count[t] = score
	
lucene.initVM()
analyzer = StandardAnalyzer(Version.LUCENE_48)
reader = IndexReader.open(SimpleFSDirectory(File("index/")))
searcher = IndexSearcher(reader)

def searcher_text(text):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    tags_count = {}
    sentences = tokenize.sent_tokenize(text)
    t_phrases = []
    for sentence in sentences:
	    sentence = sentence.replace('\n',' ')
	    #print sentence
	    t_phrases = sentence.split()
	    t_phrases = [p.lower() for p in t_phrases]
	    query = BooleanQuery()
            query.setMinimumNumberShouldMatch(1)
	    i = 0
	    phrases = getPhrases(sentence)
	    t_phrases = t_phrases + phrases
    	    for k in t_phrases:
	        for t in k.split():
                    if(i < 1000):
			query.add(TermQuery(Term("Body", t)),BooleanClause.Occur.SHOULD)
            	    i = i+1
	    MAX = 5
            hits = searcher.search(query, MAX)
            for hit in hits.scoreDocs:
                if(hit.score > 0.0):
                    doc = searcher.doc(hit.doc)
                    tgs = doc.get("Tags")
                    score = hit.score
                    addTags(tgs,score,tags_count)
    for tg in tags_count:
        tags_count[tg] = tags_count[tg] / float(1+math.log(stack_tags_count[tg]))
    sorted_words = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
    k = 25
    ret = []
    for word, score in sorted_words[:k]:
	ret.append(word)	
    return ret


