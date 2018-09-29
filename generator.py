#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import sys
import os
from collections import defaultdict
import numpy as np
import re

def parse_id_melt(fileMelt):
    """
    function that reads the file melt and extract the key words and the context,
    return:
    - a dictionary with the folowing structure:
        { (key_word1, cat_syn, context_id, key_w_id): [(word1,cat_syn), (word2,cat_syn), ... (key_word,cat_syn), ... (wordn,cat_syn)],
        (key_word2, cat_syn, context_id, key_w_id): [...],
        ...
        }
    - a set which contains all the words appeared in the melt file (key_word and words in context)
    """
    # create a dictionnary to store all the sentences in file melt, and a set to stock the vocabulary in melt
    dico_melt = {}
    voc_melt = set()
    try:
        with open(fileMelt, 'r') as stream:
            for line in stream:
                sentence = line.rstrip().split()
                # take the 4 first elements to create a quartple (key_word, cat_syn, context_id, key_w_id)
                sent_id, w_key, cat_key, w_id = sentence[:4]    
                voc_melt.add(w_key.lower())            
                # create an list to stock each sentence so that the order of the words in context can be perserved
                dico_sent = []
                # look into the context, and extract each word form with its syntactic category
                for element in sentence[4:]:
                    w_cat, w_form = element.split("/")[1:]
                    # clean the word form (if starts with "*", strip it)
                    if w_form.startswith("*"):
                        w_form = w_form[1:].lower()
                    dico_sent.append((w_form, w_cat))
                    voc_melt.add(w_form)
                # attach the list to melt dictionnary
                dico_melt[(w_key, cat_key, sent_id, w_id)] = dico_sent
        # pprint.pprint(dico_melt)
        print(voc_melt) # len(voc_melt = 2049)
        return dico_melt, voc_melt 
    except OSError as e:
        print(e.errno)


class Fredist(object):
    """
    A class that reads the Fredist repository and stock the neighbor words for each of the key word
    input dirname is the repository which stores 4 files for each category of words: A, N, V and ADV
    return a dictionnary neighbors with the following structure: 
    { (key_word1, cat_syn): {neigh1:score_sim, neigh2:score_sim, neigh3:score_sim, ...},
      (key_word2, cat_syn): {...},
      ...
    }
    """

    def __init__(self, dirname):
        self.dirname = dirname
        self.cats_num = 0
        self.neighbors = {}
 
    def __iter__(self):
        for fName in os.listdir(self.dirname):
            if fName != 'README': # skip the README file
                # print(fName)
                self.cats_num += 1
                joined_rn = os.path.join(self.dirname, fName)
                sys.stderr.write("reading file from %s\n" %joined_rn)
                self.neighbors.update(self.read_a_thesaurus(joined_rn))


    def read_a_thesaurus(self, filename):
        dico_thesau = defaultdict()
        with open(filename, 'r') as stream:
            for line in stream:
                # words is a list of word, with the first element <cat|key_word>, and the following <cat_neigh|neig>:<neig score> 
                words = line.rstrip().split()
                cat, w_key = words[0].split("|") 
                w_neigh = {} 
                for w in words[1:]:
                    one_neig, score_sim = w.split("|")[1].split(":")
                    # print(one_neig, score_sim)
                    w_neigh[one_neig] = score_sim
                # print(w_neigh)
                # input()
                dico_thesau[(w_key, cat)] = w_neigh
        # print(dico_thesau)
        return dico_thesau

    def show_fred_stats(self):
        print("In total %d files have been read.\n%d key_word and their 100 neighbors have been recorded." % (self.cats_num, len(self.neighbors)))



def read_frwak(frwakFile):
    """
    read the file frwak and stock the 700-dimention vectors in a numpy array
    return wordVector dictionnary:
    {(word, cat_syn): nparray([0.0001, -0.00034, ...]),
     (word, cat_syn): nparray(...),
     ...
    }
    """   
    wordVectors = {}
    fileObject = open(frwakFile, encoding = "ISO-8859-1")
    print("FrWak file is openning...")

    not_noise = 0
    for line in fileObject:
        line = line.strip().lower()
        if not line.startswith("215020"): #skip the first line
            word_cat = line.split()[0] #get the word_category  
            if '_' in word_cat: # take only the lines with the structure <word_catSyntaxe>
                len_w_c = len(line.split()[0].split("_"))
                if len_w_c == 2: # avoid valueError when the structure <w_w_cat> appears
                    word, cat_w = line.split()[0].split("_")
                    not_noise +=1
                    wordVectors[(word, cat_w)] = np.zeros(len(line.split())-1, dtype=float)
                    for index, vecVal in enumerate(line.split()[1:]):
                        wordVectors[(word, cat_w)][index] = float(vecVal)
                
    # print(wordVectors)
    sys.stderr.write("Vectors read from: %s\nWords recorded = %d/215020\n" % (frwakFile, not_noise))
    return wordVectors






def score_cosinus():
    pass    





if __name__ == "__main__":
    #-------- files --------
    melt_file = "lexsubfr_semdis2014_test.id_melt"
    # melt_file = "melt_extract.id_melt"
    fred_rep = "../ressources/thesauri-1.0"
    frwak_file = "../ressources/frWac_postag_no_phrase_700_skip_cut50.txt"
    #frwak_file = "try108722.txt"

    #-------- test --------
    #melt_dico, melt_voc = parse_id_melt(melt_file)

    # candidates_fredist = Fredist(fred_rep)
    # candidates_fredist.__iter__() # candidate fredist is ready
    # candidates_fredist.show_fred_stats()

    frwak_dico = read_frwak(frwak_file)

