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
        self.write_q = []
        self.db = db_interactor.DB_interactor()
        data = self.db.get_all_user_id()
        self.stat_work = {}
        if (data != None):
            self.stat_work = { i[0]: [0,0] for i in data }
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
            elif (split_req[0] == 'signup' and len(split_req) == 4):
                signup = signup_t(split_req[1], split_req[2], split_req[3])
                self.inner_rep.append(request_t(cur_req.id, "signup", signup))
    
            elif (split_req[0] == 'ok'):

                mark_me = mark_me_t(cur_req.time, \
				    self.time_to_lesson(cur_req.time), \
                                    cur_req.time)
                self.inner_rep.append(request_t(cur_req.id, "ok", mark_me))

            elif (split_req[0] == 'no'):

                mark_me = mark_me_t(cur_req.time,
                                    self.time_to_lesson(cur_req.time),
                                    cur_req.time)
                self.inner_rep.append(request_t(cur_req.id, "no", mark_me))

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
            if self.db.user_isregistred(cur_req.user_id)[0] == False \
               and (cur_req.type == 'mark_me' or  cur_req.type == 'ok'\
					      or  cur_req.type == 'no' ):
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

    def who_can_mark_me(self):
        for cur_req in self.current_req:
            workers = self.db.mark_me(cur_req.user_id, cur_req.data.n_lesson)
            print(cur_req.user_id, cur_req.data.n_lesson)
            print(workers)
            if workers == None or len(workers) == 0:
                continue
            workers.sort( key=lambda el: el[1] )
            best_choices = [i for i in reversed(workers)]
            l = len(best_choices)
            the_man = None
            busy_level = 0

            while (busy_level < 6 and the_man == None):
                i = 0
                while (i < l) and (self.check_busy(best_choices[i][0], busy_level)):
                    i += 1
                if (i != l):
                    the_man = best_choices[i]
                busy_level += 1
            if the_man == None:
                writev = writev_t(cur_req.user_id,"Sorry. Nobody can mark you")
            else:
                self.mark_busy(the_man[0])
                data = self.db.get_user(cur_req.user_id)
                #print(data)
                surname = data[0]
                name = data[1]
                group = data[2]
                msg = "Could you please mark " + str(surname) + " " + str(name) +\
		      " " +  str(group) + "?"
                writev = writev_t(the_man[0], msg)

            self.write_q.append(writev)
		
	    
    def check_busy(self, user_id, busy_level):
        print(self.stat_work)
        return busy_level < self.stat_work[user_id][0]

    def mark_busy(self, user_id):
        self.stat_work[user_id][0] += 1

    def mark_ok(self, user_id):
        self.stat_work[user_id][1] += 1

    def check_ok(self, user_id):
        return self.stat_work[user_id][1] < \
               self.stat_work[user_id][0]
    def cur_lesson(self):
        lesson = self.time_to_lesson(datetime.datetime.now())
        return lesson

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
                if (self.db.add_user(cur_req.data.name,  cur_req.data.surname, \
                                     cur_req.data.group, cur_req.user_id) == cur_req.user_id):
                    writev = writev_t(cur_req.user_id, "You have already been "+\
                                                       "registered.")
                else:
                    writev = writev_t(cur_req.user_id, "You have been "+\
                                                       "registered.")
                    self.stat_work[cur_req.user_id] = [0, 0]
                self.write_q.append(writev)

            if cur_req.type == 'ok':
                if (self.check_ok(cur_req.user_id)):
                    self.stat_work[cur_req.user_id][1] += 1
                    self.db.rate_up(cur_req.user_id, cur_req.data.n_lesson)
                else:
                    writev = writev_t(cur_req.user_id, "Cheating is a bad thing.")
                    self.write_q.append(writev)

            if cur_req.type == 'no':
                if (self.stat_work[cur_req.user_id][1] > 0):
                    self.stat_work[cur_req.user_id][1] -= 1
                else:
                    writev = writev_t(cur_req.user_id, "Nobody asked you.")
                    self.write_q.append(writev)

    def update_stat(self):
        self.stat_work = {key: [0, 0] for key in self.stat_work}

    def send_requests(self):
        for cur_req in self.write_q:
            self.msg.send(cur_req.id, cur_req.text)
        self.write_q = []

obj = manager()
lesson = obj.cur_lesson()
while True:
    #print("current",obj.current_req)
    #print("pending",obj.pending_req)

    if (lesson != obj.cur_lesson()):
        obj.update_stat()
        lesson = obj.cur_lesson()
    obj.read_requests()
    obj.convert_to_inner()
    obj.reg_check()
    obj.time_filter()
    obj.who_can_mark_me()
    obj.signup_service_command()
    obj.send_requests()
    time.sleep(1)
