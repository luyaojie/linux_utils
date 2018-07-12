#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by Roger on 2018/07/12
import sys
import os
import subprocess
import signal


def find_child(to_find_pid, process_relation):
    children = set()

    for pid, ppid in process_relation:
        if ppid == to_find_pid:
            children.add(pid)
    return children


def get_process_relation():
    p = subprocess.Popen("ps -al", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    process_relation = []

    for line in p.stdout.readlines()[1:]:
        att = line.strip().split()
        process_relation += [[int(att[3]), int(att[4])]]

    return process_relation


def main():
    pid = int(sys.argv[1])
    process_relation = get_process_relation()
    to_kill_set = {pid}
    while True:
        pre_size = len(to_kill_set)
        children = set()
        for pid in to_kill_set:
            children.update(find_child(pid, process_relation))
        to_kill_set.update(children)
        if pre_size == len(to_kill_set):
            break
    for pid in to_kill_set:
        os.kill(pid, signal.SIGTERM)


if __name__ == "__main__":
    main()
