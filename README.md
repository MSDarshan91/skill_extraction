
# Extracting Skills from Personal Communication Data using StackExchange Dataset

In this project, we will see how to make use of the stack exchange publicly available dump to extract skills from the communication data. This project was implemented on an openstack linux platform.

###Downloading the dataset
First, download the entire stack exchange dataset from [here](https://archive.org/details/stackexchange). There are many stackexchange websites like stackoverflow, cs, datascience, physics, history and so on. One can download the necessary compressed files or one can download the entire dump using torrents. More information about downloading the torrent files from command line can be found [here](https://www.learn2crack.com/2013/10/download-torrent-using-terminal.html). After downloading the files extract the 7z files (Can be done in one script). Each 7z file corresponds to a stackexchange website. Since we are interested only in technical websites, delete 7z files corresponding to websites like japanese.stackexchange, spanish.stackexchange and so on.

###Building the Knowledge Base
We will only be using the Posts.xml file in every folder. A post in stack exchange is either a question, answer or a comment. Each post will be associated with a set of tags. We consider these tags as skills. We use this stack exchange knowledge base as a training set to predict the tags. In this project, we implemented a K-NN multi label classification model using lucene. A very nice explanation of setting up pylucene is given [here](http://bendemott.blogspot.fi/2013/11/installing-pylucene-4-451.html).  To build this search engine, first we need to index all the posts with two fields 'text' and 'tags'. 
```
doc.add(Field("Body",body,Field.Store.YES, Field.Index.ANALYZED))
doc.add(Field("Tags",tags,Field.Store.YES, Field.Index.ANALYZED))
```
The 'text' field is the body of the post with some pre processing. This process is done over all folders and indexed into one file system. The code to build the knowledge base is indexer.py. Run this indexer.py program in the directory where all the extracted folders are present. This might take some hours to complete. But this is run only once.

```
python indexer.py
```

###Extracting the skills
If we are given a set of messages (from an instant messaging platform) of an individual, the task is to predict the tags for each message. A message is used as a query to the search engine. The searching is done on the 'text' field.  A score is associated with every tag and it is initialized to zero. We retrieve top k most similar posts associated with the message along with the similarity value and tags. The similarity value is added to the tags. This is done for each message and finally the tags which have larger values are declared as the skills of an individual. 

```
In [1]: from searcher import *
In [2]: searcher_text('''I want to get a list of the column headers from a pandas DataFrame. The DataFrame will come from user input so I won't know how many columns there will be or what they will be called.''')

Out[2]: 
[u'pandas',
 u'dataframes',
 u'python',
 u'python 3.x',
 u'python 2.7']
```


