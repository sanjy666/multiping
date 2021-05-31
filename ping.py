import subprocess
import platform
import ipaddress
from multiprocessing import dummy


def ip_check(ip):
    """
    #validate ip
    return bool
    """
    try:
        ipv4 = ipaddress.ip_address(ip)
    except:
        return False
    else:
        if ipv4.is_global:
            return True


def ping(host):
    """Ping with syscall and detect OS
        spawn shell and parse stdout

    Args:
        host (string): host ip

    Returns:
        [string]: ping avg rounded to whole number
    """
    if platform.system().lower() == 'windows':
        ping_str = "ping " + "-n 3" + " " + str(host)
        try:
            shell_str = subprocess.check_output(
                ping_str, shell=True).decode('cp866')
        except:
            return 'n/a'
        else:
            # stdout string magic
            str_enc = str(shell_str.encode('utf8'))
            # find trigger and cut
            trigger_str = 'Average = '
            ms_str = str_enc[
                str_enc.find(trigger_str): str_enc.rfind('ms')
            ]
            ms = ms_str[
                ms_str.find('= ') + len('= '): len(ms_str)
            ]
            return ms
    else:
        ping_str = "ping " + "-c 3" + " " + str(host)
        try:
            shell_str = subprocess.check_output(
                ping_str, shell=True).decode('cp866')
        except:
            return 'n/a'
        else:
            # stdout string magic
            str_enc = str(shell_str.encode('utf8'))
            # find trigger and cut
            trigger_str = 'avg/max'
            ms_str = str_enc[str_enc.find(trigger_str): str_enc.rfind('ms')]
            # cut str
            ms_str = str_enc[
                str_enc.find('= ') + len('= '): str_enc.rfind('ms') - 1
            ]
            # split result
            ms = ms_str.split('/')
            return str(int(float(ms[1])))


def ping_worker(host):
    """ping worker

    Args:
        host (single value list): aka [8.8.8.8]

    Returns:
        single value list : [90] or ['n/a'] or ['invalid IP'] if host empty, return empty list
    """
    if host:
        if ip_check(host[0]):
            response = ping(host[0])
            if response:
                return [response]
            else:
                return ['n/a']
        else:
            return ['invalid IP']
    else:
        return ['']


def ping_pool(hosts, num_threads):
    """spawn pool ping worker

    Args:
        hosts (list): list of lists [[123.123.123.123], [123.123.123.123]]
        num_threads (int): number of parallel ping

    Returns:
        [list]: list of lists [[32], ['n/a'], ['invalid ip'], [], [11]]
    """
    p = dummy.Pool(int(num_threads))
    results = p.map(ping_worker, hosts)
    p.close()
    return results
