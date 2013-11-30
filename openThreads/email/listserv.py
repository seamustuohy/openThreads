import re
import difflib
import random
import string
import openThreads

from openThreads import logger
from . import util
from . import regular_expressions
#===TERMS===:
##Thread Root: The first message in a thread. 
##?????? :The number of back-and-forth interactions past the initial reply. a(0)<-b(0)<-a(1)<-b(2)

def get_it(message, ls):
    """TODO: Using this function to allow me to grab data currently. Will need to be replaced with a more logical function set later.
    :param message:
    :param ls: plain text dump from a listserv
    """
            #Grab plain-test listserv
    if util.is_file("compiled_lists/"+ls):
        data = util.open_listserv("compiled_lists/"+ls)

class list():
    def __init__(self, listserv=None, message_index=None, thread_index=None, users_index=None):
        """
        :param listserv: a listserv object that has been built from the archive_reader.
                
        """
        if listserv != None:
            self.listserv = listserv
        if message_index == None:
            #if not passed an index, but passed a list-serv create an index
            self.messages = {}
        #always take the listserv and check it against the index. If there is an index already then suppress warning, if not, then log all warnings.
        else:
            self.messages = message_index
        self.create_message_index(self.listserv)
        self.threads = {}
        self.users = {}

    class message():
        """The basic unit of storage for message analysis"""
        def __init__(self):
            pass

    class User():
        """The basic unit for email thread users."""
        def __init__(self):
            pass
        
    def get_uid(self, typeof):
        """
        Unique thread ID creator.
        :param typeof: The name of the dictionary the uid will be used in to ensure uniqueness
        :type typeof: string
        :returns: unique thread identifier
        :return type: string
        """
        uid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(42))
        #lets make sure we don't think pseudo-random == unique and check before overwriting a thread
        while uid in getattr(self, typeof).keys():
            uid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(42))
        return uid
    
    
    def create_thread(self, message):
        """
        Creates a new thread and adds it to the threads dict.
        :param message: A parsed message that creates a thread
        :returns: New Threads unique ID
        """
        utid = self.get_uid("threads")
        #create thread and add to threads
        self.threads[utid] = self.thread(utid)
        #try to add a message to the thread
        if self.threads[utid].add_root(message.Subject, message.ID, message.Name) == True:
            return utid
        else:
            #If we can't successfully create the thread we should delete it. 
            del(self.threads[utid])
            return False

    def get_thread(self, message):
        """Returns the ID of the message's thread if  one exists. Creates a thread and returns the thread ID if one does not already exist.
        @param message Message ID
        """
        if "Reply_To" in message.keys():
            root = self.find_msg_root(message)
            if root not in self.threads.keys():
                self.create_thread(self.messages[root])
            else:
                logger.warn("Thread already exists")
            self.add_message(root, message)
            return root
        else:
            self.create_thread(message)
            return message['ID']

    def find_msg_root(self, message):
        parent = getattr(message, "Reply_To", None)
        if parent != None:
            return self.find_msg_root(self.messages[parent])
        else:
            return message['ID']
        
    def add_message(self, thread, message):
        """Identifies where a message should be in a tree and adds the message to the tree accordingly.
        @return True/False True returned if node added. False if node not added
        """
        if "Reply_To" in message.keys():
            parent = message['Reply_To']
            if self.threads[thread].contains(parent):
                self.threads[thread].add_node(message['Subject'], message['ID'], parent, message['Name'])
            else:
                self.add_message(thread, self.messages[parent])
        else:
            return
          
    class msg(Node):
        def add_user(user):
            """Add a user ID to a message"""
            self.user = user

    def get_msg_data(self, message):
        """
        Adds a new message to an existing message struct
        TODO Add all msg_data functions to this controller function
        """
        if message['ID'] not in self.messages:
            self.messages[message['ID']] = self.message()
            for i in message:
                setattr(self.messages[message['ID']], i, message[i])
        #The set of functions that are used to parse message context out.
        parsed_body = self.get_parsed_body(message)
        #TODO START CODING HERE!!!!!!!!!!
        thread_ID = self.get_thread(message)
        user = self.get_user(message)
        self.get_reply_length(message)
        #After get_thread is called you only need to pass the ID of the message to thread calls, not the whole message
        ID = message['ID']
        #need to define the structure for user activity
        historic_user_activity = self.threads[thread].get_user_thread_history(ID)
        location = self.threads[thread].get_location(ID)
        direct_replies = self.threads[thread].get_children(ID)
        decendants = self.threads[thread].get_descendants(ID)
        siblings = self.threads[thread].get_siblings(ID)
        response_time = self.threads[thread].get_response_time(ID)
        user_response_time = self.threads[thread].get_user_response_time(ID)
        self.threads[thread].get_interaction_level(ID)
        quoted = get_quoted_text(message)
        get_gender(message)
        
        ###Get length of text in response to each quote (if top or bottom post then length applies to all text in quoted messages)
        #Go to the user lists and find the most accurate user. This needs to take all messages into account to try and break apart users with the same name, but whom are different, as well as the same user with various names listed in the header info. This is going to be hard-ish 
        get_user(message)
        
    def get_reply_length():
        pass
        get_thread_root(message)
        get_thread_tree(message, root)
        ##check if user exists in thread before this message
        get_user_thread_history(message, tree)
        ##Check number of thread splits before & after this message
        get_message_node_location(message, tree)
        ##Check number of replies directly to this message
        get_direct_replies(message, tree)
        ##check number of refrences spawned by message
        get_descendants(message, tree)
        ##check number of emails reply-to this messages parent
        get_siblings(message, tree)
        ##Check time between this message and all responses (will need a relitive time for users of those messages as well once users are run.)
        get_response_time(message, tree)
        #TODO create a structure for tagging user nodes with info that they need to update once all there messages have been updated, or are updated in the future. That way old data will be contantly updated to show things such as if the message was replied to in their usual message response period for that list.
        ##check time between this message and parent as well as user relitive time, once user is fully computed
        get_user_response_time(message, tree)
        ##see if anyone quoted replies, and if they quote message (this is another area where it will have to see if all messages on the tree have been run, and if they have it will ping them for quoted text. If they have not yet run it will mark as a task to run once those are completed and have them run once they have finished.)
        get_quoted_text(message, tree)
            ##length of message
            ##deviation +/- of length from average length of messages by user of similar type
            ##Salutation vs. salutationless
            ##signed message (can use signatures across messages to identify unique individuals who are on multiple listservs)
            ##check is parent replies (the n ext function here shoudl be under quoted reply but err for sudo code stuffs)
        get_parent_response(message, tree)
        #Check gender of sender against multiple data sets
        get_gender(message)
        #number of interactions with users in this thread and distance from message sender (quoted = 1 [if quoted without other replies that are closer in distance to the user], reply-to=1, other=message     distance from user)
        get_thread_interaction_levels(message, thread)
        #check number of replies to threads started by thread root message sender
        #deviation +/- of time posted from normal message posting times
        #if in proper message format see if there is a cc'ed line and see if they responded in the thread
        #What key terms are contained in the quoted text that are also in an indiduals response.
        #

        
        
        for i in parsed_body:
            setattr(self.messages[message['ID']], i, parsed_body[i])

            
    def create_message_index(self, listserv):
        """create a dictionary of each message indexed by message ID
        @param listserv SEE: class "list"'s param listserv
        @return msg_dictionary a dict of messages indexed by message ID
        """
        if self.messages != {}:
            existing_index = True
        msg_dictionary = {}
        for message in listserv:
            if message['ID'] not in self.messages:
                self.messages[message['ID']] = self.message()
                for i in message:
                    setattr(self.messages[message['ID']], i, message[i])
            else:
                if existing_index == True:
                    logger.debug("Duplace message ID detected in list-serv: "+message['ID']+" found with subject "+message["Subject"])
                else:
                    logger.warn("Duplace message ID detected in list-serv: "+message['ID']+" found with subject "+message["Subject"])

    
    def split_body(self, message):
        """ split the body of a message into its component parts
        returns a dict with a section for PGP keys, if HTML exists, and raw content.
        @param message SEE: class "list"'s param message
        """
        parsed = {}
        body = message['Body']
        #Get PGP Keys if possible
        pgp, body = regular_expressions.PGP(body, True)
        if pgp != False and pgp != []:
            parsed['PGP'] = pgp[0]
        #See's if the user uses an html client
        #TODO Make this compatable with non plain-text listservs
        scrub, body = regular_expressions.scrubbed(body, True)
        if scrub:
            parsed['HTML'] = True
        #Gather seperated chunks of the message
        parsed['content'] = regular_expressions.message_components(body)
        if body != message['Body']:
            parsed['clean_body'] = body
        return parsed
        
    def get_parsed_body(self, message):
        """Takes a message and and returns a dict with a section for PGP keys, if HTML exists, and content that includes the user name, original message, length of section, section, and difference ratio between quoted text and referenced users email (1 = exact, 0 = completely different)

        @param message
        @return

        @return message componenets = (USER NAME, MESSAGE ID, LENGTH, SECTION TEXT, PERCENT OF MATCH)
        """
        parsed_body = self.split_body(message)
        #get comtent origins of replys in order "parsed_body['content']"
        if "References" in message.keys():
            references = message['References']
            #logger.debug(str(parsed_body))
            parsed_body = self.get_quote_body(parsed_body, references, message['ID'])
        else:
            #put body in format created for reference text
            #magic number 1.0 == 100% match between text and user text
            parsed_body['content'][0] = ('user', message['ID'],     len(parsed_body['content'][0]),  parsed_body['content'][0], "1.0")
        return parsed_body
    
    def get_quote_body(self, parsed_body, references, ID):
        """
        @return parsed_body['content'] componenets = (USER NAME, MESSAGE ID, LENGTH, SECTION TEXT, PERCENT OF MATCH)
        """
        #acceptable ratio of deviance for a modified quote to be attributed to an origin (.80 is a good fit found from test data that had html links scraped out)
        diff_ratio = .80
        for i in parsed_body['content']:
            #logger.debug(str(parsed_body['content'][0]))
            chunk_index = parsed_body['content'].index(i)
            #logger.debug(str(parsed_body['content'][0]))
            #if a quoted chunk
            if re.match(">", i):
                plain = regular_expressions.un_quote(i)
                quote_origin, ref_msg, ratio = self.get_quote_origin(plain, references, diff_ratio)
                if quote_origin != False:
                    if ratio >= diff_ratio:
                        parsed_body['content'][chunk_index] = (quote_origin, ref_msg, len(i), plain, ratio)
                        ratio = False
                        ref_msg = False
                    else:
                        logger.error(str(ratio))
                        logger.error("This is bad... You should never get here. Somehow you have been passed an quote origin as well as a ratio that is too small. No one will ever see this message. But, if you do... well, I blame you.")
                        pass
                else:
                    logger.error("Quoted text not found")
                    #magic number == 0% match between text and known references
                    parsed_body['content'][chunk_index] = ("unknown", "unknown", len(i), plain, "0.0")
            else:
                #magic number == 100% match between text and user text
                parsed_body['content'][chunk_index] = ('user', ID, len(i),  i, "1.0")
        return parsed_body

    def get_quote_origin(self, plain, references, diff_ratio):
        quote_origin = False
        ref_msg = False
        ratio = 0
        for ref in references:
            if ref in self.messages.keys():
                        #print(self.index[ref]['Name'], ref)
                if plain in self.messages[ref].Body and ">"+plain not in self.messages[ref].Body:
                    quote_origin = self.messages[ref].Name
                    ref_msg = self.messages[ref].ID
                    ratio = 1
                    return quote_origin, ref_msg, ratio
                else:
                    ratio = difflib.SequenceMatcher(None, self.messages[ref].Body, plain).quick_ratio()
                    if ratio  >= diff_ratio:
                        quote_origin = self.messages[ref].Name
                        ref_msg = self.messages[ref].ID
                        return quote_origin, ref_msg, ratio
        return quote_origin, ref_msg, ratio


        #TODO Each of the following need to use parsed_body in get_msg_data to create a secondary structure that includes parsed body.

    def get_reply_length():
        pass
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
        #number of interactions with users in this thread and distance from message sender (quoted = 1 [if quoted without other replies that are closer in distance to the user], reply-to=1, other=message     distance from user)
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
    
