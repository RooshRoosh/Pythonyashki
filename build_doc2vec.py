__author__ = 'talipov'

__author__ = 'talipov'

import pymongo

c = pymongo.MongoClient('localhost', 27017)
db = c.ooo

# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# shuffle
from random import shuffle

# logging
import logging
import os.path
import sys

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))


import re

def prepare_document(source):
    return re.sub('[^А-Яа-яЕё ]', ' ', source['qtext']+'\n'+source['qcomment']).lower()


class LabeledLineSentence(object):

    def __iter__(self):
        for source in db.question.find():
            if not source.get('qtext'):
                continue
            yield LabeledSentence(utils.to_unicode(source['qtext']+'\n'+source['qcomment']).split(), [str(source['_id'])])


sentences = LabeledLineSentence()

model = Doc2Vec(min_count=3, window=10, size=200, sample=1e-4, negative=5, workers=7)
model.build_vocab(sentences)

for epoch in range(50):
    logger.info('Epoch %d' % epoch)
    model.train(sentences)
    model.save('./document2vector_'+str(epoch)+'.d2v')