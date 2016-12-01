import xml.etree.ElementTree as ET
import math
import pickle
import os
import sys
import lucene
import re
from BeautifulSoup import BeautifulSoup
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field , StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

lucene.initVM()
indexDir = SimpleFSDirectory(File("index/"))
writerConfig = IndexWriterConfig(Version.LUCENE_48, StandardAnalyzer(Version.LUCENE_48))
writer = IndexWriter(indexDir, writerConfig)
def clean_text(html):
	soup = BeautifulSoup(html)
	invalid_tags = ['code']
	for tag in soup.findAll(True):
		if tag.name in invalid_tags:
	        	tag.replaceWith('')
	text = soup
	query_text = re.sub('<[^<]+?>', '', str(text)).replace('\n',' ')
	return query_text



stack_tags_count = {}
def countTags(tags):
        sp_tags = tags.split('>')
        for t in sp_tags[:-1]:
                t = t.replace("<","").replace("-"," ")
                if(t not in stack_tags_count):	
                	stack_tags_count[t] = 0 
                stack_tags_count[t] += 1



def index_documents(direct):
        tags_id = {}
        print "%d docs in index" % writer.numDocs()
        with open('Posts.xml', "r") as infile:
                next(infile)
                next(infile)
                for line in infile:
                        try:
                                row = ET.fromstring(line)
                                score = int(row.attrib['Score'])
                                if(score < 0):
                                        continue
                        except Exception as e:
                                continue
                        title = ''
                        idd = ''
                        sp_tags = []
                        tags = ''
                        pType = int(row.attrib['PostTypeId'])
                        if(pType > 2):
                                continue
                        if(pType==1):
                                tags = row.attrib['Tags']
                                #sp_tags = tags.split('>')
                                idd = row.attrib['Id']
                                title = row.attrib['Title']
                                tags_id[idd] = tags
                        else:
                                idd = row.attrib['Id']
                                idd_p= row.attrib['ParentId']
                                if(idd_p in tags_id):
                                        tags = tags_id[idd_p]
                        body = row.attrib['Body']
			body = clean_text(body)
                        doc = Document()
			doc.add(Field("PostType",str(pType),Field.Store.YES, Field.Index.ANALYZED))
                        doc.add(Field("Id",idd,Field.Store.YES, Field.Index.ANALYZED))
                        doc.add(Field("Title",title,Field.Store.YES, Field.Index.ANALYZED))
                        doc.add(Field("Tags",tags,Field.Store.YES, Field.Index.ANALYZED))
			countTags(tags)
			doc.add(Field("Stack",direct,Field.Store.YES, Field.Index.ANALYZED))
			sp_tags = tags.split('>')
			for t in sp_tags:
                                t = t.replace("<","").replace("-"," ")
				body = body +' '+t
                        #for t in sp_tags:
                                #t = t.replace("<","").replace("-"," ")
                                #doc.add(Field("Tags",t,Field.Store.YES, Field.Index.ANALYZED))
                        doc.add(Field("Body",body,Field.Store.YES, Field.Index.ANALYZED))
                        writer.addDocument(doc)
                        if(writer.numDocs()%100000 == 0):
                                print 'added doc, Total docs Now:', writer.numDocs()
        print "Closing index of %d docs..." % writer.numDocs()



directories = os.listdir('.')
#for subdir, dirs, files in os.walk("."):
#    if(dirs):
#        directories = dirs

print directories
cwd = os.getcwd()
for direct in  directories:
        if('.' in direct):
		continue
	cd = cwd + "/" +direct
        os.chdir(cd)
        print  os.getcwd()
	if(not (os.path.isfile('Posts.xml'))):
                continue
	index_documents(direct)	

os.chdir(cwd)
writer.close()

pickle.dump(stack_tags_count, open( "stack_count_tags.p", "wb" ) )
