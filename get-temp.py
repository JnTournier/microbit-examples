"""Get-temp

Usage:
    get-temp.py --device <ble_mac> --timeloop <timeloop> [-s <security>]

Options:
    -h, --help                 Print this message.
    -d, --device <ble_mac>     MAC address of the device.
    -t, --timeloop <timeloop>  Number of seconds to wait between two requests.
    -s, --security <security>  The security level of the pairing method. [Default : none]
"""

import time
from docopt import docopt, DocoptExit
from timeloop import Timeloop
from datetime import timedelta
from bluepy import btle

try:
    docopt(__doc__)
except DocoptExit:
    print(__doc__)
    exit(1)
else :
    args = docopt(__doc__)
    
getTemp = Timeloop()
randomAddress = 'random'
#peripheralDevice = "DC:D0:17:9D:1D:5D"
#peripheralDevice = "FE:E2:20:7D:1A:9D"

@getTemp.job(interval=timedelta(seconds=int(args['--timeloop'])))
def getTemperature():
    # Without this, the reading of the temperature characteristic fails
    # ch = p.getCharacteristics(uuid="e95d9250-251d-470a-a062-fa1922dfa9a8")[0]
    # temperature = p.getCharacteristics(uuid="e95d9250-251d-470a-a062-fa1922dfa9a8")[0]
    # accelerometer = p.getCharacteristics(uuid="e95dca4b-251d-470a-a062-fa1922dfa9a8")[0]
    
    t = temperature.read()
    #a = accelerometer.read()
    
    print(f"Temperature: {ord(t)}")

if __name__ == "__main__":
    
    try:
        docopt(__doc__)
    except DocoptExit:
        print(__doc__)
    else:
        peripheralDevice = args['--device']
        
        print(f'[i] Connecting to {peripheralDevice}')
        try:
            p = btle.Peripheral(peripheralDevice, randomAddress)
        except btle.BTLEDisconnectError:
            print(f'[w] Your BTLE device is not connected')
            print(f'[i] Quiiting the program')
            exit(1)
        else:
            # for svc in p.getServices():
            #     print(f"Services : {svc.uuid.get}")
            
            svc = p.getServiceByUUID('e95d6100-251d-470a-a062-fa1922dfa9a8')
            temperature = svc.getCharacteristics("e95d9250-251d-470a-a062-fa1922dfa9a8")[0]
            
            getTemp.start(block=True)
            
            # p.setSecurityLevel(level='medium') 
            
            print('[i] End of the connection...')
