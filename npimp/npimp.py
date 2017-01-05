#!/usr/bin/env python3

import logging
#import paho.mqtt.client as mqtt
import asyncio
from pprint import pprint
import time

from .info_modules import Smapi
from .action_modules import Dumper, Charging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    print('start main')
    info_classes = [Smapi]
    info_objects = []

    action_classes = [Dumper, Charging]
    action_objects = []

    def init_objects():
        for c in info_classes:
            info_objects.append(c())

        for c in action_classes:
            action_objects.append(c())

    def update_info_objects():
        for o in info_objects:
            o.refresh()

    def merge_info_objects():
        data = {}
        for o in info_objects:
            data[o.__class__.__name__] = o.__dict__

        return data

    def run_action_objects(data):
        tasks = [i.run(data) for i in action_objects]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))

        print(tasks)

    init_objects()
    while True:
        update_info_objects()
        run_action_objects(merge_info_objects())
        time.sleep(60)
