import sys
import os

def obtain_cap():
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

    anotator_attack_diff = 0
    for file in corpus_anotator_00_attack:
        if file not in corpus_anotator_01_attack:
            anotator_attack_diff += 1
    print("00 anotator attack diff {}".format(anotator_attack_diff))

    anotator01_attack_diff = 0
    for file in corpus_anotator_01_attack:
        if file not in corpus_anotator_00_attack:
            anotator01_attack_diff += 1
    print("01 anotator attack diff {}".format(anotator01_attack_diff))

    anotator_nonattack_diff = 0
    for file in corpus_anotator_00_nonattack:
        if file not in corpus_anotator_01_nonattack:
            anotator_nonattack_diff += 1
    print("00 anotator nonattack diff {}".format(anotator_nonattack_diff))

    anotator01_nonattack_diff = 0
    for file in corpus_anotator_01_nonattack:
        if file not in corpus_anotator_00_nonattack:
            anotator01_nonattack_diff += 1
    print("01 anotator attack diff {}".format(anotator01_nonattack_diff))

if __name__ == "__main__":
    print('test')
