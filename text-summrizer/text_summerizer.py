import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text ='''The founder and sponsor of a far-right network of secretive, men-only, invitation-only fraternal lodges in the US is a former industrialist who has frequently speculated about his future as a warlord after the collapse of America, a Guardian investigation has found.

Federal and state tax and company filings show that the Society for American Civic Renewal (SACR) and its creator, Charles Haywood, also have financial ties with the far-right Claremont Institute.

SACR’s most recent IRS filing names Haywood as the national organization’s principal officer. Other filings identify three lodges in Idaho – in Boise, Coeur d’Alene and Moscow – and another in Dallas, Texas.

SACR’s public-facing presence is confined to a slick one-page website advertising the organization’s goal as “civilizational renaissance”, and a society “with strong leadership committed to family and culture”.

The site claims SACR is “raising accountable leaders to help build thriving communities of free citizens” who will rebuild “the frontier-conquering spirit of America”. It condemns “those who rule today”, saying that they “corrupt the sinews of America”, “[alienate] men from family, community, and God” and promising to “counter and conquer this poison”.

It also prominently features SACR’s cross-like insignia or “mark” which it describes variously as symbolizing “sword and shield” and the rejection of “Modernist philosophies and heresies”.

Finally, the site advises that SACR membership “is organized primarily around local groups overseen by a national superstructure” and “is by invitation only”, offering an email address for those “interested in learning more”.

The Guardian emailed the website contact address from a pseudonymous address but received no response.'''

lent=0.1



def summerize_text(text,lent=0.2):
    cleaned_text = text.replace('\n\n','').replace('\n','')

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(cleaned_text)
    
    stop_words = list(STOP_WORDS)
    
    token = [token.text for token in doc]
    
    
    word_freq ={}
    
    for word in doc:
        if word.text.lower() not in stop_words and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] =1
            else:
                word_freq[word.text]+=1



    # this is updated version of the word_freq/
    

    max_freq = max(word_freq.values())
    
    
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
        
    sent_token = [sent for sent in doc.sents]
    
    sent_score={}
    
    
    for sent in sent_token:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in  sent_score.keys():
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]
                    
                    
    select_len = int(len(sent_score)*lent)
    
    
    summary = nlargest(select_len,sent_score,key=sent_score.get)
    
    
    summary_text = ''
    
    for token in summary:
        summary_text+=(token.text)
        
    print(summary_text)
        
    return (summary_text)


summerize_text(text,lent)