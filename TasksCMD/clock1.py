import schedule
import datetime


repeat_counter = 0
start = False


def print_qu():
    global repeat_counter
    repeat_counter += 1
    for _ in range(repeat_counter):
        print('Ку')
    print()
    if repeat_counter == 12:
        return schedule.CancelJob


schedule.every().hour.do(print_qu)

while True:
    if not start:
        start_time = datetime.datetime.now()
        if start_time.minute == 0:
            start = True
    if start:
        schedule.run_pending()
