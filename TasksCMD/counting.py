import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--per-day", type=float)
parser.add_argument("--per-week", type=float)
parser.add_argument("--per-month", type=float)
parser.add_argument("--per-year", type=float)
parser.add_argument("--get-by", choices=["day", "month", "year"], default="day")


if __name__ == '__main__':
    args = parser.parse_args()
    day_val1 = args.per_day if args.per_day else 0
    day_val2 = args.per_week / 7 if args.per_week else 0
    day_val3 = args.per_month / 30 if args.per_month else 0
    day_val4 = args.per_year / 360 if args.per_year else 0
    per_day = day_val1 + day_val2 + day_val3 + day_val4
    get_by = args.get_by
    if get_by == "day":
        print(int(per_day))
    elif get_by == "month":
        print(int(per_day * 30))
    elif get_by == "year":
        print(int(per_day * 365))
