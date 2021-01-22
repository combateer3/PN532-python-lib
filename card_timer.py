from multiprocessing import Process, Event, Value
import time

# this function blocks until the card has been removed
# for some number of seconds
def card_removal_wait(card_read_func, sec=1, check_interval=0.1):
    card_removed = Event()
    # 2 processes are spawned
    # one keeps a timer
    # other resets the timer when the card is read again
    removed_for = Value('f', 0) # keeps track of how long the card has been removed for
    lock_timer = Process(target=card_remove_timer, args=(card_removed, removed_for, sec, check_interval))
    lock_con = Process(target=check_card_active, args=(card_removed, removed_for, card_read_func))

    # start processes
    lock_timer.start()
    lock_con.start()

    card_removed.wait() # wait until the processes have determined that the card has been removed

    # clean up
    lock_timer.terminate()
    lock_con.terminate()


def card_remove_timer(card_removed, removed_for, time_limit, check_interval):
    while removed_for.value < time_limit:
        time.sleep(check_interval)

        with removed_for.get_lock():
            removed_for.value += check_interval

    # while loop is only passed if the timer went time_limit seconds without resetting
    card_removed.set()


# if the card is still on the reader, this function will continuously reset the timer
# activity_func is the function to call to check if the card is on the reader
def check_card_active(card_removed, removed_for, activity_func):
    while not card_removed.is_set():
        activity_func() # should block unless it has a card to read
        with removed_for.get_lock():
            removed_for.value = 0

