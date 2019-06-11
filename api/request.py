import schedule
import time
import requests
from datetime import datetime
import csv

now = datetime.now()
format = "%H:%M"
init = now.strftime(format)

qtd2xx = 0
qtd4xx = 0
qtd5xx = 0

header = ["timestamp", "qtd de 2xx", "qtd de 4xx", "qtd de 5xx"]

with open('/csv/data.csv','a') as cf:
    writer = csv.writer(cf)
    writer.writerow(header)
cf.close()

def job():

    global qtd2xx
    global qtd4xx
    global qtd5xx
    global init

    try:
      r = requests.head("https://desafioperformance.b2w.io/bairros")
      print(r.status_code)
    except requests.ConnectionError:
      print("failed to connect")

    now2 = datetime.now().strftime(format)

    print(init + " " + now2 + " " +str(r.status_code))

    if now2 == init:
    
       if str(r.status_code)[0] == "2":
           qtd2xx += 1
           print(str(qtd2xx))
       elif str(r.status_code)[0] == "4":
           qtd4xx += 1
           print(str(qtd4xx))
       elif str(r.status_code)[0] == "5":
           qtd5xx += 1
           print(str(qtd5xx))
    else:
        if qtd5xx > qtd2xx:
            try:
               put = requests.put("https://desafioperformance.b2w.io/reinicia")
               print(put.status_code)
               print("Successful Restart")
            except requests.ConnectionError:
               print("failed to connect")

        # print(init + " " + str(qtd2xx) + " " + str(qtd4xx) + " " + str(qtd5xx))
        print('{}: qtd2xx: {} | qtd4xx: {} | qtd5xx: {}'.format(init, qtd2xx, qtd4xx, qtd5xx))
        
        row = [init, qtd2xx, qtd4xx, qtd5xx ]

        with open('/csv/data.csv','a') as cf:
            writer = csv.writer(cf)
            writer.writerow(row)

        cf.close()

        qtd2xx = 0
        qtd4xx = 0
        qtd5xx = 0

        init = now2


schedule.every(2).seconds.do(job)

while True:

   schedule.run_pending()
   time.sleep(1)    