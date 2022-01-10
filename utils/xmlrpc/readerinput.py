import xmlrpclib

def authPeople(url, lane_id, people_id, operator='admin', documents=[]):
    print 'authPeople lane_id=%d, people_id=%d operator=%s' % (lane_id, people_id, operator)
    s = xmlrpclib.ServerProxy(url)
    s.authPeople(lane_id, people_id, operator, documents)

def authBadge(url, lane_id, badge_code, badge_type=None):
    print 'authBadge lane_id=%d badge_code=%s badge_type=%s' % (lane_id, badge_code, badge_type)
    s = xmlrpclib.ServerProxy(url, allow_none=True)
    s.authBadge(lane_id, badge_code, badge_type)

url = 'http://gate004:166315190763@gate004:9999/'
people_id = 4113
lane_id = 36 
badge_code = 'FCE557C01C64'

authPeople(url, lane_id, people_id)
#authBadge(url, lane_id, badge_code)
