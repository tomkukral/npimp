#!/usr/bin/env python3

import logging
#import paho.mqtt.client as mqtt
import asyncio
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Reporter(object):
    """Reports information via MQTT"""

    def __init__(self, **kwargs):
        """
        kwargs:
            server
            port
            user
            password
        """

        # set variables
        self.logger = logging.getLogger(__name__)
        self.server = kwargs.get('server')
        self.port = kwargs.get('port', 1883)
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')

        # debug
        self.logger.debug('Initialized with: {}'.format(self.__dict__))


        # connect to mqtt broker
        self.client = mqtt.Client()
        self.client.username_pw_set(self.user, password=self.password)
        self.client.connect(self.server, port=self.port)


    def pub(self, topic, msg=None, retain=False):
        self.client.publish(topic, payload=msg, retain=retain)
        self.logger.debug(
            'Published {}: {}'.format(topic, msg)
        )

class Informator(object):
    battery_dir = '/sys/devices/platform/smapi/BAT0/'

    def __init__(self):
        self.refresh()

    def __str__(self):
        return str(self.__dict__)

    def refresh(self):
        self.set_battery()

    def set_battery(self):
        files = [
            'state',
            'remaining_percent',
            'power_avg',
            'cycle_count',
            'remaining_running_time',
            'stop_charge_thresh',
        ]
        for filename in files:
            with open(self.battery_dir + filename, 'r') as f:
                try:
                    setattr(self, filename, f.read().replace('\n', ''))
                except FileNotFoundError:
                    raise


def main():
    async def control_charging():
        interval = 900
        info = Informator()
        stop_thresh_charging = 100
        stop_thresh_idle = 6

        def get_state():
            """Return current state"""
            if int(info.stop_charge_thresh) < stop_thresh_charging:
                return 'charging-disabled'
            elif int(info.stop_charge_thresh) == stop_thresh_charging:
                return 'charging-enabled'

        def set_state(state):
            logger.debug('Requested state: {}'.format(state))

            thresh_file = '/sys/devices/platform/smapi/BAT0/stop_charge_thresh'

            if state == 'charging-enabled':
                value = stop_thresh_charging
            elif state == 'charging-disabled':
                value = stop_thresh_idle

            if value:
                with open(thresh_file, 'w') as f:
                    f.write(str(value))

        def transition():
            """Check and make transition"""
            if get_state() == 'charging-disabled':
                if (int(info.remaining_percent) <= stop_thresh_idle and
                    int(info.stop_charge_thresh) <= stop_thresh_charging):
                    set_state('charging-enabled')
                    logger.debug('Move to state charging-enabled')

            elif get_state() == 'charging-enabled':
                if info.state == 'idle':
                    set_state('charging-disabled')
                    logger.debug('Move to state charging-disabled')

            else:
                logger.error('Unknown state')





        while True:
            logger.debug('Checking charging')
            info.refresh()
            print(get_state())
            print(info)
            print(transition())


            await asyncio.sleep(interval)

#    asyncio.ensure_future(send_info())
    asyncio.ensure_future(control_charging())

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
