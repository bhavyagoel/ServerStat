import psutil
import json
import platform
from time import sleep
import matplotlib.pyplot as plt
import os


def cpu_usage(**kwargs):
    """
    Returns the CPU usage in percent.
    """
    data = {}
    data['cpu_percent'] = psutil.cpu_percent(interval=1)
    data['cpu_times'] = psutil.cpu_times()
    data['cpu_times_percent'] = psutil.cpu_times_percent()
    data['cpu_count'] = psutil.cpu_count()
    data['cpu_stats'] = psutil.cpu_stats()
    data['cpu_freq'] = psutil.cpu_freq()

    data['percpu'] = psutil.cpu_percent(percpu=True)
    data['percpu_percent'] = psutil.cpu_times_percent(percpu=True)
    data['percpu_times'] = psutil.cpu_times(percpu=True)
    data['percpu_freq'] = psutil.cpu_freq(percpu=True)

    return data


def memory_usage(**kwargs):
    """
    Returns the memory usage in percent.
    """
    data = {}
    data['virtual_memory'] = psutil.virtual_memory()
    data['virtual_memory_free'] = psutil.virtual_memory().free
    data['virtual_memory_used'] = psutil.virtual_memory().used
    data['virtual_memory_total'] = psutil.virtual_memory().total
    data['virtual_memory_percent'] = psutil.virtual_memory().percent

    data['swap_memory'] = psutil.swap_memory()
    data['swap_memory_free'] = psutil.swap_memory().free
    data['swap_memory_used'] = psutil.swap_memory().used
    data['swap_memory_total'] = psutil.swap_memory().total
    data['swap_memory_percent'] = psutil.swap_memory().percent
    return data


def disk_usage(**kwargs):
    """
    Returns the disk usage in percent.
    """
    data = {}
    data['disk_usage'] = psutil.disk_usage('/')
    data['disk_partitions'] = psutil.disk_partitions()
    data['disk_io_counters'] = psutil.disk_io_counters()
    data['disk_io_counters_perdisk'] = psutil.disk_io_counters(perdisk=True)

    data['free'] = psutil.disk_usage('/').free
    data['used'] = psutil.disk_usage('/').used
    data['total'] = psutil.disk_usage('/').total
    data['percent'] = psutil.disk_usage('/').percent

    return data


def network_usage(**kwargs):
    """
    Returns the network usage in percent.
    """
    data = {}
    data['net_io_counters'] = psutil.net_io_counters()
    data['tcp'] = psutil.net_connections(kind='tcp')
    data['udp'] = psutil.net_connections(kind='udp')

    data['sent'] = psutil.net_io_counters().bytes_sent
    data['recv'] = psutil.net_io_counters().bytes_recv
    data['sntpkt'] = psutil.net_io_counters().packets_sent
    data['recvpkt'] = psutil.net_io_counters().packets_recv

    return data

def process_list(**kwargs):
    """
    Returns the process list.
    """
    data = {}
    for p in psutil.process_iter():
        try:
            temp = {}
            temp['pid'] = p.pid
            temp['name'] = p.name()
            temp['exe'] = p.exe()
            temp['cmdline'] = p.cmdline()
            temp['cwd'] = p.cwd()
            temp['status'] = p.status()
            temp['username'] = p.username()
            temp['create_time'] = p.create_time()
            temp['terminal'] = p.terminal()
            temp['threads'] = p.threads()
            temp['tree'] = p.children(recursive=True)
            temp['parent'] = p.parent()
            temp['files'] = p.open_files()
            temp['connections'] = p.connections()
            temp['environ'] = p.environ()
            data[p.pid] = temp
        except psutil.AccessDenied:
            pass
    return data



def process_usage(pid=os.getpid(), **kwargs):
    """
    Returns the process usage in percent.
    """
    data = {}
    data['details'] = psutil.Process(pid)
    data['cpu_times'] = psutil.Process(pid).cpu_times()
    data['cpu_times_user'] = psutil.Process(pid).cpu_times().user
    data['cpu_times_system'] = psutil.Process(pid).cpu_times().system
    data['cpu_percent'] = psutil.Process(pid).cpu_percent()
    data['memory_info'] = psutil.Process(pid).memory_info()
    data['memory_info_rss'] = psutil.Process(
        pid).memory_info().rss  # resident set size
    data['memory_info_vms'] = psutil.Process(
        pid).memory_info().vms  # virtual memory size
    data['memory_percent'] = psutil.Process(pid).memory_percent()
    
    temp = process_list()
    temp = temp[pid]
    data['name'] = temp['name']
    data['exe'] = temp['exe']
    data['cmdline'] = temp['cmdline']
    data['cwd'] = temp['cwd']
    data['status'] = temp['status']
    data['username'] = temp['username']
    data['create_time'] = temp['create_time']
    data['terminal'] = temp['terminal']
    data['threads'] = temp['threads']
    data['tree'] = temp['tree']
    data['parent'] = temp['parent']
    data['files'] = temp['files']
    data['connections'] = temp['connections']
    data['environ'] = temp['environ']

    return data


def system_details(**kwargs):
    """
    Returns the system information.
    """
    data = {}
    data['name'] = platform.node()
    data['release'] = platform.release()
    data['version'] = platform.version()
    data['machine'] = platform.machine()
    data['processor'] = platform.processor()
    data['platform'] = platform.platform()
    data['uname'] = platform.uname()
    data['uname_system'] = platform.uname().system
    data['uname_node'] = platform.uname().node
    data['uname_release'] = platform.uname().release
    data['uname_version'] = platform.uname().version
    data['uname_machine'] = platform.uname().machine
    data['uname_processor'] = platform.uname().processor

    return data

def cpu_usage_graph(min=1, **kwargs):
    """
    Returns the cpu usage in percent.
    """

    data = {}
    data['cpu'] = []
    data['mem'] = []
    data['net'] = []
    data['freq'] = []

    count = 0
    while True:
        count += 1
        if count == min*60:
            fig, axs = plt.subplots(2, 2, figsize=(10, 10))
            axs[0, 0].plot(data['cpu'])
            axs[0, 0].set_title('CPU Usage')
            axs[0, 0].set_xlabel('Time')
            axs[0, 0].set_ylabel('Percent')

            axs[0, 1].plot(data['mem'])
            axs[0, 1].set_title('Virtual Memory Usage')
            axs[0, 1].set_xlabel('Time')
            axs[0, 1].set_ylabel('Percent')

            axs[1, 0].plot(data['net'])
            axs[1, 0].set_title('Network Usage')
            axs[1, 0].set_xlabel('Time')
            axs[1, 0].set_ylabel('Bytes')

            axs[1, 1].plot(data['freq'])
            axs[1, 1].set_title('CPU Frequency')
            axs[1, 1].set_xlabel('Time')
            axs[1, 1].set_ylabel('MHz')

            fig.suptitle('Usage over {} minutes'.format(min))
            plt.savefig('out.jpg')
            return plt

        data['cpu'].append(psutil.cpu_percent())
        data['mem'].append(psutil.virtual_memory().percent)
        data['net'].append(psutil.net_io_counters().bytes_sent)
        data['freq'].append(psutil.cpu_freq().current)

        sleep(1)
