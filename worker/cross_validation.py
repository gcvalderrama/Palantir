import os
import glob
import random
import shutil


def build_folds(source_folder_path, destination_folder_path):
    """
    Build folds
    :param source_folder_path: Source folder to fold
    :return: nothing
    """
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)
    attack_news = [c for c in glob.glob(source_folder_path + "/*.txt")
                   if os.path.basename(os.path.normpath(c)).startswith('attack--')]

    nonattack_news = [c for c in glob.glob(source_folder_path + "/*.txt")
                   if os.path.basename(os.path.normpath(c)).startswith('nonattack--')]

    total_attack_news = len(attack_news)
    total_nonattack_news = len(nonattack_news)

    print('Total Attacks ', total_attack_news)
    print('Total NonAttacks ', total_nonattack_news)

    '#take the minimum'

    total_news = total_nonattack_news if total_attack_news > total_nonattack_news else total_attack_news
    total_news = total_news - total_news % 10

    print('Total  ', total_news)
    attack_news = attack_news[:total_news]
    nonattack_news = nonattack_news[:total_news]

    random.shuffle(attack_news)
    random.shuffle(nonattack_news)



    period = int(total_news / 10)
    print('Test Size', period)
    dev_size = int( int(total_news - (period / 10)) / 10)
    print('Dev Size', dev_size)

    for i in range(10):
        current_folder_path = destination_folder_path + '/' + str(int(i % (total_news / 10)))
        current_folder_train_path = current_folder_path + '/train/'
        current_folder_dev_path = current_folder_path + '/dev/'
        current_folder_test_path = current_folder_path + '/test/'
        os.makedirs(current_folder_path)
        os.makedirs(current_folder_train_path)
        os.makedirs(current_folder_dev_path)
        os.makedirs(current_folder_test_path)

        tmp_attack = []
        tmp_nonattack = []

        for k in range(period):
            tmp_attack.append(attack_news[(i*10) + k])
            shutil.copy(attack_news[(i * 10) + k], current_folder_test_path)
            tmp_nonattack.append(nonattack_news[(i*10) + k])
            shutil.copy(nonattack_news[(i * 10) + k], current_folder_test_path)


        tmp_dev_attack = []
        tmp_dev_nonattack = []

        for file in attack_news:
            if file not in tmp_attack and len(tmp_dev_attack) < dev_size:
                shutil.copy(file, current_folder_dev_path)
                tmp_dev_attack.append(file)

        for file in nonattack_news:
            if file not in tmp_nonattack and len(tmp_dev_nonattack) < dev_size:
                shutil.copy(file, current_folder_dev_path)
                tmp_dev_nonattack.append(file)

        for file in attack_news:
            if file not in tmp_attack and file not in tmp_dev_attack:
                shutil.copy(file, current_folder_train_path)

        for file in nonattack_news:
            if file not in tmp_nonattack and file not in tmp_dev_nonattack:
                shutil.copy(file, current_folder_train_path)










