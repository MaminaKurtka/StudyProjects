# MetricClientServer

To check capacity launch server (host, port) on 1 tab, then launch python3 interpreter and import class client in another tab. Create some clients with same host and port and try to use methods. 

Here's description of operating (RUS):

Клиент и сервер взаимодействуют между собой по простому текстовому протоколу через TCP сокеты. Текстовый протокол имеет главное преимущество – наглядность, можно просматривать диалог взаимодействия клиентской и серверной стороны без использования дополнительных инструментов.

Общий формат запросов и ответов.
Протокол поддерживает два вида запросов к серверу со стороны клиента:

- отправка данных для сохранения их на сервере

- получения сохраненных данных

Общий формат запроса клиента: 

<команда> <данные запроса><\n>

где:

- <команда> - команда сервера (команда может принимать одно из двух значений: put — сохранить данные на сервере, get — вернуть сохраненные данные с сервера),

- <данные запроса> - данные запроса (их формат мы подробно разберем ниже в примере),

- <\n> - символ переноса строки.

Обратим ваше внимание на пробел между командой и данными запроса и его отсутствием между данными и символом перевода на новую строку.

Общий формат ответов сервера:        


<статус ответа><\n><данные ответа><\n\n>


где:

- <статус ответа> - статус выполнения команды, допустимы два варианта: «ok» - команда успешно выполнена на сервере и «error» - выполнение команды завершилось ошибкой

- <данные ответа> - не обязательное поле (формат ответа и случаи его отсутствия будут рассмотрены в примере ниже)

- <\n\n> - два символа переноса строки.

Обратите внимание, что статус ответа и данные ответа разделены символом перевода строки <\n>.

Пример взаимодействия сервера и клиента.

Для наглядности рассмотрим протокол взаимодействия между клиентом и сервером на конкретном примере. В примере мы будем, собирать данные о работе операционной системы: cpu (загрузка процессора), usage (потребление памяти), disk_usage (потребление места на жестком диске), network_usage (статистика сетевых интерфейсов).

Запросы клиента.

Рассмотрим пример отправки на сервер данных для сохранения. Пусть у нас имеются данные измерений - загрузка процессора «cpu» на сервере "palm" во время 1150864247 была равна 23.7 процента. Строка запроса в этом случае будет иметь вид:             


put palm.cpu 23.7 1150864247\n


Чтобы получить с сервера данные, сохраненные по ключу «palm.cpu», необходимо в данных запроса просто передать имя ключа:         
 
 get palm.cpu\n
 
 
 Для случая, когда необходимо получить все хранимые на сервере данные, в качестве ключа используется символ звездочки «*». Пример строки запроса:     
 
 
 get *\n
 

В случаях:

- когда в запросе на получение данных передан не существующий ключ

- успешного выполнения команды сохранения данных put

сервер отправляет клиенту строку со статусом «оk» и пустым полем с данными ответа:          


ok\n\n


Если в параметре запроса переданы не валидные данные (например: нарушен формат запроса, ошибочная команда или значения value и timestamp не могут быть приведены к необходимому типу данных) сервер отправляет строку со статусом ответа «error» и данными ответа «wrong command»:       

error\nwrong command\n\n
