"""
author: john nemeth
sources: class material
description: test file for get summary logic
"""
#import flask_main
#from flask_main import getSummaries
import nose
"""
def test_getsummaries():
    calids = ['first', 'third']
    caldict = [{'id': 'first', 'summary': 'correct'}]
    summaries = flask_main.getSummaries(calids, caldict)
    assert 'correct' in summaries
"""

# test to return span of day
def test_spanGreaterThanDay():
    now = arrow.utcnow()
    later = now.shift(days=1)
    assert spanGreaterThanDay(now, later)
    assert spanGreaterThanDay(now, later.shift(secs=1))
    assert not spanGreaterThanDay(now, later.shift(secs=-1))
