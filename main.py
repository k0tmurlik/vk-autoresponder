import vk_api
import time 
import random

vk = vk_api.VkApi(token = "сюда токен") #Токен ВК
 
owner_id = 417583878 #ID Вк
owner_name = "Влад" #Ваше имя
owner_tg = "свой ник в тг" #Ваш ник в TG

def GetDialogs():#Запрос всех диалогов
	return vk.method("messages.getConversations")["items"]

def GetInfo(ids):#Запрос информации по ID
	return vk.method("users.get",{"user_ids":ids})[0]

massive = vk.method("messages.getById",{"message_ids":vk.method("messages.getConversationsById",{"peer_ids":owner_id})["items"][0]["last_message_id"]})["items"][0]["text"]#Запрос нужных массивов(Список тех, кому уже отвечал и список, кому нельзя отвечать)

#Парсинг массива
try:
	splitted_massive = massive.split("|")
	try:
		Writed = splitted_massive[0].replace(" ","").split(",")
	except:
		Writed = []
	blacklist = splitted_massive[1].replace(" ","").split(",")
except:
	Writed = []#Массив тех, кому писал
	blacklist = ["1","2","3","4"]#Массив тех, кому нельзя писать

Unreaded = False #Задаём стандартную переменную

while True:
	try:
		for Dialog in GetDialogs():#Перебираем диалоги
			ids = str(Dialog["conversation"]["peer"]["id"])#Получение ID диалога
			text = Dialog["last_message"]["text"] #Получение текста сообщения
			from_id = Dialog["last_message"]["from_id"] #Получение ID человека
			if ids[:2] != "20" and ids[:1] != "-" and ids not in blacklist: #Если диалог с человеком, и он не в чёрном списке
				if "!счс" in text.lower() and from_id == owner_id: #Команда на добавления в чёрный список
					blacklist.append(ids)#Добавление
					vk.method("messages.send",{"random_id":0,"peer_id":owner_id,"message":str(str(Writed).replace("'","").replace("[","").replace("]",""))+"|"+str(str(blacklist).replace("'","").replace("[","").replace("]",""))})#Отправили изменённый массив
					vk.method("messages.send",{"random_id":0,"peer_id":ids,"message":"Автоответчик больше не будет отвечать в этом диалоге"}) #Уведомили об этом
				try:
					Unreaded = Dialog["conversation"]["unread_count"] #Проверяем, прочитан ли диалог
					Unreaded = True #Не прочитан
				except:
					Unreaded = False #Прочитан
				if Unreaded: #Если не прочитан
					if ids in Writed: #Если бот уже писал человеку
						answer = random.choices(["если есть важный вопрос или дело, пиши в тг","я уже написал, что "+owner_name+" не прочтёт твоё сообщение.","если есть вопросы пиши в тг",owner_name+" не ответит, можешь не пытаться..","если что, это автоответчик, и я отвечаю за него"])#Выбираем одну из фраз
						vk.method("messages.send",{"random_id":0,"peer_id":ids,"message":GetInfo(ids)["first_name"]+", "+answer[0]+"\nhttps://t.me/"+owner_tg}) #Пишем
					else:#Если не писал
						vk.method("messages.send",{"random_id":0,"peer_id":ids,"message":"Привет, "+ GetInfo(ids)["first_name"]+". На данный момент "+owner_name+" включил режим не беспокоить и возможно в ближайший час, день, неделю или месяц он не прочтёт твоё сообщение. Если у тебя что-то важное, можешь написать ему в телеграм. Спасибо за понимание!\nhttps://t.me/"+owner_tg}) #Отвечаем о занятости
						if ids not in Writed:#Если человека нет в массиве, добавляем
							Writed.append(ids) #Добавляем
							time.sleep(1)#Подождём, пока переменная обновится(На всякий, бывали баги)
							vk.method("messages.send",{"random_id":0,"peer_id":owner_id,"message":"Ответил: "+str(str(Writed).replace("'","").replace("[","").replace("]",""))+"\n\nИгнор: "+str(str(blacklist).replace("'","").replace("[","").replace("]",""))})#Отправляем новый пакет данных
		time.sleep(1)

	except KeyboardInterrupt:
		print("\Автоответчик завершает свою работу") #Если бота закрыли, выводим сообщение 
		vk.method("messages.send",{"random_id":0,"peer_id":owner_id,"message":"Ответил: "+str(str(Writed).replace("'","").replace("[","").replace("]",""))+"\n\nИгнор: "+str(str(blacklist).replace("'","").replace("[","").replace("]",""))}) #Отправляем последнюю версию массива себе в лс
		break #Завершаем цикл
