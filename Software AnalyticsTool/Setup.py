import csv
import os

import sys

import tkinter
import operator
import time
import pandas as pd

# Path for spark source folder
os.environ['SPARK_HOME']="/Users/avneet/opt/packages/spark/spark-1.5.1-bin-hadoop2.6"

os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3.4"

# Append pyspark  to Python Path
sys.path.append("/Users/avneet/opt/packages/spark/spark-1.5.1-bin-hadoop2.6/python")


try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)



from pyspark.mllib.stat import Statistics
sc = SparkContext()

def delete_widget_children(widget):
    for child in widget.winfo_children():
        child.grid_remove()


from pyspark.mllib.fpm import FPGrowth
data = sc.textFile('/Users/avneet/Downloads/Transactions.txt')
# read the input file line by line and split it based on whitespaces & return a set of tokens
transactions = data.map(lambda line: line.strip().split(","))
model = FPGrowth.train(transactions, minSupport=0.02, numPartitions=20)
result = model.freqItemsets().collect()
frequent_itemsets = []
for fi in result:
    frequent_itemsets.append(fi)


#Write frequent itemsets to Tableau for analysis
with open("frequent_itemsets.txt", "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	for frequent_itemset in frequent_itemsets:
		writer.writerow([frequent_itemset.items, frequent_itemset.freq])
#Creating a dict for efficient indexing

#Find top 3 authors for each file
auth_info = pd.read_csv('/Users/avneet/Downloads/GetTopAuthors.txt', header= 0 , sep=',')
auth_info.columns = ["file_name","author","count"]

#Find category count for each file
category_info = pd.read_csv('/Users/avneet/Downloads/GetTopCommits.txt', header= 0 , sep=',')
category_info.columns = ["file_name","Addition","Deletion","BugFix"]

#Find last 5 commit messages for each file
commit_info = pd.read_csv('/Users/avneet/Downloads/GetRecent5Commits.txt', header= 0 , sep=',')
commit_info.columns = ["file_name","commit_msg"]

#Read file counts for support calculations
support_info = pd.read_csv('/Users/avneet/Downloads/Support.txt', header= 0 , sep=',')
support_info.columns = ["file_name","support"]

rule_index = {}
for frequent_itemset in frequent_itemsets:
    #print(frequent_itemset)
    for current_file in frequent_itemset.items:
         orig_rule = frequent_itemset.items[:]
         if current_file in rule_index.keys():
             rule_list = rule_index[current_file]
         else:
             rule_list = []
         orig_rule.remove(current_file)
         if len(orig_rule) > 0 and orig_rule not in rule_list:
             support_count = support_info[support_info['file_name'] == current_file]
             for i,row in support_count.iterrows():
                 support = row["support"]
             confidence = (frequent_itemset.freq/float(support))
             confidence = "%.3f" % confidence
             tup = (orig_rule,frequent_itemset.freq, confidence)
             rule_list.append(tup)
             rule_index[current_file] = rule_list
# # #print(rule_index)
# # cnt = 0
def generateRecommendations():
    # group = tkinter.LabelFrame(window, text="Results", padx=5, pady=5)
    # group.pack(padx=10, pady=10)
    df = auth_info[auth_info['file_name'] == input.get()]
    authors = list(df['author'])

    df1 = category_info[category_info['file_name'] == input.get()]
    for i,row in df1.iterrows():
        addition_count = row['Addition']
        deletion_count = row['Deletion']
        bugfix_count = row['BugFix']

    df2 = commit_info[commit_info['file_name'] == input.get()]
    commit_msgs = list(df2['commit_msg'])
    changed_file = input.get()

    delete_widget_children(group)

    delete_widget_children(author_frame)
    delete_widget_children(category_frame)
    delete_widget_children(commit_frame)

    if changed_file in rule_index.keys():
        rule_list = rule_index[changed_file]
        max_results = max(10, len(rule_list))
        #Sort rules by frequency
        tuple_list = rule_list[0:max_results]
        rule_list.sort(key=operator.itemgetter(1),reverse=True)
        max_results = min(10, len(rule_list))
        #print(max_results)
        tuple_list = rule_list[0:max_results]
        if(len(tuple_list)>0):
            label_file = tkinter.Label(group, text = "File to be changed").grid(row=6,column=0,sticky=tkinter.W)
            label_supp = tkinter.Label(group, text = "Support").grid(row=6,column=1,sticky=tkinter.W)
            label_conf = tkinter.Label(group, text = "Confidence").grid(row=6,column=2,sticky=tkinter.W)

            count_row=6
        for rule_tuple in tuple_list:
            #print("Files ",rule_tuple[0]," may need to be changed and has frequency = ",rule_tuple[1])
            text_val = str(rule_tuple[0])
            support_val=str(rule_tuple[1])
            confidence_val=str(rule_tuple[2])
            count_row=1+count_row
            label1 = tkinter.Label(group, text = text_val).grid(row=count_row,column=0,sticky=tkinter.W)
            label2 = tkinter.Label(group, text = support_val).grid(row=count_row,column=1,sticky=tkinter.W)
            label3 = tkinter.Label(group, text = confidence_val).grid(row=count_row,column=2,sticky=tkinter.W)

    else:
        label3 = tkinter.Label(group, text = "This file has no previous version history OR is not frequent").grid(row=6,column=0,sticky=tkinter.W)


    for a in authors:
        label_auth = tkinter.Label(author_frame, text = a).grid()

    add_label = tkinter.Label(category_frame, text ="Addition count="+str(addition_count)).grid()
    del_label = tkinter.Label(category_frame, text ="Deletion count="+str(deletion_count)).grid()
    bug_label = tkinter.Label(category_frame, text ="BugFix count="+str(bugfix_count)).grid()


    for msg in commit_msgs:
        label_msg = tkinter.Label(commit_frame, text = msg).grid()

window = tkinter.Tk()
window.geometry('1000x1000')




window.title("File level analysis")

label= tkinter.Label(window, text = "Enter full changed file name :").grid(row=0,column=0, sticky=tkinter.W,columnspan=3,padx=20,pady=10)
input=tkinter.Entry(window,width = 45)
input.grid(row=1,column=0, sticky=tkinter.W,columnspan=3, padx=20,pady=10)

submit = tkinter.Button(window, text = "Find changed files",command = generateRecommendations).grid(row=2,column=0,sticky=tkinter.W,columnspan=3, padx=20,pady=20)

group = tkinter.LabelFrame(window, text="Recommendation Results", padx=10, pady=10)
group.grid(row=4,column=0,columnspan=3, rowspan=6,sticky=tkinter.W,padx=40,pady=40)

author_frame = tkinter.LabelFrame(window, text = "Top Authors who modified this file",padx=10,pady=10)
author_frame.grid(row=12,column=0,sticky=tkinter.W,columnspan=2, rowspan=4,padx=20)


category_frame = tkinter.LabelFrame(window, text = "Category wise commit count",padx=10,pady=10)
category_frame.grid(row=12,column=2,columnspan=2, rowspan=4,sticky=tkinter.W)


commit_frame = tkinter.LabelFrame(window, text = "Recent commit messages",padx=10,pady=10)
commit_frame.grid(row=22,column=0,columnspan=3, rowspan=4,sticky=tkinter.W,pady=40,padx=40)


#time.sleep(5)
window.mainloop()