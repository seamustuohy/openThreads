import re

def PGP(self, body):
    "Get PGP content from a message body if it exists. Return false if it does not."
    beginPGP = '\-{5}[A-Z]{5} [A-Z]{3} [A-Z]{9}\-{5}\n'
    endPGP = '\-{5}[A-Z]{3} [A-Z]{3} [A-Z]{9}\-{5}\n'
    rePGP = beginPGP + '(.*?)' + endPGP
    PGP = re.findall(rePGP, body, flags=re.DOTALL)
    if PGP != []:
        return PGP
    else:
        return False

def scrubbed(body):
    """When parsing from a plain_text listerv this function Returns true if an email is html formatted and false if an email was not"""
    next_part = re.findall("-------------- next part --------------(.*)", i['Body'], flags=re.DOTALL)
    if next_part != []:
        return True
    else:
        return False

def message_components(body):
    lines = re.split("\n", body)
    print(lines)
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
    unquoted_reply = re.sub("\n>*", "\n", quoted_reply)
    return unquoted_reply
