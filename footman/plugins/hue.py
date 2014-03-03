import phue

HUE_IP = '10.0.1.19'
HUE_USER = 'maximillianvitek'

# # get the commandline arguments
# cmd = str(sys.argv)
# targetLight = sys.argv[1]
# targetCmd = sys.argv[2]
#
# # network setup
# hueURL = 'http://' + HUE_IP + '/api/' + HUE_USER + '/lights/'
#
# if targetCmd == 'off':
#     reqData = "{\"on\":false}"
# elif targetCmd == 'on':
#     reqData = "{\"on\":true, \"sat\":35, \"bri\":150,\"hue\":15000,\"effect\":\"none\"}"
# elif targetCmd == 'crazy':
#     reqData = "{\"on\":true, \"sat\":255, \"bri\":255,\"hue\":0,\"effect\":\"colorloop\"}"
# elif targetCmd == 'bright':
#     reqData = "{\"on\":true, \"sat\":35, \"bri\":255,\"hue\":15000,\"effect\":\"none\"}"
# elif targetCmd == 'dim':
#     reqData = "{\"on\":true, \"sat\":35, \"bri\":20,\"hue\":15000,\"effect\":\"none\"}"
# else:
#     reqData = "{}"
#
# requests.put(hueURL + targetLight + '/state',
#              data=reqData)
