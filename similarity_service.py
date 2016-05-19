__author__ = 'talipov'
import os
import re
import cgi
import sys
from wsgiref.simple_server import make_server

# gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

# random shuffle
from random import shuffle

# numpy
import numpy as np
# pymongo

import pymongo
import bson

c = pymongo.MongoClient('localhost', 27017)
db = c.ooo

def get_document(doc_id):
    return db.question.find_one({'_id':bson.ObjectId(doc_id)})


def get_class(sim):
    if sim >0.6:
        return 'success'
    else:
        return 'danger'

class DemoApp:

    def __init__(self, test_mod = False):

        self.test_mod = test_mod # режим работы демона
        self.model = Doc2Vec.load('./document2vector_X.d2v')
        self.urls = [
            # ('^$', self.index),
            # ('^upload_tra$', self.upload_tra),
            # ('^upload_tst$', self.upload_tst),
            # ('^reset_model$', self.reset_model)
        ]

    def __call__(self, environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)

        doc_id = np.random.randint(self.model.docvecs.count)
        original_question = get_document(self.model.docvecs.index_to_doctag(doc_id))
        original = original_question.get('qtext')
        question_id = original_question.get('id')

        sims = '''<table class="table table-bordered">
        <tr>
        <th>Подобие</th>
        <th>Вопрос</th>
        </tr>
        %s</table>

        ''' % '\n'.join((
            '''
            <tr>
                <td  class="{row_class}">{sim}</td>
                <td>{q}</td>
            </tr>
            '''.format(
                sim=sim,
                q=get_document(_id).get('qtext'),
                row_class=get_class(sim),
                question_id = get_document(_id).get('id')
            )
            for _id, sim in self.model.docvecs.most_similar(doc_id, topn=100)
        ))

        with open('index_question_service.html', 'r') as template:
            yield template.read().format(original=original, question_id=question_id, sims=sims).encode('utf8')


if __name__ == '__main__':

    # if len(sys.argv) > 1 and sys.argv[1].lower() == 'test':
    #     test_mod = True
    #     mod = 'test'
    # else:
    #     test_mod = False
    #     mod = 'stage'

    httpd = make_server('', 8080, DemoApp())
    print("Serving on port 8080... Mod: %s" % 'gogo')
    httpd.serve_forever()
