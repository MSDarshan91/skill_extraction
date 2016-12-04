
# Extracting Skills from Personal Communication Data using StackExchange Dataset

In this project, we will see how to make use of the stack exchange publicly available dump to extract skills from the communication data. This project was implemented on an openstack linux platform.

###Downloading the dataset
First, download the entire stack exchange dataset from [here](https://archive.org/details/stackexchange). There are many stackexchange websites like stackoverflow, cs, datascience, physics, history and so on. One can download the necessary compressed files or one can download the entire dump using torrents. More information about downloading the torrent files from command line can be found [here](https://www.learn2crack.com/2013/10/download-torrent-using-terminal.html). Each 7z file corresponds to a stackexchange website. Since we are interested only in technical websites, delete 7z files corresponding to websites like japanese.stackexchange, spanish.stackexchange and so on. After downloading the files extract the 7z files (Can be done in one script).

###Building the Knowledge Base
In this project, we implemented a K-NN multi label classification model using lucene. A very nice explanation of setting up pylucene is given [here](http://bendemott.blogspot.fi/2013/11/installing-pylucene-4-451.html).  To build this search engine, first we need to index all the posts with two fields 'text' and 'tags'. 
This process is done over all folders and indexed into one file system. Run the `indexer.py` program in the directory where all the extracted folders are present. This might take some hours to complete. But this is run only once.

```
python indexer.py
```
A folder called `index` is created.
###Extracting the skills
After building the knowledge base, next step is use the `searcher_text()` in `searcher.py` to extract the skills.
The folder `index` will be used in  `searcher.py`.
Open python and:
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
###Testing the application on Apache Spark Mailing Lists Dataset
Download the mbox file from (http://mail-archives.apache.org/mod_mbox/spark-dev/201511.mbox). 
Run the file apache_spark_example.py. One can see the output like in apache_spark_output.txt 

