from email import header
import re

headerSetext =r'''
       
        \n(=+|-+) # matches newline followed by by one or more = or - 
        [ \t]* # matches 0 or more occurences of space or tab
        \n+ # matches 1 or morce occurences of new line 
    
    '''
headerSetextText = r'''
     ### setext style of headers 
        ^(.+) # starts with any character (.) with one ore more char occurencies (+)
        [ \t]{0,99} # matches space or tab with 0-99 occurences 
     
    '''

headerAtx = r'''
    
        ^(\#{1,6})  # starts with 1-6 # chars 
        [ \t]* # matches space or tab followed by string       
    
    '''

headerAtxText = r'''
     ### atx style of headers 
        (.+?)       # \2 = Header text
        [ \t]{0,99}
        (?<!\\)     # ensure not an escaped trailing '#'
        \#*         # optional closing #'s (not counted)
        \n+
    
    '''
headerSetextPatterns = re.compile("({}{})".format(headerSetext,headerSetextText),re.IGNORECASE|re.VERBOSE) 
headerAtxPatterns = re.compile("({}{})".format(headerAtx,headerAtxText),re.IGNORECASE|re.VERBOSE) 


def markdownConverter(title):
        ############### global patterns #####################
    # pattern to split between description and the header content in MD file
    #headerPatterns = re.compile("({}{})|({}{})".format(headerSetext,headerSetextText,headerAtx,headerAtxText),re.IGNORECASE|re.VERBOSE) 



    # pattern to split betwene header text and header style
    #headerStylePatterns = re.compile("({})|({})".format(headerSetext,headerAtx),re.IGNORECASE|re.VERBOSE)
   



    f = open(f"CSS.md")
    content =  f.read()

    if re.match(headerSetextPatterns,content):
        headerPatterns= headerSetextPatterns
        headerStylePatterns = re.compile("({})".format(headerSetext),re.IGNORECASE|re.VERBOSE)
    elif re.match(headerAtxPatterns,content):
        headerPatterns= headerAtxPatterns
        headerStylePatterns = re.compile("({})".format(headerAtx),re.IGNORECASE|re.VERBOSE)
    else:
        return

    headerConverter(content,headerPatterns,headerStylePatterns)
    textConverter(content, headerPatterns)



#def headerRepl(matchobj):
#    if matchobj.group(0) =="#":
#def getHeaderStyle(headerTextMD):




def headerConverter(content,headerPatterns,headerStylePatterns):
    #get a raw header text from MD
    headerTextMD =headerPatterns.match(content).group()

    headerTextMD =re.match(headerStylePatterns,headerTextMD).group()
    headerTextMD =re.sub(r"[^#]","",headerTextMD)
    print(len(headerTextMD))
    #convert it

    #headerText = headerStylePatterns.sub("",headerTextMD)
    #headerText = headerText.replace("\n","")
    #print(headerText)
    #return headerText


def textConverter(content, headerPatterns):
    text = headerPatterns.sub("",content)
    text = text.replace("\n","")

    return text

markdownConverter("CSS")