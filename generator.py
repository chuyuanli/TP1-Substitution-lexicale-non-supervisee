#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import sys
import os
from collections import defaultdict


def parse_id_melt(fileMelt):
    """
    function that reads the file melt and extract the key words and the context,
    return a dictionary with the folowing structure:
    { (key_word1, cat_syn, context_id): {word1: cat_syn, word2: cat_syn, ... key_word: cat_syn, ... wordn: cat_syn},
      (key_word2, cat_syn, context_id): {...},
      ...
    }
    """
    # create a dictionnary to store all the sentences in file melt
    dico_melt = {}
    try:
        with open(fileMelt, 'r') as stream:
            for line in stream:
                sentence = line.rstrip().split()
                # take the 3 first elements to create a triple (key_word, cat_syn, context_id)
                sent_id, w_key, cat_key = sentence[:3]                
                # create an inner dictionnary to stock each sentence
                dico_sent = {}
                # look into the context, and extract each word form with its syntactic category
                for element in sentence[4:]:
                    w_cat, w_form = element.split("/")[1:]
                    # clean the word form (if starts with "*", strip it)
                    if w_form.startswith("*"):
                        w_form = w_form[1:]
                    dico_sent[w_form] = w_cat
                # attach the inner dictionnary to melt dictionnary
                dico_melt[(w_key, cat_key, sent_id)] = dico_sent
        # pprint.pprint(dico_melt)
        return dico_melt    
    except OSError as e:
        print(e.errno)


class Fredist(object):
    """
    A class that reads the Fredist repository and stock the neighbor words for each of the key word
    input dirname is the repository which stores 4 files for each category of words: A, N, V and ADV
    return a dictionnary neighbors with the following structure: 
    { (key_word1, cat_syn): [neigh1, neigh2, neigh2, ...],
      (key_word2, cat_syn): [...],
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
                # words is a list of word, with the first element <cat|key_word>, and the following <neig>:<neig score> 
                words = line.rstrip().split()
                cat, w_key = words[0].split("|") 
                w_neigh = []
                for w in words[1:]:
                    one_neig = w.split(":")[0].split("|")[1]
                    w_neigh.append(one_neig)
                # print(w_neigh)
                # input()
                dico_thesau[(w_key, cat)] = w_neigh
        # print(dico_thesau)
        return dico_thesau

    def show_fred_stats(self):
        print("In total %d files have been read.\n%d key_word and their 100 neighbors have been recorded." % (self.cats_num, len(self.neighbors)))



def candidates_frwak():
    pass




if __name__ == "__main__":
    melt_file = "lexsubfr_semdis2014_test.id_melt"
    # melt_file = "melt_extract.id_melt"
    fred_rep = "../ressources/thesauri-1.0"

    melt_dico = parse_id_melt(melt_file)

    candidates_fredist = Fredist(fred_rep)
    candidates_fredist.__iter__()
    candidates_fredist.show_fred_stats()



