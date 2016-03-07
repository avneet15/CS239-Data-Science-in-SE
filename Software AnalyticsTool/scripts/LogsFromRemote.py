import sys
import os.path
import git
import argparse
from Commit import Commit
import subprocess
import time
from Author_details import Author_Det
import unicodedata

url = "/home/ms/Desktop/239CS/jline2/.git"

def main(args):

    file = open("Transactions.txt", "w")
    # if we wish to append to existing file change w to a for all files
    # file =open(<filename>,"a")

    repo=git.Repo(os.path.dirname(url),search_parent_directories=True)
    commits = list(repo.iter_commits('master'))

    file_bugs =open("TransactionsRelatedToBugFixes.txt","w")


    #commit_objects = [] #no need for now
    file_dict={}
    file_support_dict={}
    commit_messages_per_file={}
    c1 = None
    prev_changed_files = []
    consecutive_transactions_combined_count=0
    max_consecutive_transactions_combined_count=0
    print "Total Number of Commits: ",len(commits)

    file2=open("TransactionWithoutCombining.txt","w")
    write_individual_transactions(file2,commits)
    file2.close()

    print "Transaction with Combining similar transactions"

    for com in range(len(commits)-1):

        changed_files = []
        prev=c1
        timestamp = time.mktime(time.gmtime(commits[com].committed_date))

        #get changed files between 2 consecutive commits
        getChangedFiles(changed_files, com, commits)

        #store commit object in list commit_objects
        #eliminate changed_files which are empty
        if(len(changed_files)>0):
            c1 = Commit(com+1,commits[com].author,commits[com].message,changed_files,timestamp)

            if("fix" in c1.commit_message.lower() or "issue" in c1.commit_message.lower() or "patch" in c1.commit_message.lower() or "bug" in c1.commit_message.lower() or "avoid" in c1.commit_message.lower() or "handle" in c1.commit_message.lower()):
                file_bugs.write(','.join(changed_files))
                file_bugs.write("\n")


            #Add file and author to dictionary
            for i in range(len(changed_files)):
                author_object = file_dict.has_key(changed_files[i])
                if author_object==True:
                    author_object = file_dict.get(changed_files[i])
                    found_author=False
                    #print "Entered for file ",changed_files[i]
                    for x in range(len(author_object)):
                        author=author_object[x]
                        if (author.name == commits[com].author):
                            author.addCommitDetails(commits[com].message,timestamp)
                            found_author=True


                    if(found_author==False):
                        #add a new author to list
                        author= Author_Det(commits[com].author)
                        author.addCommitDetails(commits[com].message,timestamp)
                        author_object.append(author)
                        file_dict[changed_files[i]]= author_object

                else:
                    author_object=[]
                    author= Author_Det(commits[com].author)
                    author.addCommitDetails(commits[com].message,timestamp)
                    author_object.append(author)
                    file_dict[changed_files[i]]= author_object



            #Combining transactions which are by same author and have same commit message
            max_consecutive_transactions_combined_count, prev_changed_files,consecutive_transactions_combined_count = combineTransactionsSuper(c1,changed_files,consecutive_transactions_combined_count,file,max_consecutive_transactions_combined_count,prev,prev_changed_files)

            #Get support of each
            #Getting stats related to commit Messages
            #commit_messages_per_file
            for f in range(len(changed_files)):
                commit_message_list=[]
                if commit_messages_per_file.has_key(changed_files[f]):
                    #print "File already present. Add commit message to it"
                    commit_message_list=commit_messages_per_file.get(changed_files[f])
                commit_message_list.append(c1.commit_message)
                commit_messages_per_file[changed_files[f]]=commit_message_list
                support = 0
                if file_support_dict.has_key(changed_files[f]):
                    support=file_support_dict.get(changed_files[f])
                file_support_dict[changed_files[f]]=support+1


        #statistics like
        '''
        count_modified_files = len(repo.index.diff(None))
        count_staged_files = len(repo.index.diff("HEAD"))
        '''

    writePreviousCommitsToFile(file, None, prev_changed_files)
    file.close()
    file_bugs.close()

    #Write all commit messages to file
    file = open("Support.txt", "w")
    keys= file_support_dict.keys()
    for m in xrange(len(keys)):
        k = file_support_dict.get(keys[m])
        str_to_write=keys[m]+","+str(k)+"\n"
        file.write(str_to_write)
    file.close()


    print "*******************************"
    print "STATISTICS"
    print "\n--------------------------------\n"
    print "Maximum Number of transactions Combined: ",max_consecutive_transactions_combined_count
    print "Transaction are saved to a file"


    #printing top 3 authors for a file
    print "\n--------------------------------\n"
    file = open("GetTopAuthors.txt", "w")
    key_list=file_dict.keys()
    print "Finding top authors for files. Count=",len(key_list)
    getTopCommitAuthorsForFile(file, file_dict, key_list)
    file.close()
    print "Top authors are saved to a file"

    # getting various stats related to commit messages
    print "\n--------------------------------\n"
    file = open("GetCommitsCategories.txt", "w")
    file_top_5 = open("GetRecent5Commits.txt", "w")
    key_list=commit_messages_per_file.keys()
    print "Analysis on commit messages per file. Count=",len(key_list)
    getCommitCategoriesForFile(file, commit_messages_per_file, key_list,file_top_5)
    file.close()
    file_top_5.close()
    print "Stats are saved to a file"


def getCommitCategoriesForFile(file, messages_dict, key_list,file_top_5):
    global_add_count=0
    global_remove_count=0
    global_fix_count=0
    for i in range(len(key_list)):
        item = messages_dict.get(key_list[i])
        messages_list = item
        #categories :
        #1 . Add/ update
        #2. Remove/Delete
        #3. Fix/Issue/patch
        #4. Other
        add_count=0
        remove_count=0
        fix_count=0
        for m in range(len(messages_list)):
            if "add" in messages_list[m].lower() or "update" in messages_list[m].lower():
                add_count=add_count+1
                global_add_count+=1
            elif "remove" in messages_list[m].lower() or "delete"  in messages_list[m].lower():
                remove_count+=1
                global_remove_count+=1
            elif "fix" in messages_list[m].lower() or "issue" in messages_list[m].lower() or "patch" in messages_list[m].lower() or "bug" in messages_list[m].lower() or "avoid" in messages_list[m].lower() or "handle" in messages_list[m].lower():
                fix_count+=1
                global_fix_count+=1

        write_string= key_list[i]+","+str(add_count)+","+str(remove_count)+","+str(fix_count)+"\n"
        file.write(write_string)

        #Recent 5 Commit Messages
        top5 =0
        for x in range(len(messages_list)):
            top5+=1
            write_string = key_list[i]+","
            file_top_5.write(write_string)
            mess  = (messages_list[x][:75] + '..') if len(messages_list[x]) > 75 else messages_list[x]
            mess=mess.replace(","," ")
            file_top_5.write("".join( mess.splitlines()))
            file_top_5.write("\n")
            if top5>=5:
                break

    print "Statistics based on Commit Messages: "
    print "Total Commits related to code addition/modification: ",global_add_count
    print "Total Commits related to code deletion: ",global_remove_count
    print "Total Commits related to bug fix: ",global_fix_count




def getTopCommitAuthorsForFile(file, file_dict, key_list):
    for i in range(len(key_list)):
        item = file_dict.get(key_list[i])
        authors_list = item
        name = []
        count = []
        for x in range(len(authors_list)):
            name.append(authors_list[x].getName())
            count.append(authors_list[x].getCount())
        name = [x for (y, x) in sorted(zip(count, name))]
        count.sort()
        count.reverse()
        name.reverse()
        name_count = 0
        for n in range(len(name)):
            name_count = name_count + 1
            string_to_write = str(key_list[i]) + "," + name[n] + "," + str(count[n]) + "\n"
            file.write(string_to_write)

            if (name_count >= 3):
                break


def combineTransactionsSuper(c1, changed_files, consecutive_transactions_combined_count, file,
                             max_consecutive_transactions_combined_count, prev, prev_changed_files):
    # comparing prev and current commit to see if its part of same transaction
    # we subtract prev from current timestamp since the commit history is from latest to previous.
    if (prev is not None and prev.author == c1.author and (prev.commit_message == c1.commit_message) and (
        prev.timestamp - c1.timestamp) < 200):
        print "*******************************"
        consecutive_transactions_combined_count = consecutive_transactions_combined_count + 1
        if max_consecutive_transactions_combined_count < consecutive_transactions_combined_count:
            max_consecutive_transactions_combined_count = consecutive_transactions_combined_count
        isPartOfMultipleConsecutiveTransactions(consecutive_transactions_combined_count)
        prev_changed_files = combineTransactions(prev_changed_files, changed_files, prev)

    elif (prev is not None and (prev.author != c1.author or prev.commit_message != c1.commit_message or (
        prev.timestamp - c1.timestamp) > 200)):
        consecutive_transactions_combined_count = 0
        writePreviousCommitsToFile(file, prev, prev_changed_files)
        prev_changed_files = changed_files
    else:
        consecutive_transactions_combined_count = 0
        writePreviousCommitsToFile(file, None, prev_changed_files)
        prev_changed_files = changed_files

    return max_consecutive_transactions_combined_count, prev_changed_files,consecutive_transactions_combined_count


def getChangedFiles(changed_files, com, commits):
    for x in commits[com].diff(commits[com + 1]):  # we get difference between 2 consecutive commits
        # a_blob is from earlier file and b_blob is from latest file
        if x.a_blob is not None and x.a_blob.path not in changed_files:
            changed_files.append(x.a_blob.path)

        if x.b_blob is not None and x.b_blob.path not in changed_files:
            changed_files.append(x.b_blob.path)


def writePreviousCommitsToFile(file, prev, prev_changed_files):
    if len(prev_changed_files) > 0:
        file.write(','.join(prev_changed_files))
        file.write("\n")

    elif prev is not None:
        file.write(','.join(prev.changed_file))
        file.write("\n")


def isPartOfMultipleConsecutiveTransactions(consecutive_transactions_combined_count):
    if consecutive_transactions_combined_count == 1:
        print "Combining a new set of consecutive transaction. Count=1"
    else:
        print "Number of consecutive transactions combined (in progress) : Count=", consecutive_transactions_combined_count


def combineTransactions(prev_changed_files,changed_files,prev):
    if (len(prev_changed_files)==0):
        print "Changed Files in previous commit: ",prev.changed_file
        print "Changed Files in current commit: ",changed_files
        for i in range(len(prev.changed_file)):
            if prev.changed_file[i] not in changed_files:
                changed_files.append(prev.changed_file[i])
        print changed_files
        prev_changed_files = changed_files #this is done to combine multiple transactions
    else:
        #multiple transaction
        #combine them together
        print "Changed Files in previously combined transactions: ",prev_changed_files
        print "Changed Files in current commit: ",changed_files
        for i in range(len(changed_files)):
            if changed_files[i] not in prev_changed_files:
                prev_changed_files.append(changed_files[i])

    return prev_changed_files

def write_individual_transactions(file,commits):
    for com in range(len(commits)-1):

            changed_files = []
            timestamp = time.mktime(time.gmtime(commits[com].committed_date))

            #get changed files between 2 consecutive commits
            getChangedFiles(changed_files, com, commits)

            if len(changed_files) > 0:
                file.write(','.join(changed_files))
                file.write("\n")

if __name__ == '__main__':
    main(url)
    sys.exit(0)