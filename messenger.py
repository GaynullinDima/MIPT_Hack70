'''/*
    * Messenger class
    * This class is just wrapper over specific messenger, for 
    * integration with other messengers, just forward follow 
    * syscalls.
    * receive() - tries to read requests from the server and
    *             collects them to list of tuple, each of them 
    *             has follow fields:
    *               user_id = unique id
    *               raw_msg = text, which has been typed by user
    * send(user_id, msg) - send message to particular user
    * Example:
    *    bot = messenger()
    *    while True:
    *        msgs = bot.receive()
    *        print(msgs)
    */'''

import config
import telepot as telegram
import collections
import time
from datetime import datetime
import _thread

msg_t = collections.namedtuple('msg_t', 'id text time')

class messenger:
    def __init__(self):
        self.token = config.token 
        self.name  = config.name
        self.username = config.username
        self.backend_bot = telegram.Bot(config.token)
        self.update_id = 0
        self.receive_msg = []
        self.lock = _thread.allocate_lock() 
        self.backend_bot.message_loop(self.handle)

    def handle(self, msg):
        with self.lock:
            self.receive_msg.append(msg)

    def send(self, user_id, text):    
        self.backend_bot.sendMessage(user_id, text)

    def receive(self):
        msg_vector = []
        with self.lock:
            for msg in self.receive_msg:
                chat_id = msg['chat']['id']
                date = datetime.fromtimestamp(msg['date'])
                msg_vector.append(msg_t(chat_id, msg['text'], date)) 
            self.receive_msg = []
        return msg_vector 
