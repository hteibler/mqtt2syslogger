# parameter file
# rename to parameter.py

TOPICS82 = [
    ('shellies/#', 0), 
    ('homie/#', 0)
    ]

    
TOPICS95 = [
    ('shellies/#', 0), 
    ('zigbee2mqtt/#', 0),
    ('zwave/#', 0)
    ]

BROKER82 = {
    'ip' : '192.x.x.x',
    'username': 'xx...xx',
    'password': 'yy...yy',
    'port': 1880
}
BROKER95 = {
    'username': 'xx...xx',
    'password': 'yy..yy',
    'ip': '192.z.z.z',
    'port': 1883,
}

options = {
    'broker' : BROKER95,
    'topics': TOPICS95,
    'storechangesonly': False,
    'loglevel': 'WARNING',
    'cname': 'test',
    'sys_level':"INFO",
    'sys_address':"192.168.192.100",
    'sys_port':512,
    'sys_facility':19,
    'do_syslog':True,
    'do_screen_full':False,
    'do_screen_short':True,
    'do_file':False
    }

