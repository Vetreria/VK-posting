# Постим коммиксы про Python во Вконтакте

Програама находит случайный коммикс с https://xkcd.com и постит его в сообщество вместе с текстовым описанием.


## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

* Создайте сообщество
* Создайте приложение Вконтакте
* Получите client_id созданного приложения
* Прикрепите приложение к сообществу


## Переменные окружения

Создайте в папке проекта файл .env и положите в него переменные по образцу:
* VK_TOKEN='ваш токен'
* USER_ID='ваш ID'
* GROUP_ID='ID сообщества для публикации (первый символ "-", без него коммикс опубликуется на стене пользователя)'

## Где брать настройки для окружения

Implicit Flow для получения ключа доступа пользователя
```
https://vk.com/dev/implicit_flow_user
```

Узнать ID страницы или группы ВКонтакте
```
https://regvk.com/id/
```

## Запустить

Для работы программы запустите:

```
python main.py
```


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](dvmn.org)