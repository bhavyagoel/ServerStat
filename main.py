from stats import *
import sys
import asyncio
import telebot
import os
import subprocess
import time
import schedule
import time


'''Reply Messages'''
# /info reply message
BOT_INFO = "This telegram bot helps provide the stats for the host system with an interactive user interface. "

# /help reply message
BOT_HELP = "Commands:\n" \
           "/info - show bot info\n" \
           "/cpu_usage - returns cpu usage\n" \
           "/mem_usage - returns memory usage\n" \
           "/disk_usage - returns disk usage\n" \
           "/net_usage - returns network usage\n" \
           "/proc_usage - return process usage for a given pid\n" \
           "/proc_list - returns process list\n" \
           "/graph - return usage graph for specified minutes\n" \
           "/cron - initialise a cron process to deliver usage graphs\n" \
    "/stop - stops all the scheduled cron tabs\n"


def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)


data = read_json('config.json')
tb = telebot.TeleBot(data['token'], parse_mode=None)


@tb.message_handler(commands=['info'])
def info(message):
    try:
        tb.send_message(message.chat.id, BOT_INFO)
    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['help'])
def send_help(message):
    try:

        if message.text.find('cpu_usage') != -1:
            msg = "Usage: /cpu_usage \n" \
                "Params: \n" \
                "  -p - CPU percentage \n" \
                "  -t - CPU usage time \n" \
                "  -cnt - CPU usage count \n" \
                "  -f - CPU usage frequency \n" \
                "  -s - CPU usage stats \n" \
                "  -pc - Per CPU usage \n" \
                "  -pc% - Per CPU usage percentage \n" \
                "  -pct - Per CPU usage time \n" \
                "  -pcf - Per CPU usage frequency \n" \
                "  -all - Show all details \n"
            tb.send_message(message.chat.id, msg)

        elif message.text.find('mem_usage') != -1:
            msg = "Usage: /mem_usage \n" \
                "Params: \n" \
                "  -v - Virutal Memory \n" \
                "  -s - Swap Memory \n" \
                "  -all - Show all details \n"
            tb.send_message(message.chat.id, msg)

        elif message.text.find('disk_usage') != -1:
            msg = "Usage: /disk_usage \n" \
                "Params: \n" \
                "  -p - Disk Partition \n" \
                "  -io - Disk IO Counters \n" \
                "  -iop - Disk IO Counters per CPU \n" \
                "  -det - Disk Space Details \n" \
                "  -all - Show all details \n"
            tb.send_message(message.chat.id, msg)

        elif message.text.find('net_usage') != -1:
            msg = "Usage: /net_usage \n" \
                "Params: \n" \
                "  -io - Network IO Counters \n" \
                "  -tcp - Network TCP details \n" \
                "  -udp - Network UDP details \n" \
                "  -det - Network Details \n" \

            tb.send_message(message.chat.id, msg)

        elif message.text.find('proc_usage') != -1:
            msg = "Usage: /proc_usage -pid \n" \
                "Params: \n" \
                "  -pid - Process ID \n" \
                "  -t - Process CPU Times" \
                "  -u - Process CPU Users \n" \
                "  -s - Process CPU Sys \n" \
                "  -p - Process CPU Percent \n" \
                "  -i - Process Memory Info \n" \
                "  -det - Show all details \n"
            tb.send_message(message.chat.id, msg)

        elif message.text.find('sys_det') != -1:
            msg = "Usage: /sys_det \n" \
                "Params: \n" \
                "  -all - Show all details \n"
            tb.send_message(message.chat.id, msg)

        elif message.text.find('graph') != -1:
            msg = "Usage: /graph \n" \
                "Params: \n" \
                "  -min - Minutes \n"
            tb.send_message(message.chat.id, msg)

        elif message.text.find('cron') != -1:
            msg = "Usage: /cron \n" \
                "Params: \n" \
                "  -min - Minutes \n"
            tb.send_message(message.chat.id, msg)

        else:
            tb.send_message(message.chat.id, BOT_HELP)

    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['cpu_usage'])
def get_cpu_usage(message):
    try:
        usage = cpu_usage()
        msg = message.text.split(' ')
        if message.text.find('-p') != -1:
            tb.send_message(
                message.chat.id, "CPU Usage percentage is {} %".format(usage['cpu_percent']))
        if message.text.find('-t') != -1:
            tb.send_message(message.chat.id,
                            "CPU Usage time is {}".format(usage['cpu_times']))
        if message.text.find('-cnt') != -1:
            tb.send_message(message.chat.id,
                            "CPU Usage count is {}".format(usage['cpu_count']))
        if message.text.find('-f') != -1:
            tb.send_message(
                message.chat.id, "CPU Usage freq is {}MHz".format(usage['cpu_freq']))
        if message.text.find('-s') != -1:
            tb.send_message(message.chat.id,
                            "CPU Usage stats is {}".format(usage['cpu_stats']))
        if message.text.find('-pc') != -1:
            tb.send_message(message.chat.id,
                            "Per CPU Usage is {}".format(usage['percpu']))
        if message.text.find('-pc%') != -1:
            tb.send_message(message.chat.id, "Per CPU percentage is {}".format(
                usage['percpu_percent']))
        if message.text.find('-pct') != -1:
            tb.send_message(message.chat.id, "Per CPU times is {}".format(
                usage['percpu_times']))
        if message.text.find('-pcf') != -1:
            tb.send_message(message.chat.id,
                            "Per CPU freq is {}".format(usage['percpu_freq']))
        if message.text.find('-all') != -1:
            with open('cpu_usage.json', 'w') as f:
                f.write(json.dumps(
                    usage, sort_keys=True, indent=4))
            tb.send_document(message.chat.id, open('cpu_usage.json', 'rb'))

    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['mem_usage'])
def get_mem_usage(message):
    try:
        usage = memory_usage()
        msg = message.text.split(' ')
        if message.text.find('-v') != -1:
            tb.send_message(message.chat.id, "Virutal Memory")
            tb.send_message(message.chat.id, "Free: {} MB\n".format(usage['virtual_memory_free']/1024**2)
                            + "Total: {} MB\n".format(usage['virtual_memory_total']/1024**2)
                            + "Used: {} MB\n".format(usage['virtual_memory_used']/1024**2)
                            + "Percentage: {} % \n".format(usage['virtual_memory_percent']))

        if message.text.find('-s') != -1:
            tb.send_message(message.chat.id, "Swap Memory")
            tb.send_message(message.chat.id, "Free: {} MB\n".format(usage['swap_memory_free']/1024**2)
                            + "Total: {} MB\n".format(usage['swap_memory_total']/1024**2)
                            + "Used: {} MB\n".format(usage['swap_memory_used']/1024**2)
                            + "Percentage: {} % \n".format(usage['swap_memory_percent']))
        if message.text.find('-all') != -1:
            tb.send_message(message.chat.id, "Virtual Mem\n" +
                            str(usage['virtual_memory']))
            tb.send_message(message.chat.id, "Swap Mem\n" +
                            str(usage['swap_memory']))

    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['disk_usage'])
def get_disk_usage(message):
    try:
        usage = disk_usage()
        if message.text.find('-p') != -1:
            tb.send_message(message.chat.id, "Disk Partitions")
            for partition in usage['disk_partitions']:
                tb.send_message(message.chat.id, str(partition))

        if message.text.find('-io') != -1:
            tb.send_message(message.chat.id, "Disk IO Counters \n {}".format(
                usage['disk_io_counters']))

        if message.text.find('-iop') != -1:
            tb.send_message(message.chat.id, "Disk IO Counters Per Disk")
            tb.send_message(message.chat.id, str(
                usage['disk_io_counters_perdisk']))

        if message.text.find('-det') != -1:
            tb.send_message(message.chat.id, "Disk Usage\n" +
                            "Free: {} GB\n".format(usage['free']/1024**3) +
                            "Total: {} GB\n".format(usage['total']/1024**3) +
                            "Used: {} GB\n".format(usage['used']/1024**3) +
                            "Percentage: {} % \n".format(usage['percent']))
        if message.text.find('-all') != -1:
            tb.send_message(message.chat.id, "Disk Usage\n" +
                            str(usage['disk_usage']))

    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['net_usage'])
def get_net_usage(message):
    try:
        usage = network_usage()
        if message.text.find('-io') != -1:
            tb.send_message(message.chat.id, "Network IO Counters \n {}".format(
                usage['net_io_counters']))

        if message.text.find('-tcp') != -1:
            tb.send_message(message.chat.id, "TCP")
            for tcp in usage['tcp']:
                tb.send_message(message.chat.id, str(tcp))

        if message.text.find('-udp') != -1:
            tb.send_message(message.chat.id, "UDP")
            for udp in usage['udp']:
                tb.send_message(message.chat.id, str(udp))

        if message.text.find('-det') != -1:
            tb.send_message(message.chat.id, "Network Usage\n" +
                            "Data Sent: {} MB \n".format(usage['sent']/1024**2) +
                            "Data Received: {} MB \n".format(usage['recv']/1024**2) +
                            "Packets Sent: {} \n".format(usage['sntpkt']) +
                            "Packets Received: {} \n".format(usage['recvpkt']))
    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['proc_usage'])
def get_proc_usage(message):
    try:
        usage = process_usage()
        if message.text.find('-pid') == -1:
            tb.send_message(message.chat.id, "Process ID not provided")
        else:
            msg = message.text.split(' ')
            idx = msg.index('-pid')
            pid = msg[idx+1]
            usage = process_usage(int(pid))
            if message.text.find('-t') != -1:
                tb.send_message(message.chat.id, "Process CPU Times")
                tb.send_message(message.chat.id, usage['cpu_times'])

            if message.text.find('-u') != -1:
                tb.send_message(message.chat.id, "Process CPU Users")
                tb.send_message(message.chat.id, usage['cpu_times_user'])

            if message.text.find('-s') != -1:
                tb.send_message(message.chat.id, "Process CPU Sys")
                tb.send_message(message.chat.id, usage['cpu_times_system'])

            if message.text.find('-p') != -1:
                tb.send_message(message.chat.id, "Process Memory")
                tb.send_message(message.chat.id, usage['cpu_percent'])

            if message.text.find('-i') != -1:
                tb.send_message(message.chat.id, "Process Memory Info")
                tb.send_message(message.chat.id,
                                "Resident Set Size {} MB\n".format(usage['memory_info_rss']/1024**2) +
                                "Virtual Mem Size {} MB\n".format(usage['memory_info_vms']/1024**2))

            if message.text.find('-det') != -1:
                tb.send_message(message.chat.id, "Process Details\n" +
                                "Name: {}\n".format(usage['name']) +
                                "exe: {}\n".format(usage['exe']) +
                                "cmdline: {}\n".format(usage['cmdline']) +
                                "cwd: {}\n".format(usage['cwd']))
                tb.send_message(message.chat.id, "status: {}\n".format(usage['status']) +
                                "username: {}\n".format(usage['username']) +
                                "time created: {}\n".format(usage['create_time']) +
                                "terminal: {}\n".format(usage['terminal']) +
                                "threads: {}\n".format(usage['threads']))
                tb.send_message(message.chat.id,
                                "tree: {}\n".format(usage['tree']))
                tb.send_message(message.chat.id,
                                "parent: {}\n".format(usage['parent']))
                tb.send_message(message.chat.id,
                                "files: {}\n".format(usage['files']))
                tb.send_message(
                    message.chat.id, "connections: {}\n".format(usage['connections']))
                tb.send_message(message.chat.id,
                                "environ: {}\n".format(usage['environ']))
                tb.send_message(message.chat.id,
                                "Details: {}\n".format(usage['details']))
                tb.send_message(message.chat.id, "Process Memory\n" +
                                str(usage['memory_percent']))
                tb.send_message(message.chat.id, "Process IO Counters \n {}".format(
                    usage['io_counters']))
    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['graph'])
def get_graph(message):
    try:
        min = 1
        if message.text.find('-min') == -1:
            tb.send_message(message.chat.id,
                            "Minutes not provided. Taking default as 1 Minute")
        else:
            msg = message.text.split(' ')
            idx = msg.index('-min')
            min = msg[idx+1]

        grph = cpu_usage_graph(float(min))
        grph.savefig('cpu_usage.png')
        tb.send_message(message.chat.id, "CPU Usage Graph")
        tb.send_photo(message.chat.id, open('cpu_usage.png', 'rb'))

    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


def schedule_graph(message):
    try:
        min = 1
        if message.text.find('-min') != -1:
            msg = message.text.split(' ')
            idx = msg.index('-min')
            min = msg[idx+1]

        grph = cpu_usage_graph(float(min))
        grph.savefig('cpu_usage.png')
        tb.send_message(message.chat.id, "CPU Usage Graph")
        tb.send_photo(message.chat.id, open('cpu_usage.png', 'rb'))

    except Exception as e:
        tb.send_message(message.chat.id, "Error Occured")
        tb.send_message(message.chat.id, "Error: " + str(e))


@tb.message_handler(commands=['cron'])
def set(message):
    min = 1
    if message.text.find('-min') == -1:
        tb.send_message(message.chat.id,
                        "Minutes not provided. Taking default as 1 Minute")
    else:
        msg = message.text.split(' ')
        idx = msg.index('-min')
        min = msg[idx+1]
    schedule.every(float(min)).minutes.do(schedule_graph, message)
    while(True):
        schedule.run_pending()
        time.sleep(1)


@tb.message_handler(commands=['stop'])
def scehduler_stop(message):
    schedule.clear()
    tb.send_message(message.chat.id, "Scheduler Stopped")


def main():
    tb.polling(none_stop=True)


if __name__ == '__main__':
    main()
