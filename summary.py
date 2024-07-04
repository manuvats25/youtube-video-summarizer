import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

'''You only have to run :| 1. pip install spacy
                         | 2.python -m spacy download en_core_web_sm
'''                 


def summarize(text, per):
    # spacy.cli.download("en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

video_text="If you only have 24 hours in a day, your success is dependent upon how you use the 24. You got to hear me. People talk about Oprah Winfrey,  you know, Ted Turner, Warren Buffett. Listen to me.  I don't care how much money you make. You only get 24 hours in a day and the difference between  Oprah and the person that\'s broke is Oprah uses her 24 hours wisely. That\'s it. Listen to me. That\'s it. You get 24. I don\'t care you broke,  you grew up broke. I don\'t care if you grew up rich, I don\'t care you\'re in college,  you\'re not in college. You only get 24 hours and I blew up literally. I went from being a high school dropout to selling 6,000 books in less than six months. What happened in my 24 hours? I was like, okay, here you got to get  a grip on your 24 hours cause you bought to be  broke for the rest of your life. And it just, all I need you to do for me. I can tell you all about your life. If you just write down  your 24-hour schedule for me, you let me look at it. I can tell you where you\'re gonna be  in five years. I can tell you where you gonna be in 20 years, if you keep that schedule."
video_text='''to integrate them as we roll.out new experiences in Search.. you might want to explore more..And I can click See More.to expand here as well.. in front of thousands.of people, I'd. be checking out some of.these web results right now.... Let's see if we can make.this code a little better..But now, we're stuck.. Let's get some help..These are some cool.pictures, and I. bet my niece will love these.. Let's insert them.into the dock for fun..I'm going to play with the zoom.. Let's see..and even explains the.reasoning behind the fix.. just like you asked..sunsets, or waterfalls.. Of course, we want you to do.more than just search photos..We also want to help.you make them better.. are edited in Google Photos..can, whether you're walking,.cycling, or driving.. Let me show you what I mean..more relevant with.each passing year.. is the most profound way we.will advance our mission..helpful for a while.. With generative AI, we.are taking the next step..And then colors.. Let's see..- R-I-A-N.. - Life got a little easier..Tablet and Pixel Fold.. Check out this video..Phew.. Live demos are always.a little nerve-racking..while also matching.their lip movements.. course created in partnership.with Arizona State University..notice that we now keep the.multitasking windows paired.. and Slides earlier to.prep for this keynote..and communicate the results.. being used in.specialized domains..Yes.. - No.. - Yes!.-Hey, Tony.. TONY: Hey, Aparna.. APARNA PAPPU:completely new images from.your imagination right in Bard..or you just want to have fun.and create something new..to get things like quality.and local nuances right..Let's end with an example of.how this can help you at work..So let me show you.what this looks like..And I like classic art,.so let me tap that..and I'm going to tap on.the new option for emojis..to Brazil to our new Bayview.campus right next door..to create a new standard.for foldable technology..right into my message, like so..set when we get a new phone..also unlock a whole new category.of experiences on Search..Or if you're lazy like me,.you can just use your voice..in this new form factor, and we.see tremendous potential here.. have a versatile.form factor, making.means to develop new products..I see a new suggestion on.there for generating images..and even people like you and me..It looks like it's going.to be a beautiful ride..So let's start watching this.video on the big screen..insights and perspectives.from across the web.. It looks like, in.northern California,.to apps like Docs or Sheets.to build on with others..Looks like it's.going to pour later..Let's look at this example..just like PaLM 2..to help '''
# video_text=" you aer the boy . hell'o you "

print(summarize(video_text,.25))
# vide_text = video_text.replace("y","?")
msg = "Hell'o"
# print(msg.replace("'", ""))
# video_text=video_text.replace("'", "")
# print(video_text)
# print(summarize(video_text,.25))


