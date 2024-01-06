"""さまざまなメソッドで呼び出し"""
import requests

r = requests.get('http://127.0.0.1:5000/customer/kei')
print(r.text)
r = requests.post('http://127.0.0.1:5000/customer', data={'name': 'kei'})
print(r.text)
r = requests.put('http://127.0.0.1:5000/customer', data={'name': 'kei', 'new_name': 'suzuki'})
print(r.text)
r = requests.delete('http://127.0.0.1:5000/customer', data={'name': 'kei'})
print(r.text)