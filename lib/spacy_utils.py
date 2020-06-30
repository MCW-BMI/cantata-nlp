#  Copyright (c) 2020. Medical College of Wisconsin

import os
import sys
import glob
from xml.etree import cElementTree as ET
import spacy
import dateparser
import re
import spacy
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokenizer import Tokenizer
from spacy.tokens import Span
from pathlib import Path

def custom_tokenizer(nlp, infix_reg):
    """
    Function to return a customized tokenizer based on the infix regex
    PARAMETERS
    ----------
    nlp : Language
    A Spacy language object with loaded model
    infix_reg : relgular expression object
    The infix regular expression object based on which the tokenization is to be
    carried out.
    RETURNS
    -------
    Tokenizer : Tokenizer object
    The Spacy tokenizer obtained based on the infix regex.
    """
    return Tokenizer(nlp.vocab, infix_finditer=infix_reg.finditer)


def add_date_ent(matcher, doc, i, matches):
    """
    on_match function to name the valid date as a DATE entity
    for reference see https://spacy.io/usage/linguistic-features#on_match

    PARAMETERS
    ----------
    matcher : Matcher
    The Matcher instance
    doc : Doc
    The document the matcher was used on
    i : int
    Index of the current match
    matches : list
    A list of (match_ic, start, end) tuples, describing the matches. A matched
    tuple describe the span doc[start:end]
    RETURNS:
    -------
    The function doesn't return a value rather append a DATE entity to each valid date
    and print the date with its validity
    """
    match_id, start, end = matches[i]
    match_str = doc[start:end].text
    print(match_str, 'Suspect')

    if dateparser.parse(match_str):
        entity = Span(doc, start, end, label="MYDATE")
        doc.ents += (entity,)
        print(   match_str, 'VALID')
    else:
        print(  match_str, 'INVALID')


def add_regex_flag(vocab, pattern_str):
    """
    Function to create a custom regex based flag for token pattern matching
    Parameters
    ----------
    vocab : Vocab
    The nlp model's vocabulary, which is simply a lookup to access Lexeme objects as well as
    StringStore
    pattern_str : String
    The string regular expression pattern we want to create the flag for
    RETURNS
    -------
    flag_id : int
    The integer ID by which the flag value can be checked.
    """
    flag_id = vocab.add_flag(re.compile(pattern_str).match)
    return flag_id

def run_test_ner():

    """
    Run a quick internal test of the Spacy software
    :return:
    """
    # This note is a fake report

    text = """
Record date: 2063-12-13




NAME:     Doe, Jane 
MRN:       98765432

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

X-ray of sacrum 01/19/64 - could not see fracture as per my reading.

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

Aug-10-2018

15-Dev-2013

Jan 12 2003

Jan 14

January

"""

    nlp = spacy.load("en_core_web_md")
    # this is needed to override the tokenization and keep dash and slash words ( aka dates , togeather )
    # https://spacy.io/usage/linguistic-features#native-tokenizers
    infix_re = re.compile(r'''[-/,]''')
    nlp.tokenizer = custom_tokenizer(nlp, infix_re)
    # We use EntityRuler instead of matcher = Matcher(nlp.vocab, validate=True)
    # because it handles overlapping entities .
    # To overwrite overlapping entities, you can set overwrite_ents=True on initialization
    # https://spacy.io/usage/rule-based-matching#entityruler-usage
    # the example="" in this jsonL file is not needed , but added as a placeholder for documentation on the
    # pattern being matched. - GK
    ruler = EntityRuler(nlp, overwrite_ents=True).from_disk("./spacy_patterns.jsonl")
    # not needed , but good ref : DATE = nlp.vocab.strings['DATE']

    # See https://spacy.io/usage/rule-based-matching#entityruler-files
    # Moved to JSONL file
    # e_patterns = [
    #      # MM/DD/YYYY and YYYY/MM/DD
    #      {"label": "DATE1", "pattern": [{'IS_DIGIT': True}, {'ORTH': '/'}, {'IS_DIGIT': True}, {'ORTH': '/'}, {'IS_DIGIT': True}]},
    #      # MM-DD-YYYY and YYYY-MM-DD
    #      {"label": "DATE1", "pattern": [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]},
    #      # MM/DD and YYYY/MM
    #      {"label": "DATE1", "pattern": [{'IS_DIGIT': True}, {'ORTH': '/'}, {'IS_DIGIT': True}]},
    #  ]
    # ruler.add_patterns(e_patterns)
    # ruler.to_disk("./spacy_patterns.jsonl")
    nlp.add_pipe(ruler)
    doc = nlp(text)

    for ent in doc.ents:
        print ( f"ENTITY: {ent.text} with label: {ent.label_} from {ent.start_char} to {ent.end_char}" )


def makeTag(tagElement, tagType, matched_text, startPos, endPos, tokenCounter):
    tag = "<" + tagElement + " id=\"P" + str(tokenCounter) + "\" start=\"" + str(startPos ) + "\" end=\"" + str(endPos) + "\" text=\"" + matched_text + "\" TYPE=\"" + tagType + "\" comment=\"\" />";
    print("tag: " + tag);
    return tag

def process_xml_file(entry, output_dir, nlp):
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
        # for ent in doc.ents:
        #     print(f"ENTITY: {ent.text} with label: {ent.label_} from {ent.start_char} to {ent.end_char}")
        #print(doc)
        print( "Text:")
        print ( [t.text for t in doc])
        for sent in doc.sents:
            # print(f"S: {sent.text}" )

            for entity in sent.ents:
                print("\tE:");
                print(f'\tentity: {entity.text}\tner: {entity.label_}\t start {entity.start_char}\tend {entity.end_char}')
                # if entity.type == 'PERSON' :
                #     token_list.append(makeTag('NAME', 'PATIENT', entity.text, entity.start_char , entity.end_char, counter))
                #     counter = counter + 1
                if entity.label_ == 'MDATE'  :
                    token_list.append(makeTag('DATE', 'DATE', entity.text, entity.start_char, entity.end_char, counter))
                    counter = counter + 1
                # if entity.type == 'CARDINAL':
                #     if len ( entity.text ) == 7:
                #         token_list.append(makeTag('ID', 'MEDICALRECORD', entity.text, entity.start_char, entity.end_char, counter))
                #         counter = counter + 1
    return token_list

def create_output_cd2h(output_dir, entry, token_list):

    file = open(entry, "r")
    file_text = file.read()
    # print(file_text)
    root = ET.fromstring(file_text)
    # print(root)
    # Get text from within XML
    counter = 0

    for tag in root.iter('TEXT') :
        text = tag.text

    out_file = open(output_dir + "/" + entry.name, "w")
    out_file.write("""<?xml version="1.0" encoding="UTF-8" ?>\n<deIdi2b2>\n<TEXT><![CDATA[""");
    out_file.write( text);
    out_file.write("]]></TEXT><TAGS>\n");
    for token in token_list:
        print(token)
        out_file.write(token + "\n");
    out_file.write("</TAGS>\n</deIdi2b2>\n");
    out_file.close()

def run_cd2h(input_dir, output_dir, single_file_name):
        """
        Process a set of input files per CD2H and the 2014 I2b2 challange and output results that can be evaluated

        :param input_dir:
        :param output_dir:
        :return:
        """
        # Set up NLP
        nlp = spacy.load("en_core_web_md")

        # This breaks up words on dash slash and periods ( from end of sentences ) for better parsing
        infix_re = re.compile(r'''[-/,.]''')
        nlp.tokenizer = custom_tokenizer(nlp, infix_re)

        ruler = EntityRuler(nlp, overwrite_ents=True,  validate=True ).from_disk("./spacy_patterns.jsonl")
        nlp.add_pipe(ruler)
        # Dir of XML to process
        if single_file_name:
            entry = Path(f"{output_dir}/{ single_file_name}" )
            token_list = process_xml_file(entry, output_dir, nlp)
            for token in token_list:
                print("TOKEN " + token)
            create_output_cd2h(output_dir, entry, token_list)
        else:
            entries = os.scandir(input_dir)
            for entry in entries:
                print(f"Processing input file : {entry.path} {entry.name}")
                token_list = process_xml_file(entry, output_dir, nlp)
                for token in token_list:
                    print("TOKEN " + token)
                create_output_cd2h(output_dir, entry, token_list)

        sys.exit(0)