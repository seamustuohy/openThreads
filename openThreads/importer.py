import csv
import openthreads

def importMe(file):
     dev = []
     with open(file, 'rb') as f:
          reader = csv.reader(f)
          for row in reader:
               dev.append(row)
     return dev

#genderDict == ['name', 'old gender', 'correct gender']

def checkGender(genderDict, server, db, listserv, lsname):
     a = openthreads.openThread(listserv, lsname, 'false')
     for i in genderDict:
          if genderDict[i][2] != '':
               for n in a.messages:
                    if a.messages[n]['name'] == genderDict[i][0]:
                         a.messages[n]['gender'] = genderDict[i][2]
     a.threads = a.threader(a.messages)
     a.profiles = a.runProf()
     a.msgProf = a.runMsgs()
     a.threadProf = a.runThreads()
     for i in genderDict:
          if genderDict[i][2] != '':
               for m in a.msgProf:
                    if a.msgProf[m]['name'] == genderDict[i][0]:
                         a.msgProf[m]['UpdatedGender'] = 'true'
               for x in a.profiles:
                    if a.profiles[x]['name'] == genderDict[i][0]:
                         a.profiles[x]['UpdatedGender'] = 'true'
     a.couchDB(server=server, port=None, database=db, data=a.profiles)
     a.couchDB(server=server, port=None, database=db, data=a.msgProf)

