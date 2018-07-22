ID = 0
START_FLOOR = 1
DIRECTION = 2
DEST_FLOOR = 3
TIME = 4
POS_FAKE = 20
NEG_FAKE = -20

class Elevator:
    def __init__(self, eleid):
        self.id = eleid
        self.current = 1  # which floor
        self.direction = 0
        self.users = []
        self.MAX = POS_FAKE
        self.MIN = NEG_FAKE

    def is_empty(self):
        return not bool(len(self.users))


class User:
    def __init__(self, userid='', start=0, direction=0, time=0):
        self.userid = userid
        self.start = start
        self.direction = direction
        self.time = time


elevators = []
waiting_list = []
outside_list = []
users = {}
time = 0


def dump():
    global time
    for i, e in enumerate(elevators):
        print "Elevator No. %d, now in %d, heading %d, users: %s, MAX %d, MIN %d" \
              % (i, e.current, e.direction, map(lambda u: u[ID], e.users), e.MAX, e.MIN)
    time += 1
    print  # waiting_list


def reset():
    global elevators, waiting_list, users
    elevators = [Elevator(0), Elevator(1), Elevator(2)]
    waiting_list = []
    outside_list = []
    users = {}


def current():
    global elevators
    return {
       1: {'floor': elevators[0].current, "users": map(lambda u: u[ID], elevators[0].users)},
       2: {'floor': elevators[1].current, "users": map(lambda u: u[ID], elevators[1].users)},
       3: {'floor': elevators[2].current, "users": map(lambda u: u[ID], elevators[2].users)},
    }


def sort_by_time(a, b):
    if a[TIME] > b[TIME]:
        return -1
    if a[TIME] < b[TIME]:
        return 1
    return 0


def signal(a, b):
    if a > b:
        return 1
    if a < b:
        return -1
    return 0


# request [user1, startFloor, direction(1/0)]
# goto [user1, destFloor]
def process(request, goto):
    global elevators, waiting_list, users, time
    for u in request:
        u.append(-100)  # placeholder for dest
        u.append(time)  # placeholder for time
        if u[DIRECTION] == 0:
            u[DIRECTION] = -1
        outside_list.append(u)
        users[u[ID]] = u
        pick_flag = False
        for elevator in elevators:
            if elevator.direction == 1 and u[START_FLOOR] > elevator.MAX:
                elevator.MAX = u[START_FLOOR]
                pick_flag = True
                break
            if elevator.direction == -1 and u[START_FLOOR] < elevator.MIN:
                elevator.MIN = u[START_FLOOR]
                pick_flag = True
                break
        if not pick_flag:
            waiting_list.append(u)

    for item in goto:
        users[item[0]][DEST_FLOOR] = item[1]
        for elevator in elevators:
            for u in elevator.users:
                if item[0] == u[ID]:
                    if elevator.direction == 1:
                        elevator.MAX = max(elevator.MAX, item[1])
                    if elevator.direction == -1:
                        elevator.MIN = min(elevator.MIN, item[1])

    waiting_list = sorted(waiting_list, sort_by_time)

    # move
    for elevator in elevators:
        if elevator.current == elevator.MAX:
            elevator.direction = -1
        if elevator.current == elevator.MIN:
            elevator.direction = 1

        elevator.current += elevator.direction
        # check user out
        for u in elevator.users[:]:
            if u[DEST_FLOOR] == elevator.current:
                elevator.users.remove(u)
                users.pop(u[ID])
                if elevator.is_empty():
                    pass
                    # elevator.direction = 0

    user_in()

    for elevator in elevators:
        if elevator.is_empty() and len(waiting_list):
            elevator.MAX = elevator.current
            elevator.MIN = elevator.current
            pri_user = waiting_list[0]
            elevator.direction = signal(pri_user[START_FLOOR], elevator.current)
            if elevator.direction > 0:
                elevator.MAX = pri_user[START_FLOOR]
            else:
                elevator.MIN = pri_user[START_FLOOR]
            waiting_list.pop(0)

    # assign user to elevator.dest_users and set elevator.direction
    # single_elevator_assign()
    # assign()

    # we can remove this if assign add correct user in elevator.users list
    # user_in()


def user_in():
    global elevators, outside_list
    # check user in
    for elevator in elevators:
        for u in outside_list:
            if u[START_FLOOR] == elevator.current and (elevator.direction == u[DIRECTION] or elevator.direction == 0):
                if len(elevator.users) < 20:  # full send request to waiting list
                    elevator.users.append(u)
                    outside_list.remove(u)
                    if elevator.direction == 0:
                        elevator.direction = u[DIRECTION]


def single_elevator_assign():
    global elevators, waiting_list
    e = elevators[0]
    e.dest_users.extend(waiting_list)
    waiting_list = []
    if e.current == 1:
        e.direction = 1
    if e.current == 11:
        e.direction = -1


def assign():
    global elevators, waiting_list
    import strategy
    strategy.assign_all_waiting_users(waiting_list, elevators)
    waiting_list = []
