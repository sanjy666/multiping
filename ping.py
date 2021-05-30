import ipaddress
from multiprocessing import dummy
from pythonping import ping

def ip_check(ip):
    try:
        ipv4 = ipaddress.ip_address(ip)
    except:
        return False
    else:
        if ipv4.is_global:
            return True


def ping_worker(host):
    if host:
        if ip_check(host[0]):
            # TODO replase non privileged realisation
            response = ping(host[0], size=32, count=4, verbose=False)
            if response.success(option=3):
                return [int(response.rtt_avg_ms)]
            else:
                return ['n/a']
        else:
            return ['invalid IP']
    else:
        return ['']


def ping_pool(hosts, num_threads):
    p = dummy.Pool(num_threads)
    results = p.map(ping_worker, hosts)
    return results