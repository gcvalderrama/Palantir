
import os
import glob
import random
import shutil


class Helper:
    def clean_file_name(self, source_folder, extension='txt'):
        """
        Rename files
        :param source_folder:
        :param extension:
        :return:
        """
        news = glob.glob(source_folder + "/*." + extension)
        for news_file in news:
            if "?ref_bajada" in news_file:
                updated_news_file = news_file.replace('?ref_bajada', '')
                os.rename(news_file, updated_news_file)

    def remove_first_line(self, source_folder, extension):
        """
        Removes first line of text
        :param source_folder:
        :param extension:
        :return:
        """
        files = glob.glob(source_folder + '/*.' + extension)
        for file in files:
            with open(file, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(file, 'w') as fout:
                fout.writelines(data[1:])

    def rename_files(self, folder):
        """
        Read all html files from folder, and clean character '?ref_bajada' from title
        :param folder: Source folder
        :return: void - nothing
        """
        news = glob.glob(folder + "/*.html")
        for news_file in news:
            if "?ref_bajada" in news_file:
                updated_news_file = news_file.replace('?ref_bajada', '')
                os.rename(news_file, updated_news_file)
                news_file = updated_news_file

            if news_file.startswith(folder + "/actualidad--") \
                    or news_file.startswith(folder + "/gastronomia--") \
                    or news_file.startswith(folder + "/policiales--") \
                    or news_file.startswith(folder + "/tecnologia--"):
                continue
            os.rename(news_file, news_file.replace(folder + "/", folder + "/policiales--"))

    def distribute_files(self, source_folder, destination_folders, split_category, extension='txt'):
        news = glob.glob(source_folder + "/*." + extension)
        news.sort()
        first_category = []
        second_category = []
        for item in news:
            if split_category in item:
                first_category.append(item)
            else:
                second_category.append(item)

        start_index = 0
        random.shuffle(first_category)
        random.shuffle(second_category)

        for folder, number_items in destination_folders.items():
            if not os.path.exists(folder):
                os.makedirs(folder)

            end_index = start_index + number_items
            first_category_segment = first_category[start_index:end_index]
            for news_file in first_category_segment:
                shutil.copy2(news_file, folder)

            second_category_segment = second_category[start_index:end_index]
            for news_file in second_category_segment:
                shutil.copy2(news_file, folder)

            start_index = end_index + 1
