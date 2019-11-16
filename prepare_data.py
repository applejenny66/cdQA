# -*- coding: utf-8 -*
# prepare_data.py

from translate import Translator
from cdqa.utils.converters import pdf_converter
import csv
import jieba
import jieba.posseg as pseg
import nltk
import matplotlib.pyplot as plt

import nengo
import nengo_spa as spa

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
    #print (type(result))
    #print (result[0])
    print (result)
    type_list = []
    word_list = []
    verb_list = []
    word_n = "N"
    word_v = "V"
    word_j = "J"
    word_in = "IN"
    for i in range(0, len(result)):
        tmp_type = result[i][1]
        if (tmp_type not in type_list):
            type_list.append(tmp_type)
        if (tmp_type.find(word_n) != -1 and (tmp_type.find(word_in) == -1) and \
            (tmp_type.find(word_v) == -1)):
            word_list.append(result[i][0])
        if (tmp_type.find(word_v) != -1):
            verb_list.append(result[i][0])
    print ("total type of list: ", type_list)
    print ("N word: ", word_list)
    print ("\n")
    print ("V word: ", verb_list)
    print ("\n")
    tidy_result = []
    tidy_label_result = []
    for i in range(0, len(result)):
        tmp_type = result[i][1]
        tmp_label_list = []
        if ((tmp_type.find(word_n) != -1) or (tmp_type.find(word_v) != -1) or\
            (tmp_type.find(word_in) != -1) or (tmp_type.find(word_j) != -1) or\
            (tmp_type.find(",") != -1) or (tmp_type.find(".") != -1)):
            tidy_result.append(result[i][0])
            if (tmp_type.find(word_n) != -1):
                tmp_label = "N"
            elif (tmp_type.find(word_v) != -1):
                tmp_label = "V"
            elif (tmp_type.find(word_in) != -1):
                tmp_label = "IN"
            elif (tmp_type.find(word_j) != -1):
                tmp_label = "J"
            else:
                tmp_label = result[i][1]
            tmp_label_list.append(result[i][0])
            tmp_label_list.append(tmp_label)
            tidy_label_result.append(tmp_label_list)
    print ("tidy result: ", tidy_result)
    print ("tidy label rsult: ", tidy_label_result)

    return (word_list, verb_list, tidy_result, tidy_label_result)




def nengo_cog(sequence, label_sequence):
    def input_vision(t):
        index = int(t / 0.5) % len(sequence)
        return sequence[index]
    #sequence = 'WRITE ONE NONE WRITE TWO NONE THREE WRITE NONE'.split()
    # Number of dimensions for the SPs
    n_list = []
    v_list = []
    in_list = []
    j_list = []
    len_seq = len(sequence)
    for i in range(0, len_seq):
        if (label_sequence[i][1] == "N"):
            n_list.append(i)
        elif (label_sequence[i][1] == "V"):
            v_list.append(i)
        elif (label_sequence[i][1] == "IN"):
            in_list.append(i)
        elif (label_sequence[i][1] == "J"):
            j_list.append(i)
    dimensions = 64
    # Make a model object with the SPA network
    model = spa.Network(label='Parser sentence')
    n_per_dim = 100

    with model:
        # Specify the modules to be used
        vision = spa.Transcode(input_vision, output_vocab=dimensions)
        phrase = spa.State(dimensions, neurons_per_dimension=n_per_dim)
        motor = spa.State(dimensions, neurons_per_dimension=n_per_dim)
        noun = spa.State(dimensions, feedback=1., neurons_per_dimension=n_per_dim)
        verb = spa.State(dimensions, feedback=1., neurons_per_dimension=n_per_dim)
        print ("type spa.sym.NOUN: ", type(spa.sym.NOUN))
        # Specify the action mapping
        for i in range(0, len(n_list)):
            n_index = n_list[i]
            NT = sequence[n_index].upper()
            #print (NT)
            #print (spa.sym.VERB)
            #spa.sym.NT = PointerSymbol('NT', _TAnyVocab('TAnyNT'))

            spa.sym.NN = spa.sym.NN + spa.sym.NT
        for i in range(0, len(v_list)):
            v_index = v_list[i]
            VT = sequence[v_index].upper()
            spa.sym.VB = spa.sym.VB + VT
        for i in range(0, len(in_list)):
            in_index = in_list[i]
            IT = sequence[in_index].upper()
            spa.sym.IN = spa.sym.IN + IT
        for i in range(0, len(j_list)):
            j_index = j_list[i]
            JT = sequence[j_index].upper()
            
            spa.sym.J = spa.sym.J + JT
        none_vision_cond = spa.dot(
            spa.sym.NONE - spa.sym.VB - spa.sym.IN - spa.sym.J,
            vision)
        num_vision_cond = spa.dot(vision, spa.sym.IN + spa.sym.J)

        with spa.ActionSelection() as action_sel:
            spa.ifmax("Write vis", spa.dot(vision, spa.sym.VB),
                vision >> verb)
            spa.ifmax("Memorize", num_vision_cond,
                vision >> noun)
            spa.ifmax(
                "Write mem",
                0.5 * (none_vision_cond + spa.dot(phrase, spa.sym.VB * spa.sym.VERB)),
                phrase * ~spa.sym.NOUN >> motor)

        noun * spa.sym.NOUN + verb * spa.sym.VERB >> phrase

    with model:
        p_vision = nengo.Probe(vision.output, synapse=0.03)
        p_phrase = nengo.Probe(phrase.output, synapse=0.03)
        p_motor = nengo.Probe(motor.output, synapse=0.03)
        p_noun = nengo.Probe(noun.output, synapse=0.03)
        p_verb = nengo.Probe(verb.output, synapse=0.03)
        p_selected_actions = nengo.Probe(action_sel.thalamus.output, synapse=0.01)
        p_utility = nengo.Probe(action_sel.bg.input, synapse=0.01)

    with nengo.Simulator(model) as sim:
        sim.run(4.5)

    vocab = model.vocabs[dimensions]

    fig, ax = plt.subplots(7, 1, sharex=True, figsize=(16,12))

    ax[0].plot(sim.trange(), spa.similarity(sim.data[p_vision], vocab))
    ax[0].set_ylabel('Vision')

    ax[1].plot(sim.trange(), spa.similarity(sim.data[p_phrase], vocab))
    ax[1].set_ylabel('Phrase')

    ax[2].plot(sim.trange(), spa.similarity(sim.data[p_motor], vocab))
    ax[2].legend(vocab.keys(), loc='right', bbox_to_anchor=(1.11, 0.5))
    ax[2].set_ylabel('Motor')

    ax[3].plot(sim.trange(), spa.similarity(sim.data[p_noun], vocab))
    ax[3].set_ylabel('Noun')

    ax[4].plot(sim.trange(), spa.similarity(sim.data[p_verb], vocab))
    ax[4].set_ylabel('Verb')

    ax[5].plot(sim.trange(), sim.data[p_utility])
    ax[5].legend(tuple(action_sel.keys()), loc='right', bbox_to_anchor=(1.13, -0.1))
    ax[5].set_ylabel('Utility')

    ax[6].plot(sim.trange(), sim.data[p_selected_actions])
    ax[6].set_ylabel('Selected Action')
    plt.show()

"""
# 以下是将简单句子从英语翻译中文
translator= Translator(to_lang="chinese")
translation = translator.translate("Good night!")
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
    word_list, verb_list, tidy_result, tidy_label_result = label(sentence_list[1])
    nengo_cog(tidy_result, tidy_label_result)
    #tidy_sentence = ""
    #for i in range(0, len(tidy_result)):
    #    tidy_sentence += tidy_result[i]
    #    tidy_sentence += " "
    #print ("tidy sentence: ", tidy_sentence)
    
    sequence = tidy_result
    #print (type(sequence))
    #print (sequence)
    
    