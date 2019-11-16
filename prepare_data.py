# -*- coding: utf-8 -*
# prepare_data.py

from translate import Translator
from cdqa.utils.converters import pdf_converter
import csv
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
        for row in rows:
            tmp_list = []
            for i in range(0, len(row)):
                print (str(i) + ": ", row[i])
                translator= Translator(to_lang="chinese")
                translation = translator.translate(row[i])
                print (translation)
            #print(row)
            print ("\n")
            print ("length: ", len(row))
            count += 1
            if (count > 1):
                break



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
    readcsv('./it.csv')
    print ("\n")
    #print ("the data is: ", data)