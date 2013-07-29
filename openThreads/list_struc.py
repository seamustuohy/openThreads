import re
import difflib

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
            logger.error("Duplace message ID detected in list-serv: "+i["Subject"])
        msg_dictionary[i['Message-ID']] = i
    return msg_dictionary

def add_to_index(message, index):
    """Takes a message and an existing index and returns an index with the message included. This function does not check to see if the message is already in the index. As such, if a duplicate message id exists it will overwrite that message.
    """
    logger.debug("adding message "+message['Message-ID']+" to index")
    index[message['Message-ID']] = message
    return index

def get_msg_data(message, index):
    msg_data = {}
    if message['Message-ID'] not in index.keys():
        index = add_to_index(message, index)
    msg_data['parsed_body'] = get_parsed_body(message, index)
    return msg_data

def split_body(message):
    """ split the body of a message into its component parts
    returns a dict with a section for PGP keys, if HTML exists, and content split by user.
    """
    parsed = {}
    body = message['Body']
    #Get PGP Keys if possible
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

def get_parsed_body(message, index):
    """Takes a message and an index of previously parsed messages and returns a dict with a section for PGP keys, if HTML exists, and content that includes the user name, original message,  length of section, section, and difference ratio between quoted text and referenced users email (1 = exact, 0 = completely different)"""
    parsed_body = split_body(message)
    #get comtent origins of replys in order "parsed_body['content']"
    if "References" in message.keys():
        references = message['References']
        #logger.debug(str(parsed_body))
        parsed_body = get_quote_body(parsed_body, references, index, message['Message-ID'])
    else:
        #put body in format created for reference text
        #magic number 1.0 == 100% match between text and user text
        parsed_body['content'][0] = ('user', message['Message-ID'], len(parsed_body['content'][0]),  parsed_body['content'][0], "1.0")
    return parsed_body

def get_quote_body(parsed_body, references, index, ID):
    #logger.debug("get_quote_body started")
    #logger.debug(str(parsed_body['content'][0]))
    for i in parsed_body['content']:
        #logger.debug(str(parsed_body['content'][0]))
        chunk_index = parsed_body['content'].index(i)
        #logger.debug(str(parsed_body['content'][0]))
        #if a quoted chunk
        if re.match(">", i):
            quote_origin = False
            ref_msg = False
            #print(i)
            plain = regular_expressions.un_quote(i)
            #print(plain)
            for ref in references:
                if ref in index.keys():
                    if plain in index[ref]['Body']:
                        quote_origin = index[ref]['Name']
                        ref_msg = index[ref]['Message-ID']
                    #checking for similarity in case there was any editing of the text in the quote itself.
                    #This was mostly added because some html email clients will edit out html links when they quote. This, by the way, sucks, and makes my life hard. So I don't like them. Not at all. I am using quick ratio because it is a nice in between from sloooooow ratio and sloopy real_quick_ratio
                    else:
                        ratio = difflib.SequenceMatcher(None, index[ref]['Body'], plain).quick_ratio()
                        if ratio  >= .80:
                            quote_origin = index[ref]['Name']
                            ref_msg = index[ref]['Message-ID']
            if quote_origin:
                if ratio:
                    parsed_body['content'][chunk_index] = (quote_origin, ref_msg, len(i), plain, ratio)
                    ratio = False
                    ref_msg = False
                else:
                    #magic number == 100% match between text and known reference
                    parsed_body['content'][chunk_index] = (quote_origin, ref_msg, len(i), plain, "1.0")
                    ref_msg = False
            else:
                logger.error("Quoted text not found")
                #magic number == 0% match between text and known references
                parsed_body['content'][chunk_index] = ("unknown", "unknown", len(i), plain, "0.0")
        else:
            print("YUP?")
            #magic number == 100% match between text and user text
            parsed_body['content'][chunk_index] = ('user', ID, len(i),  i, "1.0")
    return parsed_body

    #TODO Each of the following need to use parsed_body in get_msg_data to create a secondary structure that includes parsed body.
    ###Get length of text in response to each quote (if top or bottom post then length applies to all text in quoted messages)
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
    pass
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


