import configparser


def get_information():
    config = configparser.ConfigParser()

    # lets create that config file for next time...
    cfgfile = open("config.ini", 'w')

    # add the settings to the structure of the file, and lets write it out...
    config.add_section('chromedriver')
    config.set('chromedriver', 'url', '/Users/ozo/ExternalDemo/chromedriver')
    config.write(cfgfile)
    cfgfile.close()


get_information()
