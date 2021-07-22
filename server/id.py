LAST_ID = 0

def new_id():
    global LAST_ID
    LAST_ID += 1
    return LAST_ID

