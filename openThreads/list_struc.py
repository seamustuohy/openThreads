import re

from . import logger
from . import util
from . import regular_expressions
#===TERMS===:
##Thread Root: The first message in a thread. 
##?????? :The number of back-and-forth interactions past the initial reply. a(0)<-b(0)<-a(1)<-b(2)


def main(message, ls):
    """Using this function to allow me to grab data currently. Will need to be replaced with a more logical function set later. """
    #Grab plain-test listserv
    if util.is_file("compiled_lists/"+ls):
        listserv = util.open_listserv("compiled_lists/"+ls)

def make_index(listserv):
    #create a dictionary of each message indexed by keys
    msg_dictionary = {}
    for i in listserv:
        if i['Message-ID'] in msg_dictionary.keys():
            logger.error("Duplace message ID detected in list-serv")
        msg_dictionary[i['Message-ID']] = i
    return msg_dictionary

def add_to_index(message, index):
    """Takes a message and an existing index and returns an index with the message included. This function does not check to see if the message is already in the index. As such, if a duplicate message id exists it will overwrite that message.
    """
    logger.debug("adding message "+message['Message-ID']+" to index")
    index[message['Message-ID']] = message
    return index

def parse_body(message):
    parsed = {}
    body = message['Body']
    #Get possible PGP Keys
    pgp = regular_expressions.PGP(body)
    if pgp == []:
        parsed['pgp'] = pgp[0]
    #See's if the user uses an html client
    #TODO Make this compatable with non plain-text listservs
    if regular_expressions.scrubbed(body):
        parsed['HTML'] = True
    #Gather seperated chunks of the message
    parsed['content'] = regular_expressions.message_components(body)
    return parsed

def get_msg_data(message, index):
    if message['Message-ID'] not in index.keys():
        index = add_to_index(message, index)
    parsed_body = parse_body(message)
    #get comtent origins of replys in order "parsed_body['content']"
    references = message['References']
    for i in parsed_body['content']:
        chunk_index = parsed_body['content'].index(i)
        #if a quoted chunk
        if re.match(">", i):
            find_quote_origin(i, references, index)
            plain = regular_expressions.un_quote(i)
            for ref in references:
                if plain in index[ref]['Body']:
                    quote_origin = ref
            if quote_origin:
                parsed_body['content'](chunk_index) = (quote_origin, plain)
            else:
                logger.error("Quoted text NOT found in referenced messages")
                parsed_body['content'](chunk_index) = ("UNKNOWN", plain)
        else:
            parsed_body['content'](chunk_index) = ('user', i)
    ###Get length of text in response to each quote (if top or bottom post then length applies to all text in quoted messages)
    #### TODO check for sections that ALWAYS exist in the current parser. Like, list-serv automatic text and the like.
            
    ##check if user exists in thread before this message
    ##Check number of thread splits before & after this message
    ##Check number of replies directly to this message
    ##check number of refrences spawned by message
    ##check number of emails reply-to this messages parent
    ##Check time between this message and all responses
    ##check time between this message and parent
    ##see if anyone quoted replies, and if they quote message
    ##check is parent replies
    ##length of message
    ##deviation +/- of length from average length of messages by user of similar type
    ##Salutation vs. salutationless
    ##signed message (can use signatures across messages to identify unique individuals who are on multiple listservs)
    #Check gender of sender against multiple data sets
    #number of interactions with users in this thread and distance from message sender (quoted = 1 [if quoted without other replies that are closer in distance to the user], reply-to=1, other=message distance from user)
    #check number of replies to threads started by thread root message sender
    #deviation +/- of time posted from normal message posting times
    #if in proper message format see if there is a cc'ed line and see if they responded in the thread
    #What key terms are contained in the quoted text that are also in an indiduals response.
    #

def get_user_data():
    #is the user on multiple list-servs
    #is the user interacting with the same people across list-servs
    #what are the strongest relationships a user has
    #what is the likelyhood a user is going to reply to a person they don't know than a person they do know.
    #What topics does this user most often post on
    #What users does this user most often reply to
    #what users root messages is this user most likely to comment on
    #what thread types (common quoted words and suject lines) is this user most likly to take part in
    #the ratio of initiated threads to replies
    #the number of replies
    #the number of root messages
    #average number of responses per message
    #average back-and-forth interaction length
    #number of back-and-forths
    #per-thread number of back-and-forths
    #messages per thread
    #total number of threads
    #percentage of threads replied to since first post
    #usual time's messages are sent
    
    
    
"""
Data Structure
'Body': "HERE BE BODY TEXT"
'day_number': '3'
'Name': 'SomeCoder'
'time': '12:11:02'
'seconds': '02'
'minute': '11'
'hour': '12'
'day_name': 'Wed'
'month_name': 'Jul'
'year': '2013'
'zone': '-0700'
'Address': 'somecoder@hersite.com'
'References': [
, '<SNT401-EAS37804FSED01FE4564955F91A0720@pfdshsx.gbl>',
,'<51D29F32.2023335@wfesnd.nl>',
'<51D3074E.1060200@nfet.inger.tum.de>',
'<CAJVRA1QnCK_df5NfT9rUYNeD3Tq4vP-1PgiVYuEwVRaZj2+A@mail.gmail.com>',
'<CACJAJ5-_Kg2ai+Uhz6CjF2ESA4u13w6nOP_b+j9YjvXNfVqGoRuw@mail.gmail.com>'
]
'referenced_reply_text':
(quote, user, message)
'In-Reply-To':('<CACJAJ5-_Kg2ai+Uh9ZzBz6Cju1fdsf34FDP_b+j9YjvXNfVqGoRuw@mail.gmail.com>',
name,
profile type,
time between,
quoted?,
)
'Message-ID': '<CAJVRA1Qu6QD-=ZPTo0vL6zLP+SbJO8S9SRk7RA=uWnHuaF02Nuw@mail.gmail.com>'
'Subject': '[The List] Why we hate the world'}




"""    





class listServ(name):
    def __init__():
        
