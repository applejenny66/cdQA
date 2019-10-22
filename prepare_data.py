# -*- coding: utf-8 -*
# prepare_data.py

from cdqa.utils.converters import pdf_converter
import csv
#data type
#date,title,category,link,abstract,paragraphs

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


if __name__ == "__main__":
    data = read_origin(10)
    print ("\n")
    print ("the data is: ", data)