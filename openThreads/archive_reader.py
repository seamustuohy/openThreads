import re
import email

def parse_archive(listserv_archive):
    """Parses an entire plain text listserv archive returning a table of messages"""
    raw = get_raw(listserv_archive)
    messages = get_messages(raw)
    return messages

def get_raw(text_file):
    """This function takes the location of the list-serv text file and opens it up for parsing
    """
    text = open(text_file)
    rawText = text.read()
    return rawText

def get_messages(raw):
    """Parses a plain-text email list into a series of fully parsed messages"""
    messages = []
    split_messages = split(raw)
#======================================================================
#    return split_messages
#THE LINE ABOVE IS A TESTING LINE THAT CAN BE REMOVED
    for raw_message in split_messages:
        message = message_parser(raw_message)
        messages.append(message)
    return messages

def split(raw):
    """Takes a plain text list-serv and return a series of unparsed message chunks"""
    who = '\S*\sat\s\S*'
    headerFront = '\nFrom\s' + who + '\s*'
    day = '[A-Z][a-z]{2}'
    month = day
    date = day + '\s' + month + '\s*?\d*?\s\S*?\s\d{4}\n'
    dropTop = headerFront + date
    splitText = re.split(dropTop, raw)
    return splitText

def message_parser(raw_message):
    """Uses the email module to parse a plain text email and then returns a dictionary object  """
    header_parser = {
        "From":parse_From,
        "Date":parse_Date,
        "In-Reply-To":parse_In_Reply_To,
        "References":parse_References,
        }
    parsed_message = email.message_from_string(raw_message)
    message_dict = {}
    for i in parsed_message._headers:
        message_dict[i[0]] = i[1]
    message_dict['Body'] = parsed_message._payload
    for i in message_dict.keys():
        if i in header_parser:
            message_dict[i] = header_parser[i](parsed_message[i])
            if type(message_dict[i]) == dict:
                for x in message_dict[i]:
                    message_dict[x] = message_dict[i][x]
                del message_dict[i]
    return message_dict


def parse_From(full_from_field):
    """Parser for the From field which takes the whole 'From' field and alters only the fields required to take a email formatted message and turn it into a parsable message."""
    message_dict = {}
    regex_from = '(^.*)\s\((.*)\)'
    parsed_from_field = re.findall(regex_from, full_from_field, flags=re.MULTILINE)[0]
    message_dict['Address'] = parse_Address(parsed_from_field[0])
    message_dict['Name'] = parsed_from_field[1]
    return message_dict

def parse_Address(Address):
    """Parser for the Address field that replaces a blank at blank.tld with blank@blank.tld."""
    parsed = re.findall("(.*)\sat\s(.*)\.(.*)", Address)
    email = str(parsed[0][0])+"@"+str(parsed[0][1])+"."+str(parsed[0][2])
    return email

def parse_Date(message_date):
    """Parser for the Date field which takes the whole message and alters only the fields required to take a email formatted message and turn it into a parsable message."""
    message_dict = {}
    chunked_date = re.split('\s', message_date)
    for idx,itm in enumerate(chunked_date):
        if itm == '' or itm == ' ':
            del(chunked_date[idx])
            
    regex= [
        #Note redundancy is for assignment on badly formatted dates
        ('day_name', '([A-Z][a-z]{2})'),
        ('day_number', '(\d{1,2})'),
        ('month_name', '([A-Z][a-z]{2})'),
        ('year', '(\d{4})'),
        ('time', '(\d{1,2}\:\d{1,2}\:\d{1,2})'),
        ('zone', '([+-]\d{4})')
        ]
    if len(chunked_date) < 6:
        n = 0
        for i in regex:
            found = re.findall(i[1], chunked_date[n])
            if found:
                n += 1
                message_dict[i[0]] = found[0]
    else:
        for i in regex:
            #This is taking applying the first regex to the first date item
            message_dict[i[0]] = re.findall(str(i[1]), str(chunked_date.pop(0)))[0]
    if 'time' in message_dict:
        message_dict['hour'] = re.findall("(\d{1,2})\:\d{1,2}\:\d{1,2}",message_dict['time'])[0]
        message_dict['minute'] = re.findall("\d{1,2}\:(\d{1,2})\:\d{1,2}",message_dict['time'])[0] 
        message_dict['seconds'] = re.findall("\d{1,2}\:\d{1,2}\:(\d{1,2})",message_dict['time'])[0]
#TODO Create a compact date format for compating messages
#message_dict['compact'] = parse_compact_date(message_dict)
    return message_dict

#def parse_compact_date(message_dict):
#    months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#    for i in message_dict:
#        print(i,message_dict[i])
#    for i in [i for i,x in enumerate(months) if x == message_dict['month_name']]:
#        month = i + 1
#    
#    if len(str(month)) == 1:
#        month = str(0) + str(month)
#    ('day_number', '04')
#    ('hour', '14')
#    ('zone', '+0100')
#    ('seconds', '52')
#    ('year', '2010')
#    ('day_name', 'Mon')
#    ('month_name', 'Oct')
#    ('time', '14:06:52')
#    ('minute', '06')

def test_parse_Date():
    """A test function  """
    date_struc = ['Thu,', '23', 'Sep', '2008', '11:37:39', '-0700']
    for i in range(5):
        test_string = ""
        for x, n in enumerate(date_struc):
            if x != i:
                test_string += n+" "
        test_string = re.findall("(.*)\s", test_string)[0]
        result = parse_Date(test_string)
        #TODO need to do a check against a set of prebuilt values
        if len(result) != 8:
            if len(result) != 5:
                raise Exception, str(result) + " \nThe above shows that you are a failure"    
    
def parse_In_Reply_To(reply):
    """Parser for the In-Reply-To field which currently does nothing... but I think there will be more to do later."""
    #TODO Do I need this in the future? I can't remember why I saved it
    return reply

def parse_References(references):
    """Parser for the References field which takes the references and makes them into a list."""
    reference_list = re.findall("(<.*?>)", references)
    return reference_list

