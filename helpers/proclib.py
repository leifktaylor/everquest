import subprocess
from collections import namedtuple


Proc = namedtuple('process', ['name', 'pid'])


class ProcLib(object):

    @staticmethod
    def cmd(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out, err

    def get_processes(self):
        out, err = self.cmd('tasklist /nh /fo csv')
        lines = [item for item in out.split('\r\n') if item]
        procs = []
        for line in lines:
            name = line.split(',')[0].replace('"', '')
            pid = int(line.split(',')[1].replace('"', ''))
            procs.append(Proc(name, pid))
        return procs

    def kill_process_by_pid(self, pid):
        return self.cmd('taskkill /PID {0} /F'.format(pid))

    def kill_process_by_name(self, name):
        return self.cmd('taskkill /IM {0} /F'.format(name))


if __name__ == '__main__':
    a = ProcLib()
    print(a.get_processes())
