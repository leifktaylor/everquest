import os
import sys
import time

from jinja2 import Environment, FileSystemLoader

from helpers import dictini
from helpers.ymlhelpers import load_yaml

settings = load_yaml('./pyeq_settings.yml')
EQ_DIR = settings['eq_dir']
MQ2_DIR = settings['mq_dir']
WIN_EVERQUEST_DIR = settings['win_eq_dir']
WIN_MQ_DIR = settings['win_mq_dir']


def load_character_list(character_file):
    with open(character_file, 'r') as f:
        lines = [line.strip('\r\n') for line in f.readlines()]
    return [{'name': line.split()[0], 'account': line.split()[1], 'password': line.split()[2]} for line in lines]


# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def output_autologin_ini(character_data):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    server_number = get_last_server_number()
    return j2_env.get_template('./pyeq_settings/templates/eqtitan_autologin.j2').render(characters=character_data,
                                                                                        server_number=server_number)


def generate_mq2autologin_ini(session_name):
    character_list = load_character_list('./pyeq_settings/characters.txt')
    sessions = load_yaml('./pyeq_settings/sessions.yml')

    used_characters = []
    try:
        for char_name in sessions[session_name]:
            for character in character_list:
                if char_name.lower() == character['name'].lower():
                    used_characters.append(character)
                    break
    except TypeError:
        pass

    jinja2_data = output_autologin_ini(used_characters)
    with open(MQ2_DIR + 'MQ2AutoLogin.ini', 'w') as f:
        f.write(jinja2_data)
    return used_characters


def clear_mq2autologin_ini():
    jinja2_data = output_autologin_ini([])
    with open(MQ2_DIR + 'MQ2AutoLogin.ini', 'w') as f:
        f.write(jinja2_data)


def execute_macroquest_and_server(win_mq_dir):
    # Start server, macro quest, and clients
    os.system('START {0}"eqbcs2a.exe"'.format(win_mq_dir))
    time.sleep(1)
    os.system('START {0}"MacroQuest2.exe"'.format(win_mq_dir))
    time.sleep(1)


def execute_everquest_client(eq_dir, delay=14):
    os.system('START {0}EQTitan.lnk'.format(eq_dir))
    time.sleep(delay)


def load_playerdata_ini():
    with open('{0}eqlsPlayerData.ini'.format(EQ_DIR), 'r') as f:
        lines = [line.strip('\n') for line in f.readlines()]
    return lines


def get_item_from_eqlsplayerdata(item):
    for line in load_playerdata_ini():
        if line.startswith(item):
            return line.split('=')[1]
    raise RuntimeError('Could not find {0} in eqlsPlayerData.ini'.format(item))


def get_last_server_number():
    return get_item_from_eqlsplayerdata('LastServerID')


def get_last_account_logged():
    return get_item_from_eqlsplayerdata('Username')


def get_last_server_name():
    return get_item_from_eqlsplayerdata('LastServerName')


if __name__ == '__main__':
    args = sys.argv[1:]

    # Attempt to generate MQ2AutoLogin.ini from sessions.yml, then open EQ Clients.
    try:
        session = args[0]
        if session == '-h':
            print('Last account used: {0}'.format(get_last_account_logged()))
            print('Last server number: {0}'.format(get_last_server_number()))
            print('Last server name: {0}'.format(get_last_server_name()))
        else:
            used_characters = generate_mq2autologin_ini(session)
            execute_macroquest_and_server(WIN_MQ_DIR)
            dictini.set_ini_param(EQ_DIR + 'eqclient.ini', 'Defaults', 'StickFigures', '0')
            execute_everquest_client(WIN_EVERQUEST_DIR)
            time.sleep(25)
            dictini.set_ini_param(EQ_DIR + 'eqclient.ini', 'Defaults', 'StickFigures', '1')
            for character in used_characters[1:]:
                execute_everquest_client(WIN_EVERQUEST_DIR)

    # If launched from command line with no arguments, just open EQ regularly
    except IndexError:
        clear_mq2autologin_ini()
        execute_everquest_client(WIN_EVERQUEST_DIR)


