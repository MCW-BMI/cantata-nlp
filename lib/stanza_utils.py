import stanza
import os
import sys
import glob
from xml.etree import cElementTree as ET


def run_test_ner():
    """
    Run a quick internal test of the software
    :return:
    """
    text = """
Record date: 2063-12-13




NAME:     Umphrey, Tammy 
MRN:       0942207

The patient is here as a walk-in.  Her spouse is present.

Patient says she is status post a fall this past Monday at home.  Says that she seems
to have lost her balance while opening a door at home.  Denies prodromal
symptoms including shortness of breath, dizziness, or palpitations.  There was no
loss of consciousness.  Patient was seen in the emergency room that day for trauma
to the head.  Had a negative CT of her head and had an x-ray of her pelvis, as she
complained of some hip pain.  Both studies were negative.  Patient was then sent
home with Roxicet.  Patient was seen in the walk-in clinic at CPI yesterday, after
noticing a swollen tongue and some difficulty swallowing.  Patient was immediately
told to stop both her Roxicet and Monopril and was treated for angioedema with
Zantac and Claritin.  Today patient has no further throat tightness or tongue
swelling.  She is, however, uncomfortable continuing the Effexor for unclear
reasons and wants to stop it.

Patient is also complaining of severe low back pain, which she says has persisted
since her fall on Monday.  Did not have an x-ray of the area.  Says it is very painful
to sit.  Roxicet was not helping.  She is off her Ultram as well.

PHYSICAL EXAM:  WD/overweight female in NAD.  Vital signs as per LMR,
WNL.  Weight 213 pounds. 

Lungs - clear bilateral breath sounds.  Cor - RRR, S1, S2, without murmur or S3
noted.  Back - slightly bent gait.  Tenderness over lower sacrum.  No asymmetry or
obvious deformity.  

X-ray of sacrum 12/13/63 - could not see fracture as per my reading.

ASSESSMENT AND PLAN:  

(1)  Angioedema.  Agree that most likely culprits are Roxicet since it was started
     only two days ago, and ACE inhibitors which have been associated with
     angioedema.  Currently on Lopressor and Dyazide, patient's blood pressure
     is WNL.  So will follow for now.

(2)  Low back pain.  Reviewed the possibility of a coccygeal fracture for which
     treatment would not be any different than pain management and a donut
     pillow.  Patient was given a prescription for the pillow.  She was told to look
     out for signs of nerve compression and to go to the ER if she experienced
     any perianal numbness or incontinence.  Will notify patient by phone if x-ray
     shows a fracture. 

(3)  Depression.  Did not feel I was able to speak freely in front of the patient's
     spouse.  Had been put on the Effexor by Dr. Zeman.  Advised patient to let
     her psychiatrist know that we are tapering her off of the Effexor.  Will take
     25 mg q.o.d. for the next week.  

(4)  Pain control.  Will switch from Vicodin to Vicodin ES 1 q. 6 as needed. 
     Knows to go to ER if experiences any symptoms consistent with angioedema.

Return to clinic in approximately one month.



Susan Ullom, M.D.

SU/utz/rankin
 




"""
    stanza.download('en')  # download English model
    nlp = stanza.Pipeline('en', processors='tokenize,ner')  # initialize English neural pipeline
    #doc = nlp( "\n\n  \nGeorge Kowalski has worked  at the Medical College of WI. \n Record date: 2063-12-13.\n\n  \nKowalski, George works at Stanford University\n Susan Ullom, M.D.")  # run annotation over a sentence1
    doc= nlp( text)
    # print ( doc)
    for sent in doc.sentences:
        print("------------ Sentence found ----------")
        # print("Tokens")
        # for token in sent.tokens:
        #     print(f'\ttoken: {token.text}\tner: {token.ner}\t start {token.start_char}\tend {token.end_char}')
        print("Entities")
        for token in sent.ents:
            if token.type == 'PERSON' or token.type == 'DATE':
                print(f'\tentity: {token.text}\tner: {token.type}\t start {token.start_char}\tend {token.end_char}')


def makeTag(tagElement, tagType, matched_text, startPos, endPos, tokenCounter):
    tag = "<" + tagElement + " id=\"P" + tokenCounter + "\" start=\"" + startPos + "\" end=\"" + endPos + "\" text=\"" + matched_text + "\" TYPE=\"" + tagType + "\" comment=\"\" />";
    print("tag: " + tag);
    return tag


def prcess_xml_file(entry, output_dir, nlp):
    """

    :param entry:
    :param output_dir:
    :return:
    """
    file = open(entry, "r")
    file_text = file.read()
    # print(file_text)
    root = ET.fromstring(file_text)
    # print(root)
    # Get text from within XML
    counter = 0
    token_list = []
    for tag in root.iter('TEXT'):
        # print( tag.text)
        doc = nlp(tag.text)
        for sent in doc.sentences:
            print("------------ Sentence found ----------")
            print (sent.text )
            print("Tokens")
            for token in sent.tokens:
                print(f'\ttoken: {token.text}\tner: {token.ner}\t start {token.start_char}\tend {token.end_char}')
            for token in sent.ents:
                if token.type == 'PERSON' or token.type == 'DATE':
                    print(f'\tentity: {token.text}\tner: {token.type}\t start {token.start_char}\tend {token.end_char}')
                    token_list.append(makeTag(tagElement, tagType,  matched_text, startPos , endPos, tokenCOunter))


def run_ner_cd2h(input_dir, output_dir) :
    """
    Process a set of input files per CD2H and the 2014 I2b2 challange and output results that can be evaluated

    :param input_dir:
    :param output_dir:
    :return:
    """
    stanza.download('en')  # download English model
    nlp = stanza.Pipeline('en', processors='tokenize,ner')  # initialize English neural pipeline
    entries = os.scandir(input_dir)
    for entry in entries:
      print (f"Processing input file : {entry.path} {entry.name}")
      prcess_xml_file(entry, output_dir, nlp)
      sys.exit(1)