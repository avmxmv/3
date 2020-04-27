from requests import get, delete, post

print(get('http://localhost:5000/api/v2/item/1').json())  # Получение 1 товара
print(post('http://localhost:5000/api/v2/item', json={'id': 41,
                                                      'title': 'Машина',
                                                      'content': 'Какая-то машинка',
                                                      'price': 100,
                                                      'maxspeed': 1,
                                                      'boost': '1 час',
                                                      'power': 1,
                                                      'powerdensity': 1,
                                                      'size': '1 м',
                                                      'weight': 1
                                                      }))
# Добавление товара
print(get('http://localhost:5000/api/v2/item/41').json())  # Получение добавленного товара
print(delete('http://localhost:5000/api/v2/item/41'))  # Удаление 41 товара
print(get('http://localhost:5000/api/v2/item').json())  # Получение всех товаров
