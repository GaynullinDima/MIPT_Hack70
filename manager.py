import messenger
import collections
import datetime
import time
import db_interactor

welcome_msg = "Welcome student. Are you tired of tedious lectures and you " + \
              "prefer to learn subjects from books? You are welcome then. " + \
              "Type 'help' to understand, how to use this service."

help_msg    = "'help' - you are here already \n" + \
              "'signup' %Name %Surname %group \n" + \
              "'mark me'/'markme' - mark me right now, " + \
                                   "right at the current lecture \n" + \
              "'mark me'/'markme %DayOfWeek/Today/Tomorrow %NumOfLesson/next/"+\
                                                           "current"

request_t = collections.namedtuple('request_t', 'user_id type data')
mark_me_t = collections.namedtuple('mark_me_t', 'time n_lesson mark_time')
signup_t  = collections.namedtuple('signup_t' , 'name surname group')
writev_t   = collections.namedtuple('writev_t', 'id text') 
stat_work_t = collections.namedtuple('stat_work_t', 'user_id use_coef ok_coef')

schedule = [ (datetime.time(9,0,0), datetime.time(10,25,0) ),  \
             (datetime.time(10,25,0), datetime.time(12,10,0) ),\
             (datetime.time(12,10,0), datetime.time(13,45,0) ),\
             (datetime.time(13,45,0), datetime.time(15,20,0) ),\
             (datetime.time(15,20,0), datetime.time(16,55,0) ),\
             (datetime.time(16,55,0), datetime.time(18,30,0) ),\
             (datetime.time(18,30,0), datetime.time(19,50,0) ) ]

class manager:
    def __init__(self):
        self.msg = messenger.messenger()
        self.read_q = []
        self.inner_rep = []
        self.current_req = []
        self.pending_req = []
        self.worker = []
        self.stat_work = []
        self.write_q = []
        self.db = db_interactor.DB_interactor()
        self.connection = self.db.create_connect()
    def weekday_to_number(self, weekday):
        return {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6
                }.get(weekday, "Out of range")

    def time_to_lesson(self, time):
        time = time.time() 
        return {
                schedule[0][0] <= time < schedule[0][1]: 1,
                schedule[1][0] <= time < schedule[1][1]: 2,
                schedule[2][0] <= time < schedule[2][1]: 3,
                schedule[3][0] <= time < schedule[3][1]: 4,
                schedule[4][0] <= time < schedule[4][1]: 5,
                schedule[5][0] <= time < schedule[5][1]: 6,
                schedule[6][0] <= time < schedule[6][1]: 7
                }.get(True, -1) 
        
    def read_requests(self):
        self.read_q = []
        self.read_q = self.msg.receive()

    def convert_to_inner(self):
        self.inner_rep = []
        for cur_req in self.read_q:
            split_req = cur_req.text.split(' ')
            split_req = [elem.lower() for elem in split_req if len(elem)]
            if (split_req[0] == 'help' or split_req[0] == '/start' or \
                split_req[0] == 'now'):
                self.inner_rep.append(request_t(cur_req.id, "service", \
                                                split_req[0])) 
            elif (split_req[0] == 'signup'):
                signup = signup_t(split_req[1], split_req[2], split_req[3])
                self.inner_rep.append(request_t(cur_req.id, "signup", signup))

            elif (split_req[0] == 'markme' or (split_req[0] == 'mark' and \
                split_req[1] == 'me')):
                if (len(split_req) <= 2):
                    mark_me = mark_me_t(cur_req.time,
                                        self.time_to_lesson(cur_req.time),
                                        cur_req.time)
                    self.inner_rep.append(request_t(cur_req.id,"mark_me",
                                                    mark_me))
                else:
                    dday = 0
                    if (split_req[len(split_req)-2] == "today"):
                        dday = 0
                    elif split_req[len(split_req)-2] == "tomorrow":
                        dday = 1
                    else: 
                        dday = - cur_req.time.weekday() + \
                            self.weekday_to_number(split_req[len(split_req)-2])
                        if dday < 0:
                            dday += 7

                    lesson = 0
                    if split_req[len(split_req)-1] == 'next':
                        lesson = self.time_to_lesson(cur_req.time) + 1
                    elif split_req[len(split_req)-1] == 'current':
                        lesson = self.time_to_lesson(cur_req.time)
                    else:
                        lesson = int(split_req[len(split_req)-1])

                    mark_me = mark_me_t(cur_req.time, lesson,
                                    cur_req.time+datetime.timedelta(days=dday))
                    self.inner_rep.append(request_t(cur_req.id,"mark_me",
                                                    mark_me))
            else:
                    self.inner_rep.append(request_t(cur_req.id, "service", \
                                                    "unknown"))


    def reg_check(self):
        for cur_req in self.inner_rep:
            if self.db.user_isregistred( and cur_req.type == 'mark_me':
                writev = writev_t(cur_req.user_id, "You are not registered. " \
                                         + "Type 'help' for more information")
                self.write_q.append(writev)

    def time_filter(self):
        temp_requests = self.inner_rep + self.pending_req
        self.current_req = []
        self.pending_req = []
        for cur_req in temp_requests:
            if (cur_req.type == "mark_me"):
                now_time = datetime.datetime.today()
                if (cur_req.data.n_lesson == -1):
                    writev = writev_t(cur_req.user_id, "What time is it? \n" +\
                                                       "Are you insane?")
                    self.write_q.append(writev)
                    continue

                if self.time_to_lesson(now_time) == cur_req.data.n_lesson and\
                   now_time.date() == cur_req.data.mark_time.date():
                        self.current_req.append(cur_req)
                else: 
                     self.pending_req.append(cur_req)

    def rate_up(self):
        pass

    def who_can_mark_me(self):
        pass

    def highest_rate(self):
        pass

    def signup_service_command(self):
        for cur_req in self.inner_rep:
            writev = None
            if cur_req.type == 'service':
                if cur_req.data == '/start':
                    writev = writev_t(cur_req.user_id, welcome_msg)
                elif cur_req.data == 'help':
                    writev = writev_t(cur_req.user_id, help_msg)
                elif cur_req.data == 'now': 
                    lesson = ""
                    if self.time_to_lesson(datetime.datetime.now()) == -1:
                        lesson = "It's time to have a rest!"
                    else:
                        lesson = str(self.time_to_lesson(\
                                     datetime.datetime.now()))
                    writev = writev_t(cur_req.user_id, "Current time: " + \
                             str(datetime.datetime.now().ctime()) + "\n" + \
                             "Current lesson: " + lesson)
                else: 
                    writev = writev_t(cur_req.user_id, "Command hasn't been " +
                                                       "recognized")
                self.write_q.append(writev)
            if cur_req.type == 'signup':
                if (self.db.add_user(cur_req.data.name, cur_req.data.surname, \
                                     cur_req.data.group) == None):
                    writev = writev_t(cur_req.user_id, "You have already been "+\
                                                       "registered.")
                else:
                    writev = writev_t(cur_req.user_id, "You have been "+\
                                                       "registered.")
                self.write_q.append(writev)

    def send_requests(self):
        for cur_req in self.write_q:
            self.msg.send(cur_req.id, cur_req.text)
        self.write_q = []

obj = manager()
while True:
    print("current",obj.current_req)
    print("pending",obj.pending_req)
    obj.read_requests()
    obj.convert_to_inner()
    obj.reg_check()
    obj.time_filter()
    obj.signup_service_command()
    obj.send_requests()
    time.sleep(1)
