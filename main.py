import re
print("Main Parser Function Reloaded")

def print5():
    print('five')
    
class converter:
    def __init__(self):
        self.raw = ''

    def getArchive(self, textFile):
        """This function takes the location of the list-serv text file and opens it up for parsing
        """
        text = open(textFile)
        rawText = text.read()
        self.raw = rawText
    

    def printMessage(self):
    	""" This function parses an archive and prints out the results of a generic regular expression. For testing purposes only. Will be converted into a generic dictionary generator that parses the text-file.
        """ 
        if self.raw == '':
            print("Please get a list serv archive and import it file first.")
        who = '\S*\sat\s\S*'
        headerFront = '\nFrom\s' + who + '\s*'
        capturedFront = '\nFrom\s(' + who + ')\s*'
        day = '[A-Z][a-z]{2}'
        month = day
        date = day + '\s' + month + '\s*?\d*?\s\S*?\s\d{4}\n'
        capHeader = capturedFront + '(' + date + ')'
        dropHeader = headerFront + date
#TODO - create captures for all header sections
#TODO - rewrite the following line to become a dictionary that parses the monthly log and create indiviudal dictionaries of all pertinant header info for each e-mail and includes the content.
        messageDict = re.findall(capHeader, self.raw, flags=re.DOTALL)
        print messageDict

  
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
                    
