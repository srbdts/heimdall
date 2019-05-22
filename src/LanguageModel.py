import os

from config import RESOURCEDIR

class LanguageModel:
    def __init__(self,language,status,normalize):
        self.normalize = normalize
        self.language = language
        self.probsfile = os.path.join("resources/",language+".logprobs")
        self.status = status
        self.load()

    def load(self):
        prob_data = open(self.probsfile,"r",encoding="utf-8")
        self.probs = {trigram.split("\t")[0]:float(trigram.split("\t")[2]) for trigram in prob_data.readlines()}

    def get_local_prob(self,trigram):
        local_prob = 0
        if trigram in self.probs:
            return self.probs[trigram]
        else:
            return self.probs["UNKNOWN"]

    def calculate_probs(self,word):

        return

