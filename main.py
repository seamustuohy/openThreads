import re
import time
print("Main Parser Function Reloaded")

def print5():
    print('five')
    
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
    

    def printMessage(self):
        """This function takes the location of the list-serv text file and opens it up for parsing. Much later I may add the ability to just choose the html address of a list-serv archive. That will be straight up neato!
        """
        if self.raw == '':
            print("Please get a list serv archive and import it file first.")
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
        for i in splitText:
            self.dictify(i)

    def dictify(self, email):
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
        subject = 'Subject\:\s(.*?)\n'
        inReply = 'In\-Reply\-To\:\s(.*?)\n'
        references = 'References\:\s(.*?)\nMessage\-ID\:'
        messageID = 'Message\-ID\:\s(.*?)\n'

        #create a dictionary item for the header items that are always there.
        msgDict['From'] = re.findall(whom, email, flags=re.DOTALL)
        msgDict['Date'] = re.findall(date, email, flags=re.DOTALL)
        msgDict['Subject'] = re.findall(subject, email, flags=re.DOTALL)
        msgDict['ID'] = re.findall(messageID, email, flags=re.DOTALL)

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
        print(self.messages[len(self.messages)-1]['From'])

        #its hard to make sure things are working right without time to inspect the output
        time.sleep(1)
        
    def getMessages(self):
        """This function takes a raw text version of a list-serv archive and converts it into a parsable dictionary... possibly in JSON format. Yea, we will do JSON formatting because the internets love them some JSON
        """
        who = '\S*\sat\s\S*'
        headerFront = '^From\s' + who + '\s*'
        capturedFront = '^From\s(' + who + ')\s*'
        day = '[A-Z][a-z]{2}'
        month = day
        date = day + '\s' + month + '\s{2}\d*\s\S*?\d{4}$'
        capHeader = capturedFront + '(' + date + ')'
        dropHeader = headerFront + date
    #TODO - create captures for all header sections
    #TODO - rewrite the following line to become a dictionary that parses the monthly log and create indiviudal dictionaries of all pertinant header info for each e-mail and includes the content.
        messageDict = re.findall(capHeader + '(.*?)' + dropHeader, self.raw, flags=re.DOTALL)
        return messageDict
    
    def parseMessages(self, messageDict, flags):
        """ This function takes a message dictionary and parses it to elucidate understandings about it. This will most likely be a major function that calls a series of parsing functions that will return results to the function based upon what information it passes to them. This way I can call specialized data sets on this function from elsewhere 
        """
        def parseHeader(emailList):
            for i in emailList:
                header = emailList[i][2]
                
