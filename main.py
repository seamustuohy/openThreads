import re
import time
import json
print("Main Parser Function loading")


class converter:
    def __init__(self):
        self.raw = ''
        self.messages = []

    def getArchive(self, textFile):
        """This function takes the location of the list-serv text file and opens it up for parsing
        """
        text = open(textFile)
        rawText = text.read()
        self.raw = rawText

    def defRegular(self, listserv):
        """This function takes the location of the list-serv text file and opens it up for parsing. Much later I may add the ability to just choose the html address of a list-serv archive. That will be straight up neato!
        """
        if self.raw == '':
            print("Please get a list serv archive and import it file first.")
        elif listserv == 'mailman':
            who = '\S*\sat\s\S*'
            headerFront = '\nFrom\s' + who + '\s*'
            capturedFront = '\nFrom\s(' + who + ')\s*'
            day = '[A-Z][a-z]{2}'
            month = day
            date = day + '\s' + month + '\s*?\d*?\s\S*?\s\d{4}\n'
            capTop = capturedFront + '(' + date + ')'
            dropTop = headerFront + date
#TODO - create captures for all header sections
#TODO - rewrite the following line to become a dictionary that parses the monthly log and create indiviudal dictionaries of all pertinant header info for each e-mail and includes the content.
            getHeader = '(.*?Message\-ID\:\s(.*?)\n)'
            fullHead = dropTop + getHeader
            splitText = re.split(dropTop, self.raw)
        else:
            print("please choose a list serve type to parse")
        for i in splitText:
            self.dictify(i)

    def dictify(self, email):
        """This function takes a raw text version of a list-serv archive and converts it into a parsable dictionary... possibly in JSON format. Yea, we will do JSON formatting because the internets love them some JSON
        """
        #get headers from email
        getHeader = '(.*?Message\-ID\:\s.*?\n)'
        msgDict = {}
        msg = re.findall(getHeader + '(.*)', email, flags=re.DOTALL)
        #create a dictionary item for body text
        for i in msg:
            msgDict['body'] = i[1]
        # Setting header specific regEx's
        whom = 'From\:\s(.*?)\n'
        date = 'Date\:\s(.*?)\n'
        dWrd = '[A-Z][a-z]{2}'
        subject = 'Subject\:\s(.*?)\n'
        inReply = 'In\-Reply\-To\:\s(.*?)\n'
        references = 'References\:\s(.*?)\nMessage\-ID\:'
        messageID = 'Message\-ID\:\s(.*?)\n'
        name = '\((.*)\)'
        #Tue, 8 Nov 2011 11:58:09 -0800 (PST)
        
       #create a dictionary item for the header items that are always there.
        whoCheck = re.findall(whom, email, flags=re.DOTALL)        
        if whoCheck:
            msgDict['From'] = self.checkReg(whoCheck)
            msgDict['Name'] = re.findall(name, self.checkReg(whoCheck))

        dateCheck = re.findall(date, email, flags=re.DOTALL)
        if dateCheck:
            msgDict['Date'] = self.checkReg(dateCheck)
            msgDict['compactDate'] = self.compactDate(dateCheck)
        subCheck = re.findall(subject, email, flags=re.DOTALL)
        
        if subCheck:
            msgDict['Subject'] = self.checkReg(subCheck)
        IDCheck = re.findall(messageID, email, flags=re.DOTALL)
        if IDCheck:
            msgDict['ID'] = self.checkReg(IDCheck)

        #create checks for items that may not be there.
        if re.search(references, email, flags=re.DOTALL) != 'none':
            msgDict['References'] = re.findall(references, email, flags=re.DOTALL)
        if re.search(inReply, email, flags=re.DOTALL) != 'none':
            msgDict['Reply'] = re.findall(inReply, email, flags=re.DOTALL)
       # print(msgDict['References'])
        if msgDict['References'] != []:
            msgDict['References'] = re.split('\s*|\n\t', msgDict['References'][0])

        #Body Parsing
        beginPGP = '\-{5}[A-Z]{5} [A-Z]{3} [A-Z]{9}\-{5}\n'
        endPGP = '\-{5}[A-Z]{3} [A-Z]{3} [A-Z]{9}\-{5}\n'
        PGP = beginPGP + '(.*?)' + endPGP
        scrubbed = '\-{14}\s[a-z]{4}\s[a-z]{4}\s\-{14}'
        grabScrubbed = scrubbed + '(.*)'
        replyName = 'On\s(.*?)wrote\:'
        test = re.findall(PGP, msgDict['body'], flags=re.DOTALL)

        #take all we have parsed in a message and append it to the main messages que
        self.messages.append(msgDict)

        #lets look at what we have appended.
        #print(self.messages[len(self.messages)-1]['From'])

        #its hard to make sure things are working right without time to inspect the output
        #time.sleep(1)
        
    def compactDate(self, dateCheck):
        second, minute, hour, day, month, year = 0,0,0,0,0,0
        dWrd = '[A-Z][a-z]{2}'
        compDateDict = ''+dWrd+',\s(\d*?)\s('+dWrd+')\s(\d{4})\s(\d{2})\:(\d{2})\:(\d{2})'
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        compactTup = re.findall(compDateDict, self.checkReg(dateCheck))
        for i in [i for i,x in enumerate(months) if x == compactTup[0][1]]:
            month = i
        day = compactTup[0][0]
        if len(day) == 1:
            day = str(0) + day
        year = compactTup[0][2]
        second = compactTup[0][5]
        minute = compactTup[0][4]
        hour = compactTup[0][3]
        compactDate = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)
        return(compactDate)

    def checkReg(self, item):
        if type(item) == list:
            return(item[0])
        else:
            return(item)
        
    def parseMessages(self, messageDict, flags):
        """ This function takes a message dictionary and parses it to elucidate understandings about it. This will most likely be a major function that calls a series of parsing functions that will return results to the function based upon what information it passes to them. This way I can call specialized data sets on this function from elsewhere 
        """
    def parseHeader(self, emailList):
        for i in emailList:
            header = emailList[i][2]
                
    def jsonMaker(self, command, fileName):
        if command == 'open':
            f = open('file.json', 'r');
            tmpMsg = f.read()
            self.messages = json.loads(tempMsg)
        elif command == 'save':
            f = open(fileName + '.json', 'w');
            f.write(json.dumps(self.messages));
            f.close()
        
    def firstPost(self):
        parsedFirst = {}
        exist = 0
        for i in self.messages:
            for x in parsedFirst:
                name = str(i['Name'])
                if i['Name'] == parsedFirst[x]['Name']:
                    exist = 1
                    if i['compactDate'] < parsedFirst[x]['compactDate']:
                        del(parsedFirst[x])
                        name = str(i['Name'])
                        parsedFirst[name] = i
            if exist != 1:
                name = str(i['Name'])
                parsedFirst[name] = i
            exist = 0
        return(parsedFirst)

    def initialResponse(self, ID):
        '''A function that takes a message ID and looks at what kind of response people receive on their first post. This collects the ammount of replies to an individuals first post on a listserv and returns the message id of all responses as well as the ammount of messages a individual user posts to a listserv after their first thread. '''

    #Grabs the identified message from the main message structure
    message = ''
    for i in self.messages:
        if i['ID'] = ID:
            message = i
    if message == '':
        return "no message found"
    
    #Gather replies and append them to the message structure
        replies = replies(message['ID'])
        repNum = 0
        for i in replies:
            repNum += 1
            message['replies'].append(i['ID'])
        message['repNum'] = repNum
            
    #gather the ammount of total messages a user has sent
        totalMessages = totalMessages(message['Name'])
        totalCount = 0
        for i in totalMessages:
            totalCount += 1
        message['totalMessages'] = totalCount

    #need to send this data somwhere
    

    def totalMessages(self, name):
        '''This function takes a users name and returns the ID's of all their messages on a mailing list.'''
        #need to write this
        
    def replies(self, ID):
        '''This function takes a message ID and returns a list of all the messages that replied to the identified message.''' 
        #need to write this

        
def runTest(b):
    #needs to mimic the below... it does not currently.
    #reload(main); a=main.converter(); a.getArchive('testtext'); a.defRegular('mailman'); a.firstPost()
    a = converter()
    a.getArchive(b)
    a.defRegular("mailman")
    a.firstPost()
