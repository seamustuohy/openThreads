import csv
import openthreads
import couchdb

def importMe(file):
     dev = []
     with open(file, 'rU') as f:
          reader = csv.reader(f)
          for row in reader:
               dev.append(row)
     return dev

#genderDict == ['name', 'old gender', 'correct gender']

def checkGender(genderDict, server, db, listserv, lsname):
     a = openthreads.openThread(listserv, lsname)
     for i in genderDict:
          if i[2] != '':
               for m in a.msgProf:
                    if a.msgProf[m]['participantID'] == i[0]:
                         a.msgProf[m]['UpdatedGender'] = 'true'
                         a.msgProf[m]['gender'] = i[2]
               for x in a.profiles:
                    if a.profiles[x]['name'] == i[0]:
                         a.profiles[x]['UpdatedGender'] = 'true'
                         a.profiles[x]['gender'] = i[2]
     return a.msgProf, a.profiles

def checkGender2(genderDict, msgProf, profiles):
     for i in genderDict:
          if i[2] != '':
               for m in msgProf:
                    if msgProf[m]['participantID'] == i[0]:
                         print(msgProf[m]['participantID'])
                         msgProf[m]['UpdatedGender'] = 'true'
                         msgProf[m]['gender'] = i[2]
               for x in profiles:
                    if profiles[x]['name'] == i[0]:
                         print(profiles[x]['name'])
                         profiles[x]['UpdatedGender'] = 'true'
                         profiles[x]['gender'] = i[2]
     return msgProf, profiles


def upload():
     a.couchDB(server=server, port=None, database=db, data=a.profiles)
     a.couchDB(server=server, port=None, database=db, data=a.msgProf)

def couchDB(server=None, port=None, database=None, data=None):
        """This connects to an existing couchDB server and exports data to it. This function does not provide any other couchDB functionality. You have to do that all on your end. :) """
        #checking for if external server or if server is on localhost as well as for the port of the server is unique
        if server:
            if port:
                couch = couchdb.Server('http://'+server+':'+port)
            else:
                couch = couchdb.Server('http://'+server+':5984/')
        else:
            couch = couchdb.Server()
        # select database or set to default listServ database
        if database:
            db = couch[database]
        else:
            db = couch["listserv"]
        
        #This will check if you pass it a specifc data set and send either that, or the full messages dict to the database
        if data:
            db.save(data)
        else:
            db.save(self.messages)
        
