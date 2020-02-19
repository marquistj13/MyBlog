# -*- coding: utf-8 -*-
import yaml
from collections import defaultdict
from jinja2 import Template
import codecs  # enforce "utf-8" coding when reading files
import os



def dict_from_collection(collection):
    """
    This function is purely for debugging purpose, and is not used in this python script.

    extract a menu dict from the Jekyll yaml collection
    example input:  {'ReadingNotes_Book_NeuralNetworksAndDeepLearning': {'output': True,
    'permalink': '/ReadingNotes/Book_NeuralNetworksAndDeepLearning/:path'},
    'ReadingNotes_test': {'output': True, 'permalink': '/ReadingNotes/test/:path'}}
    example output: {'ReadingNotes': ['Book_NeuralNetworksAndDeepLearning', 'test']}
    """
    menus = defaultdict(list)
    menu_name_en = ""
    menu_iterm = ""
    for k, v in collection.items():
        menu_name_en = v['permalink'].split('/')[1]
        menu_iterm = v['permalink'].split('/')[2]
        menus[menu_name_en].append(menu_iterm)
    return menus


# menus=dict_from_collection(yold['collections'])
# print menus
def collections_from_dict(dic):
    """
    construct a Jekyll yaml collection (a dictionary) from a menu dict
    example input:  {'ReadingNotes': ['Book_NeuralNetworksAndDeepLearning', 'test']}
    example output:  {'ReadingNotes_Book_NeuralNetworksAndDeepLearning': {'output': True,
    'permalink': '/ReadingNotes/Book_NeuralNetworksAndDeepLearning/:path'},
    'ReadingNotes_test': {'output': True, 'permalink': '/ReadingNotes/test/:path'}}
    """
    collection = {}
    for k, v in dic.items():
        menu_name_en = k
        for collection_directory in v:
            menu_iterm = 'collection_' + menu_name_en + '_' + collection_directory
            permalink = '/{0}/{1}/:path'.format(menu_name_en, collection_directory)
            collection[menu_iterm] = {'output': True, 'permalink': permalink}
    return collection


# collection=collections_from_dict({'ReadingNotes': ['Book_NeuralNetworksAndDeepLearning', 'test']})
# print collection
def defaults_from_dict(dic):
    """
    construct a Jekyll yaml defaults （a list） from a menu dict
    example input:  {'ReadingNotes': ['Book_NeuralNetworksAndDeepLearning', 'test']}
    example output:  [{'scope': {'path': '', 'type': 'ReadingNotes_test'},  'values': {'layout': 'page'}},
                     {'scope': {'path': '',   'type': 'ReadingNotes_Book_NeuralNetworksAndDeepLearning'},
                      'values': {'layout': 'page'}}]
    """
    defaults = []
    for k, v in dic.items():
        menu_name_en = k
        for collection_directory in v:
            menu_iterm = 'collection_' + menu_name_en + '_' + collection_directory
            tmp_dict = eval("""{'scope': {'path': '', 'type': %s},'values': {'layout': 'page'}}""" % "menu_iterm")
            defaults.append(tmp_dict)
    return defaults


# defaults=defaults_from_dict({'ReadingNotes': ['Book_NeuralNetworksAndDeepLearning', 'test']})
def directories_from_dict(dic):
    pass


if __name__ == '__main__':
    # related files for setting up our blog menus
    yamlMenuFile = r"./menu_config.yml"
    yamlConfigFile = r"../_config.yml"
    yaml_template_ConfigFile = r"./template_config.yml"
    template_header_file = r"./template_header.html"
    template_index_file = r"./template_index.html"
    header_file = r"../_includes/header.html"

    # extract menus from menu_config.yml
    menu_config = yaml.safe_load(codecs.open(yamlMenuFile, 'r', encoding='utf8'))
    menus = menu_config['menus']
    # menus is a list of menu dictionaries:
    # [
    # {'menu_name_en': 'ReadingNotes', 'menu_name_cn': u'\u9605\u8bfb\u7b14\u8bb0',
    # 'menu_list': ['Book_NeuralNetworksAndDeepLearning', 'test']},
    # {'menu_name_en': 'ScholarThings', 'menu_name_cn': u'\u5b66\u672f\u79ef\u7d2f', 'menu_list': []}
    # ]
    # menus is essential in the following configureation.

    # construct the menus_dict to update collections in yamlConfigFile and also for other use.
    menus_dict = {}
    for menu in menus:
        menus_dict[menu['menu_name_en']] = menu['menu_list']

    print("/.....................The configuration process begins...................../")

    # update collections related configurations in yamlConfigFile, so Jekyll knows who are collections
    h_yamlConfigFile = yaml.safe_load(codecs.open(yaml_template_ConfigFile, 'r', encoding='utf8'))
    streamyamlConfigFile = codecs.open(yamlConfigFile, 'w', encoding='utf8')
    # note that the initial collections are overwritten, change the following two lines if you don't want this.
    h_yamlConfigFile['collections'] = collections_from_dict(menus_dict)
    h_yamlConfigFile['defaults'] = defaults_from_dict(menus_dict)
    yaml.dump(h_yamlConfigFile, streamyamlConfigFile, default_flow_style=False, allow_unicode=True)
    streamyamlConfigFile.close()
    print("File:(%s) is updated succefully!"%yamlConfigFile)

    # update header_file in the _includes directory, so the menus are shown in the header of our blog.
    h_template_header_file = codecs.open(template_header_file, "r", "utf-8")
    h_header_file = codecs.open(header_file, "w", "utf-8")
    jinja_template = Template(h_template_header_file.read())
    h_header_file.write(jinja_template.render(menus=menus))
    h_header_file.close()
    h_template_header_file.close()
    print("File:(%s) is updated succefully!"%header_file)

    # now create an index.html in the dictory of each collection.
    # if the directory does not exist, then create it and
    # place there an index.html, which lists the content of that directory.
    collection_iterm_path = ""
    for k, v in menus_dict.items():
        menu_name_en = k
        for collection_iterm_name in v:
            collection_name = 'collection_' + menu_name_en + '_' + collection_iterm_name
            collection_iterm_path = '../_collection_' + menu_name_en + '_' + collection_iterm_name
            try:
                os.makedirs(collection_iterm_path)
                h_template_index_file = codecs.open(template_index_file, "r", "utf-8")
                h_index_file = codecs.open(collection_iterm_path + '/index.html', "w", "utf-8")
                jinja_template = Template(h_template_index_file.read())
                h_index_file.write(
                    jinja_template.render(collection_iterm_name=collection_iterm_name, collection_name=collection_name))
                h_index_file.close()
                h_template_index_file.close()
                print("an index.html is generated in your new directory:(%s)"%collection_iterm_path)
            except OSError:  # the directory already exists or it's a file name
                if not os.path.isdir(collection_iterm_path):
                    raise  # it's a file name
                else:
                    h_template_index_file = codecs.open(template_index_file, "r", "utf-8")
                    h_index_file = codecs.open(collection_iterm_path + '/index.html', "w", "utf-8")
                    jinja_template = Template(h_template_index_file.read())
                    h_index_file.write(
                        jinja_template.render(collection_iterm_name=collection_iterm_name, collection_name=collection_name))
                    h_index_file.close()
                    h_template_index_file.close()
                    print("Dictory (%s) already exists. The index.html in it is overwritten!."%collection_iterm_path)
            pass
        pass       

    print("/.....................The configuration process ends...................../")
    print("Your menus are configured succefully! You can run: " \
          "jekyll serve -w to see the effects if you have configured jekyll locally" \
          "or you can simply push the changes to github pages to see the effects.")
    print("/.............................................................../")
