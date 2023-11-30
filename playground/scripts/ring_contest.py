from dataclasses import dataclass


@dataclass
class MyTime:
    h: int
    m: int


def start():
    alarms = []
    alarms.append(MyTime(6, 30))
    alarms.append(MyTime(6, 40))
    alarms.append(MyTime(6, 45))
    alarms.append(MyTime(6, 50))

    N = len(alarms)
    X = 3
    K = 4

    awake_time = get_awake_time(alarms, X, K)
    print(f"set {N} alarms: awaking time is {awake_time.h}:{awake_time.m} (X={X}\tK={K})")


def get_awake_time(alarms: list[MyTime], X: int, K: int) -> MyTime:

    sorted_by_mod_alarms = sorted(alarms, key=lambda x: x.m % X)

    grouped_by_mod_alarms = {key: list(m) for key, group in grop}
    # grouped_items = {key: list(group) for key, group in groupby(sorted_items, key=lambda x: x.group)}