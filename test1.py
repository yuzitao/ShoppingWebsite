list1 = ['1', '2']
url = 'http://127.0.0.1:5000/order/pay_order?'
for i in range(1, len(list1)+1):
    url += 'oid_' + str(i) + '=' + list1[i-1] + '&'

print(url)

from io import StringIO

sio = StringIO()

import json

dict1 = {
    'name': 'admin'
}
