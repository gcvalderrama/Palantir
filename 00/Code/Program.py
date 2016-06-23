import sys
import os

if __name__ == "__main__":
    corpus_anotator_00 = "./../anotador_00"
    corpus_anotator_01 = "./../anotador_01"

    corpus_anotator_00_attack = []
    corpus_anotator_00_nonattack = []
    corpus_anotator_01_attack = []
    corpus_anotator_01_nonattack = []

    for file in os.listdir(corpus_anotator_00):
        if file.startswith("attack--"):
            nfile = file.replace("attack--", "")
            corpus_anotator_00_attack.append(nfile)
        else:
            nfile = file.replace("nonattack--", "")
            corpus_anotator_00_nonattack.append(nfile)
    for file in os.listdir(corpus_anotator_01):
        if file.startswith("attack--"):
            nfile = file.replace("attack--", "")
            corpus_anotator_01_attack.append(nfile)
        else:
            nfile = file.replace("nonattack--", "")
            corpus_anotator_01_nonattack.append(nfile)

    print("00 anotator attack {}".format(len(corpus_anotator_00_attack)))
    print("00 anotator nonattack {}".format(len(corpus_anotator_00_nonattack)))
    print("01 anotator attack {}".format(len(corpus_anotator_01_attack)))
    print("01 anotator nonattack {}".format(len(corpus_anotator_01_nonattack)))

    for file in corpus_anotator_00_attack:
        if file not in corpus_anotator_01_attack:
            print(file)
