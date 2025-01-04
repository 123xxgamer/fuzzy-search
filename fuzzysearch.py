#!/usr/bin/python
print('Content-type: text/html\n')

f=open("firstnames.txt", encoding="utf-8")
firstnames=f.read()
f.close()
f=open("lastnames.txt", encoding="utf-8")
lastnames=f.read()
f.close()
f=open("adverbs.txt", encoding="utf-8")
adverbs=f.read()
f.close()
f=open("adjectives.txt", encoding="utf-8")
adjectives=f.read()
f.close()
f=open("nouns.txt", encoding="utf-8")
nouns=f.read()
f.close()
f=open("verbs.txt", encoding="utf-8")
verbs=f.read()
f.close()
f=open("all.txt", encoding="utf-8")
alltext=f.read()
f.close()
firstnames=firstnames.split()
lastnames=lastnames.split()
adverbs=adverbs.split()
adjectives=adjectives.split()
nouns=nouns.split()
verbs=verbs.split()
alltext=alltext.split()
import cgitb
cgitb.enable()

import cgi

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def make_html(title, body):
    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <link href="fuzzysearchstyles.css" rel="stylesheet">
    <meta charset="utf-8">
    """
    html+= '<title>' + title + '</title></head>'
    html+= '''<body id="fuzzy"><nav>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a class="active" href="fuzzysearch.py">Fuzzy-It!</a></li>
      </ul>
    </nav>''' + body + '</body></html>'
    return html

def make_form():
    html = """
    <form action="fuzzysearch.py" method="GET">
    What is your preferred minimum percentage similarity for results? Don't use anything lower than 60.
    <br>
    <input id="simperc" type="number" name="simperc" min="60" max="100">
    <label for="simperc">%</label>
    <br><br>
    What is your search query? <em>(Note that this search utility automatically diregards any whitespace within your query.)</em>
    <br>
    <label for="query">Query:</label>
    <input id="query" type="text" name="query">
    <input id="IgnCap" type="checkbox" name="IgnCap">
    <label for="IgnCap">Ignore Capitalization?</label>
    <br><br>
    <label for="datas">Which dataset would you like to fuzzy-search from? Choose a dataset to search in:</label>
    <select name="datas" id="datas" value="firstnames">
      <option value="all">ALL: All the datasets combined</option>
      <option value="adverbs">Adverbs</option>
      <option value="firstnames">First Names</option>
      <option value="lastnames">Last Names</option>
      <option value="nouns">Nouns</option>
      <option value="verbs">Verbs</option>
      <option value="adjectives">Adjectives</option>
    </select>
    <br><br>
    Would you like to limit the results to being a maximum of a certain character count difference with your query?
    <br>
    <input id="lim" type="checkbox" name="lim">
    <label for="lim">Yes, limit by difference in character count.</label>
    <br><br>
    If so, what is your preferred maximum absolute difference in number of characters between your query and each possible result? Note that if the above checkbox is not checked, this field will not affect the results. If a value is not entered, this field will not affect the results.
    <br>
    <label for="maxdif">Maximum Character Count Difference (between 0 and 6):</label>
    <input type="number" id="maxdif" name="maxdif" min="0" max="6">
    <br><br>
    <input type="submit" value="Search"></form>"""
    return html



data = cgi.FieldStorage()
#check if any form data present
if (len(data) != 0):
    if ('query' in data and len(data['query'].value)>0):
        qexist=True
        if ('simperc' in data and len(data['simperc'].value)>0):
            simexist=True
            query = data['query'].value
            query=query.split()
            query=''.join(query)
            simperc= data['simperc'].value
            simperc=float(simperc)/100
            new=[]
            if simperc>=0.6 and simperc <=1.0:
                if ('IgnCap' in data):
                    igncap=data['IgnCap'].value
                    if igncap=='on':
                        i=0
                        while i<len(firstnames):
                            firstnames[i]=firstnames[i].lower()
                            i+=1
                        while i<len(lastnames):
                            firstnames[i]=firstnames[i].lower()
                            i+=1
                        while i<len(adverbs):
                            firstnames[i]=firstnames[i].lower()
                            i+=1
                        while i<len(adjectives):
                            firstnames[i]=firstnames[i].lower()
                            i+=1
                        while i<len(nouns):
                            firstnames[i]=firstnames[i].lower()
                            i+=1
                        while i<len(verbs):
                            firstnames[i]=firstnames[i].lower()
                            i+=1
                        query=query.lower()
                datab=data['datas'].value
                if datab=='adverbs':
                    for e in adverbs:
                        if similar(query,e)>=simperc:
                            new.append(e)
                if datab=='firstnames':
                    for e in firstnames:
                        if similar(query,e)>=simperc:
                            new.append(e)
                if datab=='lastnames':
                    for e in lastnames:
                        if similar(query,e)>=simperc:
                            new.append(e)
                if datab=='nouns':
                    for e in nouns:
                        if similar(query,e)>=simperc:
                            new.append(e)
                if datab=='verbs':
                    for e in verbs:
                        if similar(query,e)>=simperc:
                            new.append(e)
                if datab=='adjectives':
                    for e in adjectives:
                        if similar(query,e)>=simperc:
                            new.append(e)
                if datab=='all':
                    for e in alltext:
                        if similar(query,e)>=simperc:
                            new.append(e)
                valid=True
            else:
                valid=False
        else:
            simexist=False
    else:
        qexist=False
    
    body= '<h1>Fuzzy Search</h1><h2>Search Utility Page</h2>'
    if qexist and simexist:
        body+='<h3>Query: ' + query + '</h3>'
        if ('lim') in data and ('maxdif') in data:
            maxdif=data['maxdif'].value
            if len(maxdif)>0:
                maxdif=int(maxdif)
                qlen=len(query)
                i=0
                while i<len(new):
                    if (abs(qlen-len(new[i])))>maxdif:
                        new.remove(new[i])
                    else:
                        i+=1
        if len(new)>0:
            body+= 'Result(s) with '+ str(simperc*100)+ "% similarity or more:"
            if ('lim') in data:
                body+="<br><em>Limiting by a maximum character count difference of "+data['maxdif'].value+"</em>"
            body+="<ul>"
        elif valid==True:
            body+='No results have been found. Try a different search by clicking try again below!'
        if valid==False:
            body+= '<h3>Inputted Minimum Percent Similarity: '+str(simperc*100)+'%</h3>'
            body+='Your inputted percentage similarity is not between 60% and 100%. Click try again and adjust it to a valid value!'
        for c in new:
            body += '<li>'+str(c)+'</li>'
        body+= '</ul><br>'
    elif not qexist:
        body+='You did not enter a query. Please try again and enter a query.<br>'
    else:
        body+='You did not enter a min similarity percentage. Please try again and enter a min similarity percentage.'
    body+='<a href="fuzzysearch.py">Try Again</a>'
    html = make_html('Form Result', body)
    print(html)
#if no form data, return the form html instead of result
else:
    body = '<h1>Fuzzy Search</h1><h2>Search Utility Page</h2>'
    body+=make_form()
    html = make_html('Form Results', body)
    print(html)
