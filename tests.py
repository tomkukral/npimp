from unittest import main
from unittest import TestCase
from unittest.mock import PropertyMock
from unittest.mock import patch
from npimp.action_modules import Charging


class ChargingTest(TestCase):
    def setUp(self):
        self.data = {
            'Smapi': {
                'power_avg': '-9228',
                'remaining_running_time': '216',
                'remaining_percent': '75',
                'cycle_count': '3290',
                'state': 'discharging',
                'stop_charge_thresh': '6'
            }
        }
        self.action = Charging()

    @patch.object(Charging, 'smapi', create=True, new_callable=PropertyMock)
    def test_state_detection(self, mock):
        """States are detected properly"""

        mock.return_value = self.data['Smapi']

        # disabled
        self.assertEqual(self.action.get_state(), 'charging-disabled')

        # enabled
        mock.return_value['stop_charge_thresh'] = 100
        self.assertEqual(self.action.get_state(), 'charging-enabled')


class DummyTest(TestCase):
    """Check testing framework is working"""

    def test_dummy(self):
        self.assertTrue(True)


if __name__ == '__main__':
    main()
