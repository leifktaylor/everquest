from jinja2 import Environment, FileSystemLoader
import os
import yaml
import sys
import time


MQ2_DIR = './Killians\' MQ2/'
EVERQUEST_DIR = ''
EQ_SHORTCUT_PATH = ''
# To get last server number: eqlsPlayerData.ini


def load_character_list(character_file):
    with open(character_file, 'r') as f:
        lines = [line.strip('\r\n') for line in f.readlines()]
    return [{'name': line.split()[0], 'account': line.split()[1], 'password': line.split()[2]} for line in lines]


# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def output_autologin_ini(character_data):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    server_number = get_last_server_number()
    return j2_env.get_template('eqtitan_autologin.j2').render(characters=character_data, server_number=server_number)


def load_yaml(filename):
    return yaml.load(open(filename))


def generate_mq2autologin_ini(session_name):
    # used_characters = filter_character_list_with_session(session, 'characters.txt')
    character_list = load_character_list('characters.txt')
    sessions = load_yaml('sessions.yml')

    used_characters = []
    for char_name in sessions[session_name]:
        for character in character_list:
            if char_name.lower() == character['name'].lower():
                used_characters.append(character)
                break

    jinja2_data = output_autologin_ini(used_characters)
    with open(MQ2_DIR + 'MQ2AutoLogin.ini', 'w') as f:
        f.write(jinja2_data)
    return used_characters


def clear_mq2autologin_ini():
    jinja2_data = output_autologin_ini([])
    with open(MQ2_DIR + 'MQ2AutoLogin.ini', 'w') as f:
        f.write(jinja2_data)


def execute_macroquest_and_server():
    # Start server, macro quest, and clients
    os.system('START C:\\"Everquest"\\"Killians\' MQ2"\\"eqbcs2a.exe"')
    time.sleep(1)
    os.system('START C:\\"Everquest"\\"Killians\' MQ2"\\"MacroQuest2.exe"')
    time.sleep(1)


def execute_everquest_client(delay=18):
    os.system('START C:\\"Users"\\"Andrew"\\"Desktop"\\"Programs"\\"Games"\\"MMO"\\"EQ Titan"\\EQTitan.lnk')
    time.sleep(delay)


def load_playerdata_ini():
    with open('C:\\Users\\Andrew\\Desktop\\Programs\\Games\\MMO\\EQ Titan\\eqlsPlayerData.ini', 'r') as f:
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

    try:
        session = args[0]
        if session == '-h':
            print('Last account used: {0}'.format(get_last_account_logged()))
            print('Last server number: {0}'.format(get_last_server_number()))
            print('Last server name: {0}'.format(get_last_server_name()))
        else:
            used_characters = generate_mq2autologin_ini(session)
            execute_macroquest_and_server()
            for character in used_characters:
                execute_everquest_client()
    except IndexError:
        clear_mq2autologin_ini()
        execute_everquest_client()


