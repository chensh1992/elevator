from manager import ID, START_FLOOR, DIRECTION, DEST_FLOOR

def expect_wait_time(u, e):
    last_floor_current_direction = e.ext.get('last_floor_current_direction', None)
    last_floor_reverse_direction = e.ext.get('last_floor_reverse_direction', None)
    if u[DIRECTION] == e.direction or e.direction == 0:
        if (u[START_FLOOR] - e.current) * u[DIRECTION] >= 0:
            return (u[START_FLOOR] - e.current) * u[DIRECTION]
        else:
            ret = 22
            if last_floor_current_direction is not None:
                ret = (last_floor_current_direction - e.current) * e.direction  # to top
                if last_floor_reverse_direction is not None:
                    ret += ((last_floor_current_direction - last_floor_reverse_direction) * e.direction  # to reverse bottom
                         + abs(u[START_FLOOR] - last_floor_reverse_direction))  # move to target, no matter reverse or same direction
            return ret
    else:
        if last_floor_current_direction is None:
            return 22  # should not happen
        return (last_floor_current_direction - e.current) * e.direction + (u[START_FLOOR] - last_floor_current_direction) * u[DIRECTION]

def assign_user_to_elevator(u, e):
    e.dest_users.append(u)
    if e.direction == 0:
        if e.current < u[START_FLOOR]:
            e.direction = 1
        elif e.current > u[START_FLOOR]:
            e.direction = -1
        else:
            e.direction = u[DIRECTION]

def assign_all_waiting_users(requests, elevators):
    for e in elevators:
        adjust(e)

    for u in requests:
        score = 23
        elevator = None
        for e in elevators:
            expected_time = expect_wait_time(u, e)
            if score > expected_time:
                score = expected_time
                elevator = e
        assign_user_to_elevator(u, elevator)

def adjust(e):
    if len(e.users) == 0:
        if len(e.dest_users) == 0:
            e.direction = 0
        else:
            for u in e.dest_users:
                if (u[START_FLOOR] - e.current) * e.direction > 0:
                    break
            else:
                e.direction = -e.direction

    last_floor_reverse_direction = None
    if e.direction == 1:
        last_floor_current_direction = max(map(lambda u:u[DEST_FLOOR], e.users)) if e.users else e.current
        for u in e.dest_users:
            if u[START_FLOOR] > last_floor_current_direction:
                last_floor_current_direction = u[START_FLOOR]
            if (u[DIRECTION] == 1 and u[START_FLOOR] < e.current) or u[DIRECTION] == -1:
                if u[START_FLOOR] < last_floor_reverse_direction or last_floor_reverse_direction is None:
                    last_floor_reverse_direction = u[START_FLOOR]
        e.ext['last_floor_current_direction'] = last_floor_current_direction
        e.ext['last_floor_reverse_direction'] = last_floor_reverse_direction
    elif e.direction == -1:
        last_floor_current_direction = min(map(lambda u:u[DEST_FLOOR], e.users)) if e.users else e.current
        for u in e.dest_users:
            if u[START_FLOOR] < last_floor_current_direction:
                last_floor_current_direction = u[START_FLOOR]
            if (u[DIRECTION] == -1 and u[START_FLOOR] > e.current) or u[DIRECTION] == 1:
                if u[START_FLOOR] > last_floor_reverse_direction or last_floor_reverse_direction is None:
                    last_floor_reverse_direction = u[START_FLOOR]
        e.ext['last_floor_current_direction'] = last_floor_current_direction
        e.ext['last_floor_reverse_direction'] = last_floor_reverse_direction
    else:
        e.ext.pop('last_floor_current_direction', None)
        e.ext.pop('last_floor_reverse_direction', None)


