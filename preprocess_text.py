'''
    Для построения word embedding предварительно необходимо:
    1.	Удалить из текста все изображения и HTML теги.
    2.	Удалить все знаки препинания и отделить их от других слов.
    3.	Удалить слова длинной выше 20 символов.
    4.	Присоединить НЕ к следующему слову.
    5.	Привести все слова в верхний регистр (либо все в нижний).
    6.	Заменить все функциональные слова такие как URL-адреса IP-адреса числа больше 9 (их так же можно приводить к различным классам эквивалентности от 10 до 99, от 100 до 999 и так далее) на служебные маркеры, например <URL>, <IP-address>, <10-99>, <100-999>
    7.	Заменить знаки денежных обозначений на соответствующие слова, например «5$» надо представить в виде «5 долларов»
    8.	Удалить из корпуса текстов все статьи содержащие менее 80% слов используемых в анализируемом языке. Это позволяет отсечь статьи на иностранных языках, а так же статьи состоящих главным образом из программного кода.
    9.	Удалить из корпуса все статьи дубликаты. Это можно сделать вычислив 128-битных хеш от контента каждой статьи. Статьи и одинаковыми хешами считаются одинаковыми.
    10.	 Произвести автоматическое исправление ошибок и опечаток в текстах
    11.	 Разделить дефисные или соединить разделённые слова, для которых нет записей в словаре, но для компонент которого эти записи есть.
'''


__author__ = 'talipov'

import re
from string import punctuation

number_group = {
    (0, 1): 'LESS_ONE',
    (1, 3): '1_->_3',
    (3, 5): '3_->_5',
    (5, 10): '5_->_10',
    (10, 20): '10_->_20',
    (20, 50): '10_->_20',
    (50, 100): '50_->_100',
    (100, 250): '100_->_250',
    (250, 500): '250_->_500',
    (500, 1000): '500_->_1000',
    (1000, 9223372036854775807): '1000_->_max',
}


def clear_text(raw_text):
    minus_html_regexp = re.compile('(<[^>]+>?)')
    minus_punctuation = re.compile(r'[!\?,\.\\:;~\+\*={}\^_`\|\$]', re.UNICODE)
    minus_http = re.compile('https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    text = re.sub(minus_http, ' URL ', raw_text)
    text = re.sub(minus_html_regexp, ' ', text)
    text = re.sub(minus_punctuation, ' ', text)


    text = text.upper().split()

    i = 0
    _text = []
    text_append = _text.append
    while i<len(text):
        word = text[i]
        if word.isdigit():
            word_digit = int(word)
            for key in number_group.keys():
                if key[0] < word_digit <= key[1]:
                    word = number_group[key]
                    break

        elif word == 'НЕ':
            word = word+'_'+text[i+1]
            i += 1

        elif len(word) >= 18:
            word = 'LONG_WORD'

        i+=1
        text_append(word)

    return _text

def text_to_sentence(raw_text):
    # Разбиваем текст на предложения
    def gen_sentence(text):
        i=0
        while i<len(text):
            if text[i] in ('.', '!', '?') and (text[i+1] in [' ','\n'] or text[i]==text[-1]) and (text[i-1]!='/'):
                yield text[:i+1]
                text = text[i+1:]
                i = 0
            i+=1
        yield text

    minus_html_regexp = re.compile('(<[^>]+>?)')
    minus_punctuation = re.compile(r'[!\/\?,\.\\:;\~\+\*={}\^_`\|\$]', re.UNICODE)
    minus_http = re.compile('https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    for text in gen_sentence(raw_text):
        text = re.sub(minus_http, ' URL ', text)
        text = re.sub(minus_html_regexp, ' ', text)
        text = re.sub(minus_punctuation, ' ', text)


        text = text.upper().split()

        i = 0
        _text = []
        text_append = _text.append
        while i<len(text):
            word = text[i]
            if word.isdigit():
                word_digit = int(word)
                for key in number_group.keys():
                    if key[0] < word_digit <= key[1]:
                        word = number_group[key]
                        break

            elif word == 'НЕ':
                word = word+'_'+text[i+1]
                i += 1

            elif len(word) >= 18:
                word = 'LONG_WORD'

            i+=1
            text_append(word)

        if _text:
            yield _text

if __name__ == "__main__":
    t = 'занимаюсь изготовлением и продажей чипсов! '+\
    'был момент когда чипсы получались идеальные! '+\
    'хрустящие золотистые!!!картофельзакончился,' +\
    'купил в том же месте 1 !?? 90-100 но чипсы уже не те! '+\
    'то мягкие , то теряют :форму! в общем проблема! '+\
    'вот тут http://youtube.com/? всё показано. ' +\
    'нужно её решить! думаю ;что дело в картофеле! '+\
    '\nпомогите, если 12 знаете ~как!?{?}'
    print([i for i in text_to_sentence(t)])

    print(clear_text(t))
