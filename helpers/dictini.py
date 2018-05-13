from collections import OrderedDict


def ini_to_dict(ini_file):
    with open(ini_file, 'r') as f:
        lines = [line.strip('\n') for line in f.readlines() if line]
    base_dict = OrderedDict()
    current_key = 'empty'
    for line in lines:
        if _line_is_key(line):
            current_key = line.replace('[', '').replace(']', '')
            base_dict[current_key] = OrderedDict()
        else:
            base_dict[current_key][line.split('=')[0]] = line.split('=')[1]
    return base_dict


def _line_is_key(line):
    if line.startswith('['):
        return True
    return False


def dict_to_ini(ini_di, outputfile):
    lines = []
    for di_name, di in ini_di.items():
        lines.append('[' + di_name + ']')
        for k, v in di.items():
            lines.append(k + '=' + v)
    with open(outputfile, 'w') as f:
        for line in lines:
            f.write(line + '\n')


def set_ini_param(ini_file, section, param, value):
    ini_di = ini_to_dict(ini_file)
    ini_di[section][param] = value
    dict_to_ini(ini_di, ini_file)


def get_ini_param(ini_file, section, param):
    ini_di = ini_to_dict(ini_file)
    return ini_di[section][param]


if __name__ == '__main__':
    # This is an acceptance test
    INI_FILE = './eqtitan/eqclient.ini'
    set_ini_param(INI_FILE, 'Defaults', 'StickFigures', '1')
