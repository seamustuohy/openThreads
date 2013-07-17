import email_io
from archive_reader import message_parser
import threader
import profiles

def main(listserv_identifier):
    """The controlling function that parses a list-serv"""
    #1 check to see what is being passed (message, listserv, html, etc)
    listserv = email_io(listserv_file)
    #1.5 load up any corresponding message database if a single message being added to the database
    #2 parse the messages into message object
    #3 if messages referenced by a parsed message are missing create a temporary blank message to show that the message is missing, this will also allow us to intuit personal messages sent that don't make it to the list-serv
    #4 parse body of message according to list-serv history of terms and size
    #4.5 If multiple list-servs on a single device, create a common list-serv function to add "global" message charicteristics collected from multiple list-servs
    #5 parse header and body charicteristics to place message in bucket based upon the type of message and provide the user who sent the message a charicteristic. If a new grouping is found, assign retroactively to all messages in that charicteristic type.
    #6 update visualization data bank
    #7 
    # import the list
    
    
    
if __name__ == "__main__":
    from .test import test_openThreads
    test_openThreads.main()
