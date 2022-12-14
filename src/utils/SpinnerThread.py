#!/usr/bin/env python

from threading import Thread, Event
import itertools
import time
import sys
from utils import UI_colors

class SpinnerThread(Thread):

	spinner = itertools.cycle('|/-#~=\\')

	def __init__(self, prefix: str, suffix: str):
		super(SpinnerThread, self).__init__()
		self.__stop_event = Event()
		self.__prefix = prefix
		self.__suffix = suffix

	def run(self):
		while not self.__stop_event.is_set():
			time.sleep(0.1)
			UI_colors.print_green(f'{self.__prefix} {next(SpinnerThread.spinner)}', end='\r')
			sys.stdout.flush()

		print('\033[K', end='\r')
		UI_colors.print_cyan(f'{self.__suffix}')
		sys.stdout.flush()

	def stop(self):
		self.__stop_event.set()
