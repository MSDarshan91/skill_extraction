import sys
import EFZP as zp
from bs4 import BeautifulSoup
import html2text
h = html2text.HTML2Text()
h.ignore_links = True
import quotequail
import lucene
import mailbox
import os
from searcher import *
#download the mbox file from http://mail-archives.apache.org/mod_mbox/spark-dev/201511.mbox
mails = mailbox.mbox("201511.mbox")

def addTags(user,tags,score):
        if(user not in tags_count_user):
                mails_count[user] = 0
                tags_count_user[user] = {}
        mails_count[user] +=1
        sp_tags = tags.split('>')
        for t in sp_tags[:-1]:
                t = t.replace("<","").replace("-"," ")
                if(t in tags_count_user[user]):
                        tags_count_user[user][t] += score
                else:
                        tags_count_user[user][t] = score

def get_mail_body(msg):
        body = ''
        maintype = msg.get_content_maintype()
        if maintype == 'text':
                charset = msg.get_content_charset()
                body = body + msg.get_payload(decode=True)
        body = body.decode('ascii','ignore')
        if(bool(BeautifulSoup(body, "html.parser").find())):
                body  = h.handle(body)
        z = quotequail.unwrap(body)

        if z is not None:
                if 'text_top' in z:
                    body = z["text_top"]
        body = zp.parse(body)['body']
        return body
mails_count = {}
tags_count_user = {}
import sys
sys.path.append('..')

print 'Started Reading Emails...'
for message in mails:
	
        _from = message['From']
	#print _from
        queryText = message['Subject']
        queryText += get_mail_body(message)
        #if(queryText == '' or  len(queryText) > 1000):
        #       continue
        #print queryText
        try:
                query = QueryParser(Version.LUCENE_48, "Body", analyzer).parse(queryText)
        except Exception  as e:
                continue
        MAX = 10
        hits = searcher.search(query, MAX)
        #print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
        for hit in hits.scoreDocs:
            if(hit.score > 0.0):
                #print hit.score
                doc = searcher.doc(hit.doc)
                tgs = doc.get("Tags")
                #print 'Tags:',hit.score,tgs.encode('ascii','ignore')
                addTags(_from,tgs,hit.score)


print 'Extracted skills are:'
sorted_users = sorted(mails_count.items(), key=lambda x: x[1], reverse=True)
j = 5
for u,v in sorted_users[:j]:
            tags_count = tags_count_user[u]
            user = u
            print 'User::::',user
            #print  display_clusters(tags_count)
            #rint summarize_clusters(tags_count,0) 
            sorted_words = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
            k = 15
            for word, score in sorted_words[:k]:
                    print '\t',word,score
