from tokens import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import psutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import operator
import collections
import time
import telepot
import RPi.GPIO as GPIO


memorythreshold = 85  # If memory usage more this %
poll = 300  # seconds

shellexecution = []
timelist = []
memlist = []
xaxis = []
settingmemth = []
setpolling = []
graphstart = datetime.now()

stopmarkup = {'keyboard': [['/stop']]}
hide_keyboard = {'hide_keyboard': True}

RELAY_PIN1 = 22
RELAY_PIN2 = 23
RELAY_PIN3 = 24
RELAY_PIN4 = 25
RELAY_PIN5 = 21


def clearall(chat_id):
    if chat_id in shellexecution:
        shellexecution.remove(chat_id)
    if chat_id in settingmemth:
        settingmemth.remove(chat_id)
    if chat_id in setpolling:
        setpolling.remove(chat_id)


def plotmemgraph(memlist, xaxis, tmperiod):
    plt.xlabel(tmperiod)
    plt.ylabel('% Used')
    plt.title('Memory Usage Graph')
    plt.text(0.1*len(xaxis), memorythreshold+2, 'Threshold: '+str(memorythreshold)+ ' %')
    memthresholdarr = []
    for xas in xaxis:
        memthresholdarr.append(memorythreshold)
    plt.plot(xaxis, memlist, 'b-', xaxis, memthresholdarr, 'r--')
    plt.axis([0, len(xaxis)-1, 0, 100])
    plt.savefig('/tmp/graph.png')
    plt.close()
    f = open('/tmp/graph.png', 'rb')  # some file on local disk
    return f


class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None
        self.sendMessage("197882762", "I'm online!")

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # Do your stuff according to `content_type` ...
        print("Your chat_id:" + str(chat_id)) # this will tell you your chat_id
        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            if content_type == 'text':
                if msg['text'] == '/stats' and chat_id not in shellexecution:
                    print_stats(chat_id)
                elif msg['text'] == "/stop":
                    clearall(chat_id)
                    bot.sendMessage(chat_id, "All operations stopped.", reply_markup=hide_keyboard)
                elif msg['text'] == "/shell" and chat_id not in shellexecution:
                    bot.sendMessage(chat_id, "Send me a shell command to execute", reply_markup=stopmarkup)
                    shellexecution.append(chat_id)
                elif chat_id in shellexecution:
                    bot.sendChatAction(chat_id, 'typing')
                    p = Popen(msg['text'], shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    if output != b'':
                        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
                    else:
                        bot.sendMessage(chat_id, "No output.", disable_web_page_preview=True)
                elif msg['text'] == '/memgraph':
                    bot.sendChatAction(chat_id, 'typing')
                    tmperiod = "Last %.2f hours" % ((datetime.now() - graphstart).total_seconds() / 3600)
                    bot.sendPhoto(chat_id, plotmemgraph(memlist, xaxis, tmperiod))

                elif msg['text'] == "/readpin":
                    print_relay_pins(chat_id)
                elif msg['text'].find("/writepin") != -1:
                    write_cmd(chat_id, msg['text'])
                elif msg['text'] == "/capture":
                    get_photo(chat_id)
                elif msg['text'] == "/sensor":
                    get_temp(chat_id)
                elif msg['text'] == "/all":
                    print_relay_pins(chat_id)
                    get_temp(chat_id)
                    get_photo(chat_id)
                else:
                    bot.sendMessage(chat_id, "command not found: " + msg['text'], disable_web_page_preview=True)


def print_relay_pins(chat_id):
    bot.sendChatAction(chat_id, 'typing')
    p = Popen('/home/pi/readpin', shell=True, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != b'':
        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
    else:
        bot.sendMessage(chat_id, "Something wrong", disable_web_page_preview=True)


def write_cmd(chat_id, cmd):
    bot.sendChatAction(chat_id, 'upload_document')
    rNum = int(cmd.split(" ")[1])
    rVal = int(cmd.split(" ")[2])
    p = Popen('/home/pi/writepin ' + str(rNum) + ' ' + str(rVal), shell=True, stdin=PIPE, stdout=PIPE,
          stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != b'':
        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
    print_relay_pins(chat_id)


def get_photo(chat_id):
    bot.sendChatAction(chat_id, 'upload_photo')
    p = Popen('/home/pi/capture', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != b'':
        bot.sendPhoto(chat_id=chat_id, photo=open('/home/pi/captures/image.jpg', 'rb'))
    else:
        bot.sendMessage(chat_id, "Something wrong", disable_web_page_preview=True)
    get_ndvi(chat_id)


def get_ndvi(chat_id):
    bot.sendChatAction(chat_id, 'upload_photo')
    p = Popen('/home/pi/capture_ndvi', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != b'':
        bot.sendPhoto(chat_id=chat_id, photo=open('/home/pi/captures/ndvi_image.jpg', 'rb'))
    else:
        bot.sendMessage(chat_id, "Something wrong", disable_web_page_preview=True)


def get_temp(chat_id):
    bot.sendChatAction(chat_id, 'record_video_note')
    p = Popen('/home/pi/sensor', shell=True, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != b'':
        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
    else:
        bot.sendMessage(chat_id, "Something wrong", disable_web_page_preview=True)


def print_stats(chat_id):
    bot.sendChatAction(chat_id, 'typing')
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boottime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    timedif = "Online for: %.1f Hours" % (((now - boottime).total_seconds()) / 3600)
    memtotal = "Total memory: %.2f GB " % (memory.total / 1000000000)
    memavail = "Available memory: %.2f GB" % (memory.available / 1000000000)
    memuseperc = "Used memory: " + str(memory.percent) + " %"
    diskused = "Disk used: " + str(disk.percent) + " %"
    pids = psutil.pids()
    pidsreply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except:
            print("Hm")
    sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedprocs:
        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
    reply = timedif + "\n" + \
            memtotal + "\n" + \
            memavail + "\n" + \
            memuseperc + "\n" + \
            diskused + "\n\n" + \
            pidsreply
    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)

TOKEN = telegrambot
GPIO.setwarnings(False)
bot = YourBot(TOKEN)
bot.message_loop()

tr = 0
xx = 0
# Keep the program running.
while 1:
    if tr == poll:
        tr = 0
        timenow = datetime.now()
        memck = psutil.virtual_memory()
        mempercent = memck.percent
        if len(memlist) > 300:
            memq = collections.deque(memlist)
            memq.append(mempercent)
            memq.popleft()
            memlist = memq
            memlist = list(memlist)
        else:
            xaxis.append(xx)
            xx += 1
            memlist.append(mempercent)
        memfree = memck.available / 1000000
        if mempercent > memorythreshold:
            memavail = "Available memory: %.2f GB" % (memck.available / 1000000000)
            graphend = datetime.now()
            tmperiod = "Last %.2f hours" % ((graphend - graphstart).total_seconds() / 3600)
            for adminid in adminchatid:
                bot.sendMessage(adminid, "CRITICAL! LOW MEMORY!\n" + memavail)
                bot.sendPhoto(adminid, plotmemgraph(memlist, xaxis, tmperiod))
    time.sleep(10)  # 10 seconds
    tr += 10
