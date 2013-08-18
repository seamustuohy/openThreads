import re

from . import logger

def PGP(body, scrape=None):
    """Get PGP content from a message body if it exists. Return false if it does not. If scrape, then return the body text scraped of PGP key as well
    @param body The plain text body of a email
    @param scrape A control command (True) that lets function know to scrape out the PGP key. Did I mention that you use the value True to get this to work?
    
    """
    RFC4880_ASCII_OpenPGP_lines  = [
        "PGP MESSAGE",
        "PGP PUBLIC KEY BLOCK",
        "PGP PRIVATE KEY BLOCK",
        "PGP SIGNATURE",
        "PGP MESSAGE, PART \d/\d",
        "PGP MESSAGE, PART \d"
        ]
    dashes = "\-{5}"
    header = dashes+"BEGIN PGP SIGNED MESSAGE"+dashes+"\nHash.*?\n"
    PGP = []
    for armor_line in RFC4880_ASCII_OpenPGP_lines:
        if PGP == []:
            beginPGP = dashes + "BEGIN " + armor_line + dashes + "\n"
            endPGP = dashes + "END " + armor_line + dashes + "\n"
            rePGP = beginPGP + '(.*?)' + endPGP            
            PGP = re.findall(rePGP, body, flags=re.DOTALL)
    if PGP != []:
        if scrape == True:
            new_body = re.sub(rePGP, "", body, flags=re.DOTALL)
            rm_header = re.sub(header, "", new_body, flags=re.DOTALL)
            if rm_header:
                new_body = rm_header
            return PGP, new_body
        else:
            return PGP
    else:
        if scrape == True:
            return False, body
        else:
            return False
        
def scrubbed(body, scrape=None):
    """When parsing from a plain_text listerv this function Returns true if an email is html formatted (as well as the body with this indicator scraped from it if scrape=True) and false if an email was not
    @param body The plain text body of a email
    @param scrape A control command (True) that lets function know to scrape out the html message. 

    """
    htmlScrubbed = "\-{14} next part \-{14}(.*)(?=From.*)?"
    next_part = re.findall(htmlScrubbed, body, flags=re.DOTALL)
    if next_part != []:
        if scrape == True:
            new_body = re.sub(htmlScrubbed, "", body, flags=re.DOTALL)
            return True, new_body
        else:
            return True, body
    else:
        if scrape == True:
            return False, body
        else:
            return False

def message_components(body):
    lines = re.split("\n", body)
    message_set = []
    message_num = 0
    line_type = False
    reply_len = 0
    for i in lines:
        if i == '':
            pass
        elif re.match(">", i):
            new_reply_len = len(re.findall(">",i))
            if line_type == "user":
                message_num += 1
                reply_len = new_reply_len
            elif reply_len != new_reply_len:
                message_num += 1
                reply_len = new_reply_len
            if len(message_set) == message_num+1:
                message_set[message_num] = '\n'.join((message_set[message_num], i))
            else:
                message_set.append(i)
            line_type = "reply"
        elif re.match("(?!>)", i):
            if line_type == "reply":
                message_num += 1
            if len(message_set) == message_num+1:
                message_set[message_num] = '\n'.join((message_set[message_num], i))
            else:
                message_set.append(i)
            line_type = "user"
    return message_set

def un_quote(quoted_reply):
    unquoted_reply = re.sub('\n>*', '\n', quoted_reply)
    unquoted_reply = re.sub('^>*', '', unquoted_reply)
    return unquoted_reply

