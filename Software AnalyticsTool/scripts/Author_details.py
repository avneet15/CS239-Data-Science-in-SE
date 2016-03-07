
import git.objects.util as git_obj
import unicodedata


class Author_Det:

    def __init__(self, name):
       n=unicodedata.normalize('NFKD', name.name).encode('ascii','ignore')
       #print type(n)
       self.name = name
       self.authorName = n
       self.commit_message= []
       self.timestamp= []
       self.count = 0

    #commit_message,count,timestamp

    def addCommitDetails(self,commit_message,timestamp ):
        self.commit_message.append(commit_message)
        self.timestamp.append(timestamp)
        self.count=self.count +1

    def getCount(self):
        return self.count

    def getMessages(self):
        for i in range(len(self.commit_message)):
            print self.commit_message[i]

    def getName(self):
        return self.authorName