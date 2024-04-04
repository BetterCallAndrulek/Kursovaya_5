from configparser import ConfigParser
import codecs


def config(filename=r"C:\Users\ddemo\PycharmProjects\pythonProject11\database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename, encoding='utf-8')
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db