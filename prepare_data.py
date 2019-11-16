# -*- coding: utf-8 -*
# prepare_data.py

from translate import Translator
from cdqa.utils.converters import pdf_converter
import csv
import jieba
import jieba.posseg as pseg
import nltk


#data type
#date,title,category,link,abstract,paragraphs
#['date', 'title', 'category', 'link', 'abstract', 'paragraphs']

def read_origin(number):
    number = int(number)
    count = 0
    with open('./path-to-directory/bnpp_newsroom-v1.1.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            print(row)
            print ("\n")
            count += 1
            if (count < number):
                pass
            else:
                return (row)
                break

def writefirstline():
    with open('csvdata.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        first_line =  ['date', 'title', 'category', 'link', 'abstract', 'paragraphs']
        writer.writerow(first_line)

def writedata():
    with open('csvdata.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # ['date', 'title', 'category', 'link', 'abstract', 'paragraphs']
        writer.writerow(['姓名', '身高', '體重'])

#df = pdf_converter(directory_path='path_to_pdf_folder')

def readcsv(file):
    #number = int(number)
    count = 0
    with open(file, newline='') as csvfile:
        rows = csv.reader(csvfile)
        total_tmp_list = []
        for row in rows:
            #total_tmp_list.append(row)
            tmp_list = []
            tmp_list.append(row)
            sentence = row[0]
            hightlight = row[1]
            position = sentence.find(hightlight)
            tmp_list.append(position)
            total_tmp_list.append(tmp_list)
            for i in range(0, len(row)):
                print (str(i) + ": ", row[i])
                #sentence = row[i]
                tmp_list = row[i].split(" ")
                print (tmp_list)
                """
                translator= Translator(to_lang="chinese")
                translation = translator.translate(row[i])
                print (translation)
                """
            #print(row)
            print ("\n")
            #print ("length: ", len(row))
            count += 1
            if (count > 1):
                print ("total: ", total_tmp_list)
                print ("len(total): ", len(total_tmp_list))
                print ("len(total[0]): ", len(total_tmp_list[0]))
                return (total_tmp_list)
                break

def processing(total_list):
    sentence_list = []
    translate_list = []
    for i in range(0, len(total_list)):
        position = total_list[i][1]
        dev_position = len(total_list[i][0][1])
        tmp_sentence = total_list[i][0][0][:(position+dev_position+1)]
        sentence_list.append(tmp_sentence)
        #translator = Translator(to_lang="chinese")
        #translation = translator.translate(tmp_sentence)
        #translate_list.append(translation)
    return (sentence_list)
    #return (sentence_list, translate_list)

def segmentation(sentence):
    words = pseg.cut(sentence)
    return_word=''

    for w in words:
        w = str(w)
        pair = w.split("/")
        print (pair)
        return_word = return_word+','+str(w)
    return return_word
    #seg_list = pseg.cut(str(sentence))
    #print(" , ".join(seg_list))

def label(sentence):
    #nltk.download()
    text=nltk.word_tokenize(sentence)
    result = nltk.pos_tag(text)
    print (result)
"""
# 以下是将简单句子从英语翻译中文
translator= Translator(to_lang="chinese")
translation = translator.translate("Good night!")
print (translation)


# 在任何两种语言之间，中文翻译成英文
translator= Translator(from_lang="chinese",to_lang="english")
translation = translator.translate("我想你")
print (translation)
"""

if __name__ == "__main__":
    #data = read_origin(3)
    #readcsv('./nengo_data.csv')
    total_list = readcsv('./it.csv')
    sentence_list = processing(total_list)
    print ("sentence: ", sentence_list)
    #print ("translate: ", translate_list)
    print ("\n")
    #words = segmentation(translate_list[0])
    #chinese_sentence = "虽然这给生活在南方的古代玛雅人带来了困难，\
    #                    但也让现代考古学家们难以理解为什么古代干旱在潮湿的南方比在干燥的北方造成更大的问题。\
    #                    可能的解释"
    #words = segmentation(chinese_sentence)
    #print ("words: ", words)
    label(sentence_list[0])

