import unicodedata
class Commit:
   'Shows details like author name, commit message and modified files'
   commit_count=0

   def __init__(self, id, author,commit_message,changed_file,timestamp):
      m=unicodedata.normalize('NFKD', commit_message).encode('ascii','ignore')
      self.id = id
      self.author = author
      self.commit_message=m
      self.changed_file=[]
      self.changed_file = changed_file
      self.timestamp = timestamp
      Commit.commit_count += 1

   def displayCount(self):
     print "Total Number of commits %d" % Commit.commit_count

   def displayCommits(self):
      print "Id : ", self.id,  ", Message: ", self.commit_message

   def displayFileNames(self):
       print self.changed_file

   def getMessage(self):
       return self.commit_message