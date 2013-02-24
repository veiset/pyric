import unittest
import mocks
import pyric.events as events

class EventTest(unittest.TestCase):
    ''' Testing the connection '''

    def test_that_event_stores_key_value_pair(self):
        event = events.Event({})

        event.add('key', 'value')
        assert event.has('key')
        assert event.get('key') == 'value'


    def test_that_initial_value_is_stored(self):
        event = events.Event({'key' : 'value'})

        assert event.has('key')
        assert event.get('key') == 'value'
