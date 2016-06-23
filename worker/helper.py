
import os
import glob


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