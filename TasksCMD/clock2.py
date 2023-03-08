import sys
import datetime
import schedule


start = False
repeat_counter = 0
check = sys.argv[1:]


def print_qu(string):
    global repeat_counter
    repeat_counter += 1
    for _ in range(repeat_counter):
        print(string)
    if repeat_counter == 12:
        return schedule.CancelJob


if len(check) == 2:
    custom_str = check[0]
    pass_time = check[1].split('-')
    if len(pass_time) != 2:
        pass_time = None
        print('Wrong format time')
    try:
        pass_time = tuple(map(int, pass_time))
    except Exception as er:
        print(er)
        pass_time = None
    if 0 <= pass_time[0] <= 23 and 0 <= pass_time[1] <= 23:
        print('ok')
    else:
        pass_time = None
        print('Wrong format time')
else:
    custom_str = 'ку'
    pass_time = None


schedule.every().hour.do(print_qu, custom_str)

while True:
    if not start:
        start_time = datetime.datetime.now()
        if start_time.minute == 0:
            start = True
            print('started clock')
    if start:
        if not pass_time:
            schedule.run_pending()
        else:
            if pass_time[0] < datetime.datetime.now().hour < pass_time[1]:
                schedule.run_pending()
