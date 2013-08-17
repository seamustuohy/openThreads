import re

from . import logger

def PGP(body):
    "Get PGP content from a message body if it exists. Return false if it does not."

    RFC4880_ASCII_OpenPGP_lines  = [
        "PGP MESSAGE",
        "PGP PUBLIC KEY BLOCK",
        "PGP PRIVATE KEY BLOCK",
        "PGP SIGNATURE",
        "PGP MESSAGE, PART \d/\d",
        "PGP MESSAGE, PART \d"
        ]
    dashes = "\-{5}"
    PGP = []
    for armor_line in RFC4880_ASCII_OpenPGP_lines:
        if PGP == []:
            beginPGP = dashes + "BEGIN " + armor_line + dashes + "\n"
            endPGP = dashes + "END " + armor_line + dashes + "\n"
            rePGP = beginPGP + '(.*?)' + endPGP            
            PGP = re.findall(rePGP, body, flags=re.DOTALL)
    if PGP != []:
        logger.debug("PGP Key FOUND!!!")
        return PGP
    else:
        logger.debug("no PGP key found")
        return False

def scrubbed(body):
    """When parsing from a plain_text listerv this function Returns true if an email is html formatted and false if an email was not"""
    next_part = re.findall("\-{14} next part \-{14}(.*)(?=From.*)?", body, flags=re.DOTALL)
    if next_part != []:
        return True
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

