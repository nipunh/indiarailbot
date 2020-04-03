# from flask import Flask, render_template, request, redirect, url_for
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# import logging




# app = Flask(__name__)
# BotV1 = ChatBot("BotV1", storage_adapter="chatterbot.storage.SQLStorageAdapter",
# 	)
# trainer = ChatterBotCorpusTrainer(BotV1)
# trainer.train(
#     "chatterbot.corpus.english.greetings",
#     "chatterbot.corpus.english.conversations"
# )

# @app.route("/")
# def home():
# 	return render_template("index.html")

# @app.route("/bot")
# def get_bot_response():
# 	userText = request.args.get('msg')
# 	return str(BotV1.get_response(userText))


# if __name__ == '__main__':
# 	app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
import requests 
import json 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import sqlite3
#for pnr
from pnr_scraping import pnr_enqiury 

#for train route
from train_route import train_rt
# from tr import train_rt

#for train between stations
from train_bw_stn import train_bw_stn


##Running status scripts
# from rst import train_rst
from running_status import train_rst

##Platform enquiry
from platformEnq import platform_enquiry

##fare Enquiry
from fareEnquiry import fare_enquiry


# from train_bw_stn import train_bw_stn
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process



logging.basicConfig(filename="newfile.txt", level=logging.INFO,
                    filemode='r+')

date = datetime.now().strftime('%d-%m-%Y')
train_number = -1
maxpos =-1

application = Flask(__name__)
BotV1 = ChatBot("BotV1", storage_adapter="chatterbot.storage.SQLStorageAdapter",
	)
trainer = ChatterBotCorpusTrainer(BotV1)
trainer.train(

    "./data/my_corpus/greetings.yml",
    "./data/my_corpus/trainbot.yml",
    "./data/my_corpus/conversations.yml",
    "./data/my_corpus/humor.yml",
    "./data/my_corpus/computers.yml"
)

@application.route("/")
def home():
	return render_template("index.html")

@application.route("/bot")
def get_bot_response():
	userText = request.args.get('msg')
	f = open("log.txt", "a")
	f.write(userText+"\n")
	f.close()
	info = check_intent(userText)
	# words=word_tokenize(userText)
	# stop_words=set(stopwords.words("english"))
	# data=[]

	# for i in words:
	# 	if i not in stop_words:
	# 		data.append(i)
	# number = [x for x in data if x.isdigit()]

	

	# #route_inent=0 ,pnr_intent=1 , liveStatus_intent=2

	# intent_info = [['train', 'route'],['pnr','status','seat','confirm','enquiry'],['train','running','status','live'],['train','between','from']]
	# intent_score=[]
	# intent_dict={ 0: "route_inent",1:"pnr_intent",2:"liveStatus_intent",3:"Train_bw_station"}
	# size= len(intent_dict)

	# for x in range(0,size):
	# 	intent_score.append(len(set(intent_info[x])&set(data))) 
		
	# maxpos = intent_score.index(max(intent_score))
	# if intent_score[maxpos] > 0 :
	# 	intent = maxpos

	# else:
	# 	intent = -1	
	intent = info["debit"]
	if intent == 0:
		ans=train_route(info)
		return(ans)
	if intent == 1:
		ans=pnr_status(info)
		return ans
		
		
	if intent == 2:
		ans=running_status(info)
		return(ans)
	
	if intent ==3:

		ans=train_bw_station(info)
		return(ans)
	if intent == 4:
		ans=platform_enq(info)
		return ans

	if intent == 5:
		ans=fareenq(info)
		return ans	
		
	elif intent == -1:
		new_msg = userText
		words=word_tokenize(new_msg)
		stop_words=set(stopwords.words("english"))
		data=[]
		for i in words:
			if i not in stop_words:
				data.append(i)
				

		number = [x for x in data if x.isdigit()]
		
		
		prev_msg=last_msg()
		print("prev_msg="+prev_msg)
		info_next=check_intent(prev_msg)
		prev_intent=info_next["debit"]
		print("prev_intent="+str(prev_intent))

		if prev_intent == 0:
			if len(number) != 0:
				info_next["train_num"] = str(number[0])	
			ans=train_route(info_next)
			return(ans)
		
		if prev_intent == 1:
			if len(number[0]) == 10:
				info_next["pnr_number"] = str(number[0])
			ans=pnr_status(info_next)
			return(ans)	


		if prev_intent == 2:
			# if data[0].isdigit():
			# 	info_next["train_num"] = data[0]
			# 	res = [val for key, val in station_code_name.items() if data[1] in key]
			# 	info_next["station_code"] = res[0]
			# else:
			# 	info_next["train_num"] = data[1]
			# 	res = [val for key, val in station_code_name.items() if data[0] in key]
			# 	info_next["station_code"] = res[0]						
			ans=running_status(info)
			return(ans)
	
		if prev_intent == 3:
			# res1 = [val for key, val in station_code_name.items() if data[0] in key]
			# res2 = [val for key, val in station_code_name.items() if data[1] in key]
			# info_next["src_stn"]=res1[0]
			# info_next["dest_stn"]=res2[0]
			# print(info_next["src_stn"],info_next["dest_stn"])
			ans=train_bw_station(info)
			return(ans)

		if prev_intent == 4:
			# res1 = [val for key, val in station_code_name.items() if data[0] in key]
			# info_next["station_code"] = res1[0]
			# print(info_next["station_code"])
			ans=platform_enq(info)
			return(ans)

		if prev_intent == 5 :
			# res1 = [val for key, val in station_code_name.items() if data[0] in key]
			# info_next["station_code"] = res1[0]
			# print(info_next["station_code"])
			ans=fareenq(info)
			return(ans)	

		

		else:
			print("BOT REPLY")
			ans1={"debit":None,"response_code":None, "bot_reply":None}
			ans1["debit"]=intent
			ans1["bot_reply"]=str(BotV1.get_response(userText))
			print(ans1["bot_reply"])
			return(ans1)

#Train name or number
def train_name_num(info):
	train_num=info["train_num"]
	api_key=info["api_key"]
	try:
		train_route_url = "https://api.railwayapi.com/v2/name-number/train/"+str(train_num)+"/apikey/"+api_key+"/"
		response_ob = requests.get(train_route_url)
		result = response_ob.json()
		print(result["response_code"])
		return(result["response_code"])
	except:
		return("503")	
	

#Train route
def train_route(info):	
	train_num = info["train_num"]
	if train_num == -1 or int(train_num) < 5:
		info["debit"]=0
		info["response_code"] = 502
		return(info)
	else:	
		ans = train_rt(info)
		f = open("log.txt", "a")
		f.write("Query Executed Successfully"+"\n")
		f.close()
		info["html"] = ans["result"]
		info["debit"] = 0
		info["response_code"] = ans["response_code"]
		return(info)

	# train_num=info["train_num"]
	# api_key=info["api_key"]
	# ans=train_name_num(info)
	# if ans == 200 :
	# 	try:
	# 		train_route_url = "https://api.railwayapi.com/v2/route/train/"+str(train_num)+"/apikey/"+api_key+"/" 
	# 		response_ob = requests.get(train_route_url)
	# 		result = response_ob.json()
	# 		if result["response_code"] == 200 :
	# 			f = open("log.txt", "a")
	# 			f.write("Query Executed Successfully"+"\n")
	# 			f.close()
	# 			result["debit"]=info["debit"]
	# 			return(result)
	# 		else:
	# 			info["response_code"]=result["response_code"]
	# 			return(info)
	# 	except:
	# 		info["debit"]=0
	# 		info["response_code"]= 503
	# 		return(info)

	# else:
	# 	f = open("log.txt", "a")
	# 	f.write("Status:Query Not executed Successfully"+"\n")
	# 	f.close()
	# 	info["debit"]=0
	# 	info["response_code"]= ans
	# 	return(info)

def pnr_status(info):
	pnr = info["pnr_number"]
	if pnr == -1:
		info["debit"] = 1
		info["response_code"] = 502
		return(info)

	elif len(pnr) == 10:
		ans = pnr_enqiury(info)
		info["html"] = ans["result"]
		info["debit"] = 1
		info["response_code"] = ans["response_code"]
		f = open("log.txt", "a")
		f.write("Query Executed Successfully"+"\n")
		f.close()
		return(info)
	
	elif len(pnr) < 10 or len(pnr) >10:
		info["debit"] = 1
		info["response_code"] = 502
		return(info)	

def running_status(info):
	train_num = info["train_num"]
	if train_num == -1 or int(train_num) < 5:
		info["debit"] = 2
		info["response_code"] = 502
		return(info)
	else:	
		ans = train_rst(info)
		f = open("log.txt", "a")
		f.write("Query Executed Successfully"+"\n")
		f.close()
		info["html"] = ans["result"]
		info["debit"] = 2
		info["response_code"] = ans["response_code"]
		return(info)
	# station_code=info["station_code"]
	# api_key=info["api_key"]
	# train_num = int(info["train_num"])
	# print(station_code,train_num)
	# if station_code == None or train_num == None  :
	# 	info["debit"]=2
	# 	info["response_code"]=502
	# 	return(info)
	# else:
	# 	try:
	# 		train_route_url = "https://api.railwayapi.com/v2/live/train/"+str(train_num)+"/station/"+str(station_code)+"/date/"+ date +"/apikey/"+api_key+"/"
	# 		response_ob = requests.get(train_route_url)
	# 		result = response_ob.json()
	# 		print(result['response_code'])
	# 		if result["response_code"] == 200 :
	# 			f = open("log.txt", "a")
	# 			f.write("Query Executed Successfully"+"\n")
	# 			f.close()
	# 			result["debit"]=info["debit"]
	# 			return (result)
	# 		else :
	# 			info["debit"]=2
	# 			info["response_code"]=result["response_code"]
	# 			return(info)
	# 	except:
	# 		info["debit"]=2
	# 		info["response_code"]=503
	# 		return(info)
					

def train_bw_station(info):
	place1=info["src_stn"]
	place2=info["dest_stn"]
	if place1 == None or place2 == None :
		info["debit"]=3
		info["response_code"]=502
		return(info)
	else:
		ans = train_bw_stn(info)
		f = open("log.txt", "a")
		f.write("Query Executed Successfully"+"\n")
		f.close()
		info["html"] = ans["result"]
		info["debit"] = 3
		info["response_code"] = ans["response_code"]
		return(info)

				
				

def platform_enq(info):
	station_code=info["station_code"]
	train_num = info["train_num"]
	if station_code == None or train_num == None :
		info["debit"] = 4
		info["response_code"] = 502
		return(info)
	else:
		ans = platform_enquiry(info)
		f = open("log.txt", "a")
		f.write("Query Executed Successfully"+"\n")
		f.close()
		info["html"] = ans["result"]
		info["debit"] = 4
		info["response_code"] = ans["response_code"]
		return(info)

def fareenq(info):
	place1=info["src_stn"]
	place2=info["dest_stn"]
	train_num = info["train_num"]
	if place1 == None or train_num == None or place2 == None :
		info["debit"] = 5
		info["response_code"] = 502
		return(info)
	else:
		ans = fare_enquiry(info)
		f = open("log.txt", "a")
		f.write("Query Executed Successfully"+"\n")
		f.close()
		info["html"] = ans["result"]
		info["debit"] = 5
		info["response_code"] = ans["response_code"]
		return(info)		
		



def check_intent(user_text):
	# print("Hello")
	words=word_tokenize(user_text)
	# stop_words=set(stopwords.words("english"))
	data=[]

	for i in words:
		if i not in stop_words:
			data.append(i)

#Intent Classification	
	number = [x for x in data if x.isdigit()]
	info={"debit":None,"response_code":None, "bot_reply":None, "station_code":None, "train_num":-1, "src_stn":None, "dest_stn":None, "words":None,
		 "second_msg":None, "date":None, "time_bracket":None, "pnr_number":-1, "html":None}
	#route_inent=0 ,pnr_intent=1 , liveStatus_intent=2
	intent_info = [['route','path','way','direction','my','schedule','stop','stops'],['pnr','enquiry','waiting','status','seat','confirm','confirmation','booking','list'],
	['running','current','location','live', 'track', 'tracking','delay','delayed','where','present','train','status'],
	['train','between','from','stations','station','trains','destination'],['train','platform','number','which','enquiry','stop','hault'],
	['fare','ticket','price','amount','cost','much','train']]
	
	intent_score=[]
	intent_dict={ 0: "route_inent",1:"pnr_intent",2:"liveStatus_intent",3:"Train_bw_station",4:"Train_arrivals",5:"fareenq"}
	info["date"]=date
	
	res=[]
	for i in range(0,len(data)):
		res.append([val for key, val in station_code_name.items() if data[i].lower() in key])

	
	res = [x for x in res if x]	
	if len(res) >= 2:
		info["src_stn"]=res[0][0]
		info["dest_stn"]=res[1][0]
	elif len(res) >= 2 and len(number) ==1:
		info["src_stn"]=res[0][0]
		info["dest_stn"]=res[1][0]	
		info["train_num"] = number[0]
	elif len(res) ==1 and len(number) == 1:
		info["station_code"] = res[0]
		info["train_num"] = number[0]
	elif len(number) == 1 and len(res) == 0:
		info["train_num"] = number[0]
	elif len(res) == 1:
		info["station_code"] = res[0][0]
	elif len(number) == 10:
		info["pnr_number"] = number[0] 	
		

	size= len(intent_dict)
	for x in range(0,size):
		intent_score.append(len(set(intent_info[x])&set(data))) 
		
	maxpos = intent_score.index(max(intent_score))
	print(maxpos)
	if intent_score[maxpos] > 0 :
		intent = maxpos
		
	else:
		# if len(res) >= 2 and len(number) == 0:
		# 	intent = 3
		# elif len(res) >= 2 and len(number) == 1:
		# 	intent = 5
		# else:	
		intent = -1	

	info["debit"]=intent
	if len(number) != 0:
		if len(number[0]) == 5:
			info["train_num"]=str(number[0])
		elif len(number[0]) == 10:
			info["pnr_number"] = number[0]	
		elif int(number[0]) < 24 and int(number[0]) != 0:
			info["time_bracket"] = number[0]
	else:
		info["train_num"]=-1

	print(info)
	info["words"]=data
	return(info)		

def last_msg():
	with open('log.txt', 'r') as f:
		lines = f.read().splitlines()
		return(lines[-2])	

def station_code(city_name,api_key):
	train_route_url = "https://api.railwayapi.com/v2/name-to-code/station/"+city_name+"/apikey/"+api_key+"/"
	response_ob = requests.get(train_route_url)
	result = response_ob.json()
	if result["response_code"] == 200 :
		return(result["stations"]["code"])	


station_code_name = {'a n dev nagar': 'ACND', 'chengannur': 'CNGR', 'jawad road': 'JWO', 'mayyanad': 'MYY', 'rura': 'RURA', 'abhaipur': 'AHA', 'chennai beach': 'MSB',
 'jawai bandh': 'JWB', 'mccluskieganj': 'MGME', 'rusera ghat': 'ROA', 'abohar': 'ABS', 'chennai central': 'MAS', 'jawali': 'JAL', 'mecheda': 'MCA', 'ruthiyai': 'RTA', 
 'abu road': 'ABR', 'chennai egmore': 'MS', 'jayasingpur': 'JSP', 'mecheri road': 'MCRD', 's bhakhtiyarpur': 'SBV', 'achalda': 'ULD', 'cheoki': 'COI', 'jaynagar': 'JYG', 
 'medapadu': 'MPU', 'sabarmati jn': 'SBI', 'achhnera jn': 'AH', 'cherukara': 'CQA', 'jehanabad': 'JHD', 'medchal': 'MED', 'adavali': 'ADVI', 'chettinad': 'CTND', 
 'jejuri': 'JJR', 'meerut cant': 'MUT', 'sabaur': 'SBO', 'adesar': 'AAR', 'chhabra gugor': 'CAG', 'jeruwa khera': 'JRK', 'meerut city': 'MTC', 'sachin': 'SCH',
  'adhartal': 'ADTL', 'chhanera': 'CAER', 'jetalsar jn': 'JLR', 'meghnagar': 'MGN', 'sadat': 'SDT', 'adilabad': 'ADB', 'chhapi': 'CHP', 'jeur': 'JEUR', 
  'mehnar road': 'MNO', 'sadisopur': 'SDE', 'adina': 'ADF', 'chhapra': 'CPR', 'jeypore': 'JYP', 'mehsi': 'MAI', 'sadulpur jn': 'SDLP', 'adipur': 'AI', 
  'chhapra kacheri': 'CI', 'jhajha': 'JAJ', 'meja road': 'MJA', 'safdarganj': 'SGJ', 'adityapur': 'ADTP', 'chharodi': 'CE', 'jhalawar road': 'JHW', 'melattur': 'MLTR',
   'safedabad': 'SFH', 'adoni': 'AD', 'chhatna': 'CJN', 'jhalida': 'JAA', 'melmaruvattur': 'MLMR', 'sagadapata': 'SGDP', 'adra jn': 'ADRA', 'chhindwara jn': 'CWA', 
   'jhalwara': 'JLW', 'meralgram': 'MQX', 'sagar jambagaru': 'SRF', 'adrsh ngr delhi': 'ANDI', 'chhipadohar': 'CPDR', 'jhansi jn': 'JHS', 'meramandolil': 'MRDL', 
   'sagardighi': 'SDI', 'aduturai': 'ADT', 'chhulha': 'CLF', 'jhantipahari': 'JPH', 'merta road jn': 'MTD', 'sagauli jn': 'SGL', 'agartala': 'AGTL', 'chidambaram': 'CDM',
   'jhargram': 'JGM', 'metupalaiyam': 'MTP', 'sagoni': 'SAO', 'agori khas': 'AGY', 'chiheru': 'CEU', 'jharsuguda jn': 'JSG', 'metur dam': 'MTDM', 'saharanpur': 'SRE', 
   'agra cantt': 'AGC', 'chikhli': 'CKHS', 'jhinjhak': 'JJK', 'mhasoda dongar': 'MSDG', 'saharsa jn': 'SHC', 'agra city': 'AGA', 'chikjajur jn': 'JRU', 'jiaganj': 'JJG',
    'mhmdvd kheda rd': 'MHD', 'saharsrakund': 'SHSK', 'agra fort': 'AF', 'chikni road': 'CKNI', 'jind jn': 'JIND', 'midnapore': 'MDN', 'sahatwar': 'STW', 'ahmadgarh': 'AHH',
     'chikodi road': 'CKR', 'jiradei': 'ZRDE', 'migrendisa': 'MGE', 'sahibabad': 'SBB', 'ahmadnagar': 'ANG', 'chilakalapudi': 'CLU', 'jirania': 'JRNA', 'mihinpurwa': 'MIN',
     'sahibganj jn': 'SBG', 'ahmadpur jn': 'AMP', 'chilbila jn': 'CIL', 'jmlpr shaikhan': 'JPS', 'mihrawan': 'MIH', 'sahibpur kml jn': 'SKJ', 'ahmedabad jn': 'ADI', 
     'chilikidara': 'CLDR', 'jodhpur jn': 'JU', 'milak': 'MIL', 'sahibzada asngr': 'SASN', 'ahraura road': 'ARW', 'chilka': 'CLKA', 'jogal': 'JOL', 'milavittan': 'MVN',
      'sahjanwa': 'SWA', 'aishbagh': 'ASH', 'chilkahar': 'CHR', 'jogbani': 'JBN', 'minchnal': 'MNL', 'sai p nilayam': 'SSPN', 'ait': 'AIT', 'chima pahad': 'CMW', 
      'jogendranagar': 'JGNR', 'miraj jn': 'MRJ', 'saidraja': 'SYJ', 'aithal': 'ATMO', 'chinchli': 'CNC', 'jogi magra': 'JOM', 'miranpur katra': 'MK', 
      'sainagar shirdi': 'SNSI', 'ajmer jn': 'AII', 'chinchvad': 'CCH', 'jogighopa': 'JPZ', 'mirchadhori': 'MCQ', 'saintala': 'SFC', 'ajni': 'AJNI', 
      'chinna ganjam': 'CJM', 'jolarpettai': 'JTJ', 'mirthal': 'MRTL', 'sainthia': 'SNT', 'akalkot road': 'AKOR', 'chinna salem': 'CHSM', 'jorai': 'JOQ', 
      'miryalaguda': 'MRGA', 'saiyid sarawan': 'SYWN', 'akaltara': 'AKT', 'chiplun': 'CHI', 'jorawarnagar jn': 'JVN', 'mirza cheuki': 'MZC', 'sakaldiha': 'SLD', 'akanapet': 'AKE', 'chipurupalle': 'CPP', 'mirzapali': 'MZL', 'sakhi gopal': 'SIL', 'akbarganj': 'AKJ', 'chirala': 'CLX', 'joychandi pahar': 'JOC', 'mirzapur': 'MZP', 'sakhpur': 'SKR', 'akbarnagar': 'AKN', 'chirayinkil': 'CRY', 'jugaur': 'JRR', 'misrauli': 'MFL', 'sakleshpur': 'SKLR', 'akbarpur': 'ABP', 'chirgaon': 'CGN', 'jugpura': 'JRG', 'misrod': 'MSO', 'sakri jn': 'SKI', 'akividu': 'AKVD', 'chirmiri': 'CHRM', 'jujumura': 'JUJA', 'mithapur': 'MTHP', 'sakrigali jn': 'SLJ', 'akodia': 'AKD', 'chit baragaon': 'CBN', 'jukehi': 'JKE', 'miyagam karjan': 'MYG', 'saktesgarh': 'SKGH', 'akola jn': 'AK', 'chitrakot': 'CKTD', 'julana': 'JNA', 'miyana': 'MINA', 'sakti': 'SKT', 'akshaywat r ngr': 'AYRN', 'chitrod': 'COE', 'junagadh jn': 'JND', 'modinagar': 'MDNR', 'salaia': 'SYA', 'akurdi': 'AKRD', 'chittapur': 'CT', 'junnor deo': 'JNO', 'modnimb': 'MLB', 'salamatpur': 'SMT', 'alai': 'ALJ', 'chittaranjan': 'CRJ', 'jutogh': 'JTO', 'modran': 'MON', 'salar': 'SALE', 'alamnagar': 'AMG', 'chittaurgarh': 'COR', 'jwalapur': 'JWP', 'moga': 'MOGA', 'salauna': 'SLNA', 'alampur': 'ALMR', 'chittoor': 'CTO', 'kabakaputtur': 'KBPR', 'mohadi prgn lng': 'MHAD', 'salboni': 'SLB', 'aler': 'ALER', 'chityala': 'CTYL', 'kacheguda': 'KCG', 'mohanlalganj': 'MLJ', 'salekasa': 'SKS', 'algawan': 'AIG', 'chola': 'CHL', 'kachhia bridge': 'KCO', 'mohitnagar': 'MOP', 'salem jn': 'SA', 'alia bada': 'ALB', 'chopan': 'CPU', 'kadakavur': 'KVU', 'mohiuddinnagar': 'MOG', 'salem town': 'SXT', 'aligarh jn': 'ALJN', 'chorvad road': 'CVR', 'kadalundi': 'KN', 'mohol': 'MO', 'salempur jn': 'SRU', 'alipur duar jn': 'APDJ', 'choti khatu': 'CTKT', 'kadambur': 'KDU', 'mohope': 'MHPE', 'salichauka road': 'SCKR', 'allahabad city': 'ALY', 'chuchura': 'CNS', 'kadaynallur': 'KDNL', 'mokalsar': 'MKSR', 'salkaroad': 'SLKR', 'allahabad jn': 'ALD', 'chunar': 'CAR', 'kadiri': 'KRY', 'mokameh jn': 'MKA', 'salmari': 'SRI', 'alleppey': 'ALLP', 'churaibari': 'CBZ', 'kadiyan': 'KYM', 'mondh': 'MOF', 'salogra': 'SLR', 'almatti': 'LMT', 'churk': 'CUK', 'kadur': 'DRU', 'monu': 'MANU', 'samakhiali b g': 'SIOB', 'alnavar jn': 'LWR', 'churu': 'CUR', 'kahalgaon': 'CLG', 'mookambika road': 'BYNR', 'samalkha': 'SMK', 'aluabari road': 'AUB', 'cinnamara': 'CMA', 'kahiliya': 'KH', 'mor': 'MOR', 'samalkot jn': 'SLO', 'aluva': 'AWY', 'coimbatore jn': 'CBE', 'kaikolur': 'KKLR', 'moradabad': 'MB', 'samalpatti': 'SLY', 'alwar': 'AWR', 'coimbatore nrth': 'CBF', 'kailahat': 'KYT', 'morak': 'MKX', 'samastipur jn': 'SPJ', 'amalner': 'AN', 'colonelganj': 'CLJ', 'kailasapuram': 'KLPM', 'moranhat': 'MRHT', 'samba': 'SMBX', 'amalsad': 'AML', 'cuddalore port': 'CUPJ', 'kaimganj': 'KMJ', 'morappur': 'MAP', 'sambalpur': 'SBP', 'amarda road': 'ARD', 'cuddapah': 'HX', 'kaithalkuchi': 'KTCH', 'morbi': 'MVI', 'sambalpur city': 'SBPY', 'amargarh': 'AGR', 'cumbum': 'CBM', 'kajgaon': 'KJ', 'mordad tanda': 'MWK', 'sambalpur road': 'SBPD', 'amb andaura': 'AADR', 'cuttack': 'CTC', 'kajra': 'KJH', 'morena': 'MRA', 'sambhar lake': 'SBR', 'ambala cant jn': 'UMB', 'dabhaura': 'DBR', 'kajrat nawadih': 'KYF', 'morgram': 'MGAE', 'samdhari jn': 'SMR', 'ambala city': 'UBC', 'dabra': 'DBA', 'kakarghatti': 'KKHT', 'mori bera': 'MOI', 'samlaya jn': 'SMLA', 'ambalapuzha': 'AMPA', 'dabtara': 'DUB', 'kakinada port': 'COA', 'morinda': 'MRND', 'samnapur': 'SMC', 'ambale': 'ABLE', 'dadar': 'DR', 'kakinada town': 'CCT', 'morkadhana': 'MKDN', 'sampla': 'SPZ', 'ambari falakata': 'ABFC', 'kakirigumma': 'KKGM', 'morwani': 'MRN', 'samsi': 'SM', 'ambarnath': 'ABH', 'dadri': 'DER', 'kakori': 'KKJ', 'moth': 'MOTH', 'sanahwal': 'SNL', 'ambasa': 'ABSA', 'dahanu road': 'DRD', 'kala akhar': 'KQE', 'motichur': 'MOTC', 'sanand': 'SAU', 'ambasamudram': 'ASD', 'dahod': 'DHD', 'kalachand': 'KQI', 'motipur': 'MTR', 'sanat nagar': 'SNF', 'ambaturai': 'ABI', 'dakaniya talav': 'DKNT', 'kalanaur kalan': 'KLNK', 'muddanuru': 'MOO', 'sanchi': 'SCI', 'ambika kalna': 'ABKA', 'dakhineswar': 'DAKE', 'kalanwali': 'KNL', 'mudkhed': 'MUE', 'sandila': 'SAN', 'ambikapur': 'ABKP', 'daladi': 'DL', 'kalapipal': 'KPP', 'mughal sarai jn': 'MGS', 'saneh road': 'SNX', 'ambli road': 'ABD', 'dalauda': 'DLD', 'kalhar': 'KAH', 'muhammadabad': 'MMA', 'sangaria': 'SGRA', 'ambodala': 'AMB', 'dalbhumgarh': 'DVM', 'kali sindh': 'KSH', 'muhammadganj': 'MDJ', 'sangat': 'SGF', 'ambur': 'AB', 'dalelnagar': 'DLQ', 'kalianpur': 'KAP', 'mukerian': 'MEX', 'sangli': 'SLI', 'amdara': 'UDR', 'dalgaon': 'DLO', 'kaliyanganj': 'KAJ', 'muktapur': 'MKPR', 'sangmeshwar': 'SGR', 'amethi': 'AME', 'daliganj': 'DAL', 'kalka': 'KLK', 'mukundarayapurm': 'MCN', 'sangola': 'SGLA', 'amgaon': 'AGN', 'dalkolha': 'DLK', 'kallakkudi plgh': 'KKPM', 'mul marora': 'MME', 'sangrur': 'SAG', 'amguri': 'AGI', 'dalli rajhara': 'DRZ', 'kallal': 'KAL', 'mulacalacheruvu': 'MCU', 'sanichara': 'SAC', 'amla jn': 'AMLA', 'dalmau jn': 'DMW', 'kallkiri': 'KCI', 'mulanturutti': 'MNTT', 'sanjan': 'SJN', 'amlai': 'AAL', 'dalsingh sarai': 'DSS', 'kalluru': 'KLU', 'muli road': 'MOL', 'sankarankovil': 'SNKL', 'ammanabrolu': 'ANB', 'daltonganj': 'DTO', 'kalmitar': 'KLTR', 'mulki': 'MULK', 'sankaridurg': 'SGE', 'ammasandra': 'AMSA', 'damanjodi': 'DMNJ', 'kalol': 'KLL', 'multai': 'MTY', 'sankarpur': 'SNQ', 'amoni': 'AONI', 'damchara': 'DCA', 'kalpi': 'KPI', 'sanosra': 'SOA', 'amravati': 'AMI', 'damoh': 'DMO', 'kalunga': 'KLG', 'mumbai cst': 'CSTM', 'sansarpur': 'SNRR', 'amritsar jn': 'ASR', 'danapur': 'DNR', 'kalupara ghat': 'KAPG', 'munabao': 'MBF', 'sant road': 'SAT', 'amroha': 'AMRO', 'danauli phlwria': 'DPL', 'kalyan jn': 'KYN', 'munderwa': 'MND', 'santaldih': 'SNTD', 'anakapalle': 'AKP', 'dandupur': 'DND', 'kalyanpur road': 'KPRD', 'mungaoli': 'MNV', 'santalpur': 'SNLR', 'anand jn': 'ANND', 'danea': 'DNEA', 'kamakhya': 'KYQ', 'muniguda': 'MNGD', 'santragachi jn': 'SRC', 'anand nagar': 'ANDN', 'dangoaposi': 'DPS', 'kamakhyaguri': 'KAMG', 'munirabad': 'MRB', 'sanverdam chuch': 'SVM', 'anand vihar': 'ANVR', 'daniyawan bzr h': 'DNWH', 'kamalapuram': 'KKM', 'munroturuttu': 'MQO', 'sapatgram': 'SPX', 'anand vihar trm': 'ANVT', 'dantan': 'DNT', 'kamalganj': 'KLJ', 'mupa': 'MUPA', 'sapekhati': 'SPK', 'anandapuram': 'ANF', 'daotuhaja': 'DJA', 'kamalnagar': 'KMNR', 'muradnagar': 'MUD', 'saphale': 'SAH', 'anandpur sahib': 'ANSB', 'dapodi': 'DAPD', 'kamalpurgram': 'KLPG', 'murarai': 'MRR', 'saragbundia': 'SRBA', 'anantapur': 'ATP', 'dappar': 'DHPR', 'kamarbandha ali': 'KXL', 'murarpur': 'MPY', 'sarai': 'SAI', 'anaparti': 'APT', 'dara': 'DARA', 'kamareddi': 'KMC', 'murdeshwar': 'MRDW', 'sarai chandi': 'SYC', 'anara': 'ANR', 'darbhanga jn': 'DBG', 'kamarkundu': 'KQU', 'muri': 'MURI', 'sarai kansrai': 'SQN', 'anas': 'ANAS', 'darjeeling': 'DJ', 'kamptee': 'KP', 'muribahal': 'MRBL', 'sarai mir': 'SMZ', 'anavardikhanpet': 'AVN', 'darritola': 'DTL', 'kampur': 'KWM', 'murkeongselek': 'MZS', 'sarangpur': 'SFW', 'andal jn': 'UDL', 'daryabad': 'DYD', 'kamshet': 'KMST', 'murshidabad': 'MBB', 'sarbahara': 'SBRA', 'andheri': 'ADH', 'dasharathpur': 'DRTP', 'kamtaul': 'KML', 'murtajapur': 'MZR', 'sardargram': 'SDGM', 'angadippuram': 'AAM', 'dasuya': 'DZA', 'kanakpura': 'KKU', 'murukkampuzha': 'MQU', 'sardarnagar': 'SANR', 'angamali': 'AFK', 'datia': 'DAA', 'kanalas jn': 'KNLS', 'musafir khana': 'MFKA', 'sardiha': 'SUA', 'angul': 'ANGL', 'daudpur': 'DDP', 'kanas road': 'KASR', 'muzaffarnagar': 'MOZ', 'sareigram': 'SGAM', 'anjar': 'AJE', 'daulatabad': 'DLB', 'kanchipuram': 'CJ', 'muzaffarpur jn': 'MFP', 'sareri': 'SSR', 'anjhi shahabad': 'AJI', 'daulatpur hat': 'DLPH', 'kandaghat': 'KDZ', 'muzzampur nryn': 'MZM', 'sarkoni': 'SIQ', 'ankai': 'ANK', 'daund jn': 'DD', 'kandarpur': 'KDRP', 'mysore jn': 'MYS', 'sarnath': 'SRNT', 'ankleshwar jn': 'AKV', 'daurala': 'DRLA', 'kandra': 'KND', 'n ghaziabad': 'GZN', 'sarupathar': 'SZR', 'ankola': 'ANKL', 'dausa': 'DO', 'kanginhal': 'KGX', 'n. panakudi': 'NPK', 'sasaram': 'SSM', 'ankorah akorha': 'ANH', 'davangere': 'DVG', 'kanhangad': 'KZE', 'nabadwip dham': 'NDAE', 'sasthankotta': 'STKT', 'annavaram': 'ANV', 'debagram': 'DEB', 'kanjari boriyav': 'KBRV', 'nabenagar road': 'NBG', 'satara': 'STR', 'annigeri': 'NGR', 'degana jn': 'DNA', 'kankaha': 'KKAH', 'nabha': 'NBA', 'sathajagat': 'STJT', 'anpara': 'ANPR', 'dehradun': 'DDN', 'kankavali': 'KKW', 'nabipur': 'NIU', 'sathiaon': 'SAA', 'antah': 'ATH', 'dehri on sone': 'DOS', 'kanki': 'KKA', 'nadauj': 'NDU', 'sathin road': 'SWF', 'antu': 'ANTU', 'dehu road': 'DEHR', 'kannapuram': 'KPQ', 'nadbai': 'NBI', 'satna': 'STA', 'anugraha n road': 'AUBR', 'delang': 'DEG', 'kannauj': 'KJN', 'nadiad jn': 'ND', 'satrod': 'STD', 'anuppur jn': 'APR', 'delhi': 'DLI', 'kannur': 'CAN', 'nadikode': 'NDKD', 'sattenapalle': 'SAP', 'aonla': 'AO', 'delhi cantt': 'DEC', 'kanoh': 'KANO', 'nadwan': 'NDW', 'satur': 'SRT', 'ara': 'ARA', 'delhi kishangnj': 'DKZ', 'kanpur anwrganj': 'CPA', 'nagaon': 'NGAN', 'saugor': 'SGO', 'arag': 'ARAG', 'delhi s rohilla': 'DEE', 'kanpur central': 'CNB', 'nagappattinam': 'NGT', 'savarda': 'SVX', 'arakkonam': 'AJJ', 'delhi safdarjng': 'DSJ', 'kanshbahal': 'KXN', 'nagar': 'NGE', 'savarkundla': 'SVKD', 'aralvaymozhi': 'AAY', 'delhi shahdara': 'DSA', 'kansrao': 'QSR', 'nagar untari': 'NUQ', 'savda': 'SAV', 'arariya court': 'ARQ', 'deoband': 'DBD', 'kantabanji': 'KBJ', 'nagari': 'NGI', 'sawai madhopur': 'SWM', 'aravali road': 'AVRD', 'deoghar': 'DGHR', 'kanth': 'KNT', 'sawantwadi road': 'SWV', 'arigada': 'ARGD', 'deori': 'DOE', 'kanthi p h': 'KATI', 'nagaria sadat': 'NRS', 'sayan': 'SYN', 'ariyalur': 'ALU', 'deoria sadar': 'DEOS', 'kanyakumari': 'CAPE', 'nagarsol': 'NSL', 'sbb jogulamba h': 'SBBJ', 'arjuni': 'AJU', 'deotala': 'DOTL', 'kapan': 'KPNA', 'nagarur': 'NRR', 'sealdah': 'SDAH', 'arni road': 'ARV', 'depur ph': 'DPUR', 'kapasan': 'KIN', 'nagarwara': 'NWA', 'secunderabad jn': 'SC', 'arsikere jn': 'ASK', 'derol': 'DRL', 'kapilas road': 'KIS', 'nagaur': 'NGO', 'sehore': 'SEH', 'arumuganeri': 'ANY', 'desari': 'DES', 'kapseti': 'KEH', 'nagbhir jn': 'NAB', 'selu': 'SELU', 'arunachal': 'ARCL', 'deshnok': 'DSO', 'kaptanganj jn': 'CPJ', 'nagda jn': 'NAD', 'semapur': 'SMO', 'asafpur': 'AFR', 'devakottai road': 'DKO', 'kapurthala': 'KXH', 'nager coil town': 'NJT', 'senchoa jn': 'SCE', 'asalpur jobner': 'JOB', 'devbaloda chrda': 'DBEC', 'karad': 'KRD', 'nagercoil jn': 'NCJ', 'sendra': 'SEU', 'asansol jn': 'ASN', 'devlali': 'DVL', 'karagola road': 'CRR', 'nagina': 'NGG', 'sengottai': 'SCT', 'asaoti': 'AST', 'dewanganj': 'DWG', 'karaikal': 'KIK', 'nagireddipalli': 'NRDP', 'seohara': 'SEO', 'asarva jn': 'ASV', 'dewas': 'DWX', 'karaikkudi jn': 'KKDI', 'nagore': 'NCR', 'seoraphuli': 'SHE', 'ashapura gomat': 'AQG', 'dhaban': 'DABN', 'karaila road jn': 'KRLR', 'nagpur': 'NGP', 'seram': 'SEM', 'ashok nagar': 'ASKN', 'dhaca cantt': 'DHCA', 'karajgi': 'KJG', 'nagpur road': 'NPRD', 'serampore': 'SRP', 'asifabad road': 'ASAF', 'dhalgaon': 'DLGN', 'karak bel': 'KKB', 'naharkatiya': 'NHK', 'sevagram': 'SEGM', 'aslana': 'ANA', 'dhamalgaon': 'DMGN', 'karamnasa': 'KMS', 'naihati jn': 'NH', 'sewapuri': 'SWPR', 'asranada': 'AAS', 'dhamangaon': 'DMN', 'karanjgaon': 'KAJG', 'naila': 'NIA', 'seydunganallur': 'SDNR', 'atari': 'ATT', 'dhamara ghat': 'DHT', 'karauta': 'KWO', 'naini': 'NYN', 'shadnagar': 'SHNR', 'atarra': 'ATE', 'dhampur': 'DPR', 'karbigwan': 'KBN', 'nainpur jn': 'NIR', 'shahabad': 'SDB', 'athmal gola': 'ATL', 'dhanauri': 'DNRE', 'karchha': 'KDHA', 'najibabad jn': 'NBD', 'shahbad marknda': 'SHDM', 'attabira': 'ATS', 'dhanbad jn': 'DHN', 'kareli': 'KY', 'nakodar jn': 'NRO', 'shahdol': 'SDL', 'attili': 'AL', 'dhandari kalan': 'DDL', 'karengi': 'KEG', 'naksalbari': 'NAK', 'shahganj jn': 'SHG', 'attur': 'ATU', 'dhanera': 'DQN', 'karepalli': 'KRA', 'nalanda': 'NLD', 'shahjehanpur': 'SPN', 'aung': 'AUNG', 'dhanmandal': 'DNM', 'kargi road': 'KGB', 'nalbari': 'NLV', 'shahpur patoree': 'SPP', 'aunrihar jn': 'ARJ', 'dhansu': 'DNX', 'karhiya bhadeli': 'KYX', 'nalgonda': 'NLDA', 'shajapur': 'SFY', 'aurangabad': 'AWB', 'dhanuvachapuram': 'DAVM', 'karimganj jn': 'KXJ', 'nalhati jn': 'NHT', 'shakti nagar': 'SKTN', 'avadi': 'AVD', 'dharangaon': 'DXG', 'karimnagar': 'KRMR', 'nalwar': 'NW', 'shakurbasti': 'SSB', 'awatarnagar': 'ATNR', 'dharhara': 'DRH', 'karimuddin pur': 'KMDR', 'namburu': 'NBR', 'shalimar': 'SHM', 'ayodhya': 'AY', 'dhariwal': 'DHW', 'karisath': 'KRS', 'namkon': 'NKM', 'sham chaurasi': 'SCQ', 'ayodhyapattanam': 'APN', 'dharmabad': 'DAB', 'karjat': 'KJT', 'namli': 'NLI', 'shamgarh': 'SGZ', 'azamgarh': 'AMH', 'dharmanagar': 'DMR', 'karkeli': 'KKI', 'namrup': 'NAM', 'shamli': 'SMQL', 'azamnagar road': 'AZR', 'dharmapuri': 'DPJ', 'karkheli': 'KEK', 'namtiali': 'NMT', 'shankargarh': 'SRJ', 'azimganj jn': 'AZ', 'dharmavaram jn': 'DMM', 'karmali': 'KRMI', 'nana': 'NANA', 'shankarpalli': 'SKP', 'b cement nagar': 'BEY', 'dharmpur hmchl': 'DMP', 'karna': 'KAR', 'nandalur': 'NRE', 'shedbal': 'SED', 'babatpur': 'BTP', 'dharwar': 'DWR', 'karnal': 'KUN', 'nandganj': 'NDJ', 'shegaon': 'SEG', 'babhnan': 'BV', 'dhasa jn': 'DAS', 'karonji': 'KJZ', 'nandgaon': 'NGN', 'sheikpura': 'SHK', 'babina': 'BAB', 'dhaulpur': 'DHO', 'karpurigram': 'KPGM', 'nandgaon road': 'NAN', 'sheoprasadnager': 'SPDR', 'babrala': 'BBA', 'dhauni': 'DWLE', 'kartarpur': 'KRE', 'nandura': 'NN', 'shertalai': 'SRTL', 'babupeth': 'BUPH', 'dhaura': 'DUA', 'karunagapalli': 'KPY', 'nandurbar': 'NDB', 'shikara': 'SKY', 'bachhrawan': 'BCN', 'dheena': 'DHA', 'karur': 'KRR', 'nandyal': 'NDL', 'shikohabad jn': 'SKB', 'bachwara jn': 'BCA', 'dhemaji': 'DMC', 'karwar': 'KAWR', 'nangal dam': 'NLDM', 'shimoga': 'SME', 'badabandha': 'BDBA', 'dhenkanal': 'DNKL', 'kasara': 'KSRA', 'nangloi': 'NNO', 'shimoga town': 'SMET', 'badami': 'BDM', 'dhilwan': 'DIW', 'kasaragod': 'KGQ', 'nanguneri': 'NNN', 'shirravde': 'SIW', 'badarpur jn': 'BPB', 'dhirera': 'DHRR', 'kasganj': 'KSJ', 'nanpara jn': 'NNP', 'shirud': 'SHF', 'badarwas': 'BDWS', 'dhodhar': 'DOD', 'kashi': 'KEI', 'napasar': 'NPS', 'shiupur': 'SOP', 'badhwa bara': 'BDWA', 'dhodra mohar': 'DOH', 'kashi chak': 'KSC', 'naraina': 'NRI', 'shivaji bridge': 'CSB', 'badla ghat': 'BHB', 'dhola jn': 'DLJ', 'kashipur': 'KPV', 'narangi': 'NNGE', 'shivajinagar': 'SVJR', 'badlapur': 'BUD', 'dholi': 'DOL', 'kasimpur': 'KCJ', 'naranjipur': 'NRGR', 'shivanarayanpur': 'SVRP', 'badli': 'BHD', 'dhone': 'DHNE', 'kastha': 'KSTA', 'naranpur': 'NANR', 'shivnagar': 'SHNG', 'badmal': 'BUDM', 'dhoraji': 'DJI', 'katakhal jn': 'KTX', 'narasapur': 'NS', 'shivpuri': 'SVPI', 'badnapur': 'BDU', 'dhrangdhra': 'DHG', 'katareah': 'KTRH', 'narasaraopet': 'NRT', 'shivrampur': 'SWC', 'badnera jn': 'BD', 'dhubri': 'DBB', 'kathara road': 'KTRR', 'narasingapalli': 'NASP', 'shoghi': 'SGS', 'badodar': 'BDDR', 'dhule': 'DHI', 'kathgodam': 'KGM', 'narayanpet road': 'NRPD', 'sholavandan': 'SDN', 'badshahnagar': 'BNZ', 'dhulian ganga': 'DGLE', 'kathleeghat': 'KEJ', 'narayanpur': 'NNR', 'sholinghur': 'SHU', 'badshahpur': 'BSE', 'dhulkot': 'DKT', 'kathua': 'KTHU', 'naraynpur anant': 'NRPA', 'shoranur jn': 'SRR', 'badulipar': 'BLPR', 'dhupguri': 'DQG', 'katihar jn': 'KIR', 'narela': 'NUR', 'shri ganganagar': 'SGNR', 'bagaha': 'BUG', 'dhuri jn': 'DUI', 'katni': 'KTE', 'nariaoli': 'NOI', 'shri madhopur': 'SMPR', 'bagalkot': 'BGK', 'dhurwasin': 'DRSN', 'katni murwara': 'KMZ', 'narkatiaganj jn': 'NKE', 'shri mahabirji': 'SMBJ', 'bagbahra': 'BGBR', 'dibrugarh': 'DBRG', 'katol': 'KATL', 'narkher': 'NRKR', 'shribdrya lathi': 'SBLT', 'bagdihi': 'BEH', 'dibrugarh town': 'DBRT', 'katora': 'KTO', 'narnaul': 'NNL', 'shridham': 'SRID', 'bagetar': 'BF', 'didwana': 'DIA', 'katpadi jn': 'KPD', 'narsinghpur': 'NU', 'shrigonda road': 'SGND', 'bagevadi rd': 'BSRX', 'digaru': 'DGU', 'katra': 'KEA', 'narsipatnam rd': 'NRP', 'shrirajnagar': 'SAGR', 'baghauli': 'BGH', 'digboi': 'DBY', 'katrasgarh': 'KTH', 'narwana jn': 'NRW', 'shrirangapatna': 'S', 'baghdogra': 'BORA', 'digha flag stn': 'DGHA', 'katwa': 'KWAE', 'nasik road': 'NK', 'shujaatpur': 'SJT', 'baghora': 'BJQ', 'dighwara': 'DGA', 'kaurha': 'KUF', 'nasirabad': 'NSD', 'shujalpur': 'SJP', 'baghuapal': 'BGPL', 'dihakho': 'DKE', 'kavali': 'KVZ', 'nasrala': 'NAS', 'shyampuri': 'SMPA', 'bagnan': 'BZN', 'dilawarnagar': 'DIL', 'kavathe mahankl': 'KVK', 'nathnagar': 'NAT', 'sibsagar town': 'SRTN', 'bagra tawa': 'BGTA', 'dildarnagar jn': 'DLN', 'kavutaram': 'KVM', 'naugachia': 'NNA', 'siddhpur': 'SID', 'bahadur singh w': 'BSS', 'dimapur': 'DMV', 'kayalpattinam': 'KZY', 'naupada jn': 'NWP', 'sigadam': 'SGDM', 'bahadurgarh': 'BGZ', 'dina nagar': 'DNN', 'kayankulam jn': 'KYJ', 'nautanwa': 'NTV', 'sihapar': 'SIPR', 'bahjoi': 'BJ', 'dindigul jn': 'DG', 'kayar': 'KAYR', 'navagadh': 'NUD', 'siho': 'SIHO', 'bahraich': 'BRK', 'diphu': 'DPU', 'kazhakuttam': 'KZK', 'navapur': 'NWU', 'sihor gujarat': 'SOJN', 'baidyanathdham': 'BDME', 'disa': 'DISA', 'kazipet jn': 'KZJ', 'navsari': 'NVS', 'sihora road': 'SHR', 'baiguda': 'BGUA', 'ditokcherra': 'DTC', 'kcg falaknuma': 'FM', 'nawa city': 'NAC', 'sikandra rao': 'SKA', 'baihatola': 'BATL', 'divine nagar': 'DINR', 'keckhi': 'KCKI', 'nawabganj gonda': 'NGB', 'sikar jn': 'SIKR', 'baikunthpur rd': 'BRH', 'diyodar': 'DEOR', 'kedgaon': 'KDG', 'nawadah': 'NWD', 'sikarpai': 'SKPI', 'bairagarh': 'BIH', 'dodballapur': 'DBU', 'kem': 'KEM', 'nawagaon': 'NVG', 'silao': 'SILO', 'baitarani road': 'BTV', 'doiwala': 'DWO', 'kendposi': 'KNPS', 'nawandgi': 'NAW', 'silapathar': 'SPTR', 'bajud': 'BJUD', 'domingarh': 'DMG', 'kendrapara road': 'KNPR', 'nawapara road': 'NPD', 'silaut': 'SLT', 'bajva': 'BJW', 'donakonda': 'DKD', 'kendujhargarh': 'KDJR', 'naya nangal': 'NNGL', 'silchar': 'SCL', 'bakhleta': 'BQQ', 'dondaicha': 'DDE', 'kengeri': 'KGI', 'nayadupeta': 'NYP', 'silghat town': 'SHTT', 'bakhtiyarpur jn': 'BKP', 'dongargarh': 'DGG', 'kesamudram': 'KDM', 'nayagaon': 'NYO', 'siliguri jn': 'SGUJ', 'balaghat jn': 'BTC', 'doraha': 'DOA', 'keshod': 'KSD', 'nayagarh': 'NYG', 'silli': 'SLF', 'balamu jn': 'BLM', 'dornakal jn': 'DKJ', 'keshorai patan': 'KPTN', 'nazareth': 'NZT', 'simaluguri jn': 'SLGR', 'balangir': 'BLGR', 'dubaha': 'DUBH', 'kesinga': 'KSNG', 'nazirganj': 'NAZJ', 'simaria': 'SAE', 'balasore': 'BLS', 'dubrajpur': 'DUJ', 'keutguda': 'KTGA', 'nekonda': 'NKD', 'simbhooli': 'SMBL', 'balawali': 'BLW', 'duddhinagar': 'DXN', 'khachrod': 'KUH', 'nellore': 'NLR', 'simhachalam': 'SCM', 'balharshah': 'BPQ', 'dudhani': 'DUD', 'khada': 'KZA', 'neora': 'NEO', 'simla': 'SML', 'ballabgarh': 'BVH', 'duggirala': 'DIG', 'khadki': 'KK', 'nepanagar': 'NPNR', 'simultala': 'STL', 'ballia': 'BUI', 'duliajan': 'DJG', 'khaga': 'KGA', 'neral': 'NRL', 'sindhudurg': 'SNDD', 'balod': 'BXA', 'dullahapur': 'DLR', 'khagaria jn': 'KGG', 'nergundi': 'NRG', 'sindi': 'SNI', 'balotra jn': 'BLT', 'dumka': 'DUMK', 'khagraghat road': 'KGLE', 'new alipurdaur': 'NOQ', 'sindkheda': 'SNK', 'balpur halt': 'BPRH', 'dumraon': 'DURE', 'khairar jn': 'KID', 'new amravat': 'NAVI', 'sindriblock hut': 'SDBH', 'balugan': 'BALU', 'dumri bihar': 'DMBR', 'khairthal': 'KRH', 'new bongaigaon': 'NBQ', 'singapuram road': 'SPRD', 'balurghat': 'BLGT', 'dumri halt': 'DMRX', 'khajauli': 'KJI', 'new cooch behar': 'NCB', 'singaram': 'SGRM', 'bamhrauli': 'BMU', 'dumuriput': 'DMRT', 'khajuraho': 'KURJ', 'new delhi': 'NDLS', 'singarayakonda': 'SKM', 'bamla': 'BMLL', 'dundi': 'DDCE', 'khalari': 'KLRE', 'new farakka jn': 'NFK', 'singhpur': 'SNGP', 'bamnia': 'BMI', 'dungarpur': 'DNRP', 'khalilabad': 'KLD', 'new guntur': 'NGNT', 'singrauli': 'SGRL', 'bamra': 'BMB', 'dungri': 'DGI', 'khalilpur': 'KIP', 'new jalpaiguri': 'NJP', 'sini jn': 'SINI', 'banahi': 'BYN', 'duraundha jn': 'DDA', 'khalispur': 'KSF', 'new katni jn': 'NKJ', 'sirari': 'SRY', 'banapura': 'BPF', 'durg': 'DURG', 'khallikot': 'KIT', 'new mal jn': 'NMZ', 'sirathu': 'SRO', 'banar': 'BNO', 'durgapur': 'DGR', 'khambhaliya': 'KMBL', 'new maynaguri': 'NMX', 'sirhind jn': 'SIR', 'banaswadi': 'BAND', 'durgapura': 'DPA', 'khammam': 'KMT', 'new misamari': 'NMM', 'sirkazhi': 'SY', 'banbasa': 'BNSA', 'durgauti': 'DGO', 'khana jn': 'KAN', 'new tinsukia jn': 'NTSK', 'sirohi road': 'SOH', 'banda jn': 'BNDA', 'dusi': 'DUSI', 'khanapur': 'KNP', 'neyyattinkara': 'NYY', 'sirpur kagazngr': 'SKZR', 'bandakpur': 'BNU', 'duvvada': 'DVD', 'khandala': 'KAD', 'nidadavolu jn': 'NDD', 'sirpur town': 'SRUR', 'bandanwara': 'BDW', 'dwarapudi': 'DWP', 'khandwa': 'KNW', 'nidamangalam': 'NMJ', 'sirsa': 'SSA', 'bandarkhal': 'BXK', 'dwarka': 'DWK', 'khanna': 'KNN', 'nidubrolu': 'NDO', 'sirsaul': 'SSL', 'bandel jn': 'BDC', 'ekambarakuppam': 'EKM', 'khanna banjari': 'KHBJ', 'nigaura': 'NIQ', 'sisvinhalli': 'SVHE', 'bandikui jn': 'BKI', 'ekangarsarai': 'EKR', 'kharagpur jn': 'KGP', 'nigohan': 'NHN', 'siswa bazar': 'SBZ', 'bandra terminus': 'BDTS', 'ekchari': 'EKC', 'kharak': 'KHRK', 'nihalgarh': 'NHH', 'sitabinj': 'STBJ', 'bangalore cant': 'BNC', 'eklakhi': 'EKI', 'kharia khangarh': 'KXG', 'nilakantheswar': 'NKW', 'sitafal mandi': 'STPD', 'bangalore cy jn': 'SBC', 'ekma': 'EKMA', 'khariar road': 'KRAR', 'nilambur road': 'NIL', 'sitalpur': 'STLR', 'bangalore east': 'BNCE', 'elimala': 'ELM', 'kharsaliya': 'KRSA', 'nileshwar': 'NLE', 'sitamarhi': 'SMI', 'bangarapet': 'BWT', 'ellamanchili': 'YLM', 'kharsia': 'KHS', 'nilokheri': 'NLKR', 'sitapur': 'STP', 'bangriposi': 'BGY', 'eluru': 'EE', 'kharwa chanda': 'KRCD', 'nim ka thana': 'NMK', 'sitapur cant': 'SCC', 'bangrod': 'BOD', 'eranakulam jn': 'ERS', 'khatauli': 'KAT', 'nimach': 'NMH', 'sitapur city': 'SPC', 'bani': 'BANI', 'eraniel': 'ERL', 'khatima': 'KHMA', 'nimbahera': 'NBH', 'sitarampur': 'STN', 'banka': 'BAKA', 'ernakulam town': 'ERN', 'khatipura': 'KWP', 'nimbal': 'NBL', 'siuri': 'SURI', 'banka ghat': 'BKG', 'erode jn': 'ED', 'khatu': 'KHTU', 'nimbhora': 'NB', 'sivaganga': 'SVGA', 'bankata': 'BTK', 'errupalem': 'YP', 'khed': 'KHED', 'nimtita': 'NILE', 'sivakasi': 'SVKS', 'bankhedi': 'BKH', 'etawah': 'ETW', 'kheduli': 'KQW', 'ningala jn': 'NGA', 'siwaith': 'SWE', 'bankura': 'BQA', 'ettapur road': 'ETP', 'kheri salwa': 'KSW', 'niphad': 'NR', 'siwan jn': 'SV', 'banmor': 'BAO', 'ettumanur': 'ETM', 'kherli': 'KL', 'nira': 'NIRA', 'sleemanabad rd': 'SBD', 'bano': 'BANO', 'faizabad jn': 'FD', 'kheta sarai': 'KS', 'nirakarpur': 'NKP', 'snarayan chapia': 'SNC', 'bansipur': 'BSQP', 'faizullapur': 'FYZ', 'khirkiya': 'KKN', 'nisui': 'NSU', 'sohagpur': 'SGP', 'banspani': 'BSPX', 'fakiragram jn': 'FKM', 'khirsadoh jn': 'KUX', 'nivari': 'NEW', 'sohwal': 'SLW', 'bansthali niwai': 'BNLW', 'falakata': 'FLK', 'khodiyar': 'KHD', 'niwar': 'NWR', 'sojat road': 'SOD', 'bantawala': 'BNTL', 'falna': 'FA', 'khodri': 'KOI', 'niwas road': 'NWB', 'solan': 'SOL', 'banthra': 'BTRA', 'farah town': 'FHT', 'khoirabari': 'KBY', 'nizamabad': 'NZB', 'solapur jn': 'SUR', 'bapatla': 'BPP', 'faridabad': 'FDB', 'khongsara': 'KGS', 'noamundi': 'NOMD', 'somesar': 'SOS', 'bapudm motihari': 'BMKI', 'faridabad nw tn': 'FDN', 'khorason road': 'KRND', 'nokha': 'NOK', 'somnath': 'SMNH', 'faridkot': 'FDK', 'khudiram b pusa': 'KRBP', 'norla road': 'NRLR', 'sompeta': 'SPT', 'bara jamda': 'BJMD', 'farrukhabad': 'FBD', 'khumtai': 'KUTI', 'north lakhimpur': 'NLP', 'son nagar': 'SEB', 'barabanki jn': 'BBK', 'fateh singhpura': 'FSP', 'khurai': 'KYE', 'nowrozabad': 'NRZB', 'sonada': 'SAD', 'barabhum': 'BBM', 'fatehgarh': 'FGR', 'khurda road jn': 'KUR', 'nrynpur tatwar': 'NNW', 'sonagir': 'SOR', 'barabil': 'BBN', 'fatehgarh sahib': 'FGSB', 'khurdpur': 'KUPR', 'nsc bose j gomo': 'GMO', 'sonalli': 'SI', 'baradwar': 'BUA', 'fatehnagar': 'FAN', 'khurhand': 'KHU', 'nuagaon': 'NXN', 'sonbarsa kcheri': 'SBM', 'baragopal': 'BAGL', 'fatehpur': 'FTP', 'khurial': 'KWE', 'nujella': 'NUJ', 'sondad': 'SNV', 'barahat': 'BHLE', 'fatehpur sikri': 'FTS', 'khurja city': 'KJY', 'numaligarh': 'NMGY', 'sonegaon': 'SNN', 'baraigram jn': 'BRGM', 'fatwa': 'FUT', 'khurja jn': 'KRJ', 'nunkhar': 'NRA', 'songadh': 'SGD', 'barakar': 'BRR', 'ferok': 'FK', 'khusropur': 'KOO', 'nurmahal': 'NRM', 'soni': 'SONI', 'baral': 'BARL', 'firozabad': 'FZD', 'kila kadaiyam': 'KKY', 'nuzvid': 'NZD', 'sonipat': 'SNP', 'baran': 'BAZ', 'firozpur cant': 'FZR', 'kila raipur': 'QRP', 'obaidulla ganj': 'ODG', 'sonpur jn': 'SEE', 'barang': 'BRAG', 'forbesganj': 'FBG', 'kim': 'KIM', 'obra dam': 'OBR', 'sontalai': 'SQL', 'barara': 'RAA', 'furkating jn': 'FKG', 'kinwat': 'KNVT', 'obulavaripalli': 'OBVP', 'sonua': 'SWR', 'barauni jn': 'BJU', 'fursatganj': 'FTG', 'kiraoli': 'KLB', 'odela': 'OEA', 'sorbhog jn': 'SBE', 'baraut': 'BTU', 'g.ramachandrapu': 'GRCP', 'kiratgarh': 'KRTH', 'okha': 'OKHA', 'soro': 'SORO', 'barbatpur': 'BBTR', 'gachhipura': 'GCH', 'kiratpur sahib': 'KART', 'okhla': 'OKA', 'soron': 'SRNK', 'barchi road': 'BCRD', 'gadag jn': 'GDG', 'kirihrapur': 'KER', 'old malda': 'OMLF', 'sri dungargarh': 'SDGH', 'barddhaman jn': 'BWN', 'gadarwara': 'GAR', 'kirloskarvadi': 'KOV', 'omalur': 'OML', 'sri kalahasti': 'KHT', 'bardoli': 'BIY', 'gadwal': 'GWD', 'kishanganj': 'KNE', 'ondagram': 'ODM', 'srikakulam road': 'CHE', 'bareilly': 'BE', 'gahmar': 'GMR', 'kishangarh': 'KSG', 'ongole': 'OGL', 'srikrishn nagar': 'SKN', 'gajraula jn': 'GJL', 'kishanpur': 'KSP', 'orai': 'ORAI', 'sriramnagar': 'SRNR', 'bareilly city': 'BC', 'galgalia': 'GAGA', 'kiul jn': 'KIUL', 'orga': 'ORGA', 'srirangam': 'SRGM', 'barejadi': 'BJD', 'galudih': 'GUD', 'kochuveli': 'KCVL', 'osiyan': 'OSN', 'srivaikuntam': 'SVV', 'barelipur': 'BQM', 'gamharia': 'GMH', 'kodaikanal road': 'KQN', 'ottappalam': 'OTP', 'srivilliputtur': 'SVPR', 'bareta': 'BRZ', 'ganagapur road': 'GUR', 'koderma': 'KQR', 'pachhapur': 'PCH', 'subedarganj': 'SFG', 'bareth': 'BET', 'ganaur': 'GNU', 'kodiyar mandir': 'KDMR', 'pachor road': 'PFR', 'subrahmanya roa': 'SBHR', 'bargarh': 'BRG', 'gandhidham bg': 'GIMB', 'kodumudi': 'KMD', 'pachora jn': 'PC', 'subzi mandi': 'SZM', 'bargarh road': 'BRGA', 'gandhinagar cap': 'GNC', 'koduru': 'KOU', 'padadhari': 'PDH', 'sudamdih': 'SDMD', 'bargawan': 'BRGW', 'gandhinagar jpr': 'GADJ', 'koelwar': 'KWR', 'padampur': 'PDF', 'sudhani': 'SUD', 'bargi': 'BUQ', 'ganeshganj': 'GAJ', 'koiripur': 'KEPR', 'padubidri': 'PDD', 'sudsar': 'SDF', 'barh': 'BARH', 'gangadharpur': 'GNGD', 'kokrajhar': 'KOJ', 'paharpur': 'PRP', 'suhsarai': 'SOW', 'barharwa jn': 'BHW', 'gangaganj': 'GANG', 'kolaras': 'KLRS', 'pakala jn': 'PAK', 'suisa': 'SSIA', 'barhiya': 'BRYA', 'gangakher': 'GNH', 'kolkata': 'KOAA', 'pakur': 'PKR', 'sujangarh': 'SUJH', 'barhni': 'BNY', 'gangapur city': 'GGC', 'kollam jn': 'QLN', 'palachauri': 'PCLI', 'sujanpur': 'SJNP', 'bari brahman': 'BBMN', 'gangarampur': 'GRMP', 'kollikhutaha': 'KKTA', 'palakkad': 'PGT', 'sukinda road': 'SKND', 'bariarpur': 'BUP', 'gangiwara': 'GNW', 'kolnur': 'KOLR', 'palakkodu': 'PCV', 'sukritipur': 'SQF', 'baripada': 'BPO', 'gangrar': 'GGR', 'kondapalli': 'KI', 'palakollu': 'PKO', 'sulgare': 'SGRE', 'barka kana': 'BRKA', 'gangsar jaitu': 'GJUT', 'kondapuram': 'KDP', 'palam': 'PM', 'sullurupeta': 'SPE', 'barkhera': 'BKA', 'ganj basoda': 'BAQ', 'kopargaon': 'KPG', 'palanpur jn': 'PNU', 'sultanganj': 'SGG', 'barkisalalya': 'BSYA', 'ganj dundwara': 'GWA', 'koparia': 'KFA', 'palasa': 'PSA', 'sultanpur': 'SLN', 'barkur': 'BKJ', 'ganjam': 'GAM', 'koppal': 'KBL', 'palej': 'PLJ', 'sultanpur lodi': 'SQR', 'barlai': 'BLAX', 'garh jaipur': 'GUG', 'korai halt': 'KRIH', 'palghar': 'PLG', 'summer hill': 'SHZ', 'barmer': 'BME', 'garhbeta': 'GBA', 'koraput': 'KRPU', 'palghat town': 'PGTN', 'sumreri': 'SMRR', 'barnala': 'BNN', 'garhi harsaru': 'GHH', 'korba': 'KRBA', 'pali marwar': 'PMY', 'sunam': 'SFM', 'barog': 'BOF', 'garhi manikpur': 'GRMR', 'koregaon': 'KRG', 'palia kalan': 'PLK', 'suraimanpur': 'SIP', 'barpali': 'BRPL', 'garhmuktesar': 'GMS', 'kosamba jn': 'KSB', 'palliyadi': 'PYD', 'surajpur road': 'SJQ', 'barpathar': 'BXP', 'garhwa': 'GHQ', 'kosgi': 'KO', 'palwal': 'PWL', 'surat': 'ST', 'barpeta road': 'BPRD', 'garividi': 'GVI', 'kosi kalan': 'KSV', 'paman': 'PMN', 'suratgarh jn': 'SOG', 'barrackpore': 'BP', 'garla': 'GLA', 'kot kapura': 'KKP', 'pamban jn': 'PBM', 'surathkal': 'SL', 'barrajpur': 'BJR', 'garot': 'GOH', 'kota jn': 'KOTA', 'panagarh': 'PAN', 'surendranagar': 'SUNR', 'barsali': 'BYS', 'garpos': 'GPH', 'kotabommali': 'KBM', 'panch pipila': 'PCN', 'surendranagar g': 'SRGT', 'barsi town': 'BTW', 'garwa road': 'GHD', 'kotalpukur': 'KLP', 'panchgram': 'PNGM', 'surgaon banjari': 'SGBJ', 'barsoi jn': 'BOE', 'gaura': 'GRX', 'kotapar road': 'KPRR', 'pandabeswar': 'PAW', 'suriawan': 'SAW', 'barsola': 'BZO', 'gauri bazar': 'GB', 'kotdwara': 'KTW', 'pandaul': 'PDW', 'suwasra': 'SVA', 'barua bamungaon': 'BBGN', 'gauribidanur': 'GBD', 'kothari road': 'KTHD', 'pandavapura': 'PANP', 'swarupganj': 'SRPJ', 'barud': 'BRUD', 'gauriganj': 'GNG', 'kotikulam': 'KQK', 'pandharpur': 'PVR', 'tadakalpudi': 'TPY', 'barwa sagar': 'BWR', 'gaushala': 'GWS', 'kotli kalan': 'KTKL', 'pandhurna': 'PAR', 'tadali': 'TAE', 'barwadih jn': 'BRWD', 'gautamsthan': 'GTST', 'kotma': 'KTMA', 'paneli moti': 'PLM', 'tadepalligudem': 'TDD', 'barwala': 'BXC', 'gaya jn': 'GAYA', 'kotmi sonan hlt': 'KTSH', 'pangaon': 'PNF', 'tadipatri': 'TU', 'basai': 'BZY', 'gazole': 'GZO', 'kotshila': 'KSX', 'paniahwa': 'PNYA', 'tadwal': 'TVL', 'basantapur': 'BSTP', 'getor jagatpura': 'GTJT', 'kottapalli': 'KYOP', 'panipat jn': 'PNP', 'tahsil fatehpur': 'TSF', 'basar': 'BSX', 'gevra road': 'GAD', 'kottavalasa': 'KTV', 'panki': 'PNK', 'taiabpur': 'TBR', 'basbari': 'BSI', 'ghagwal': 'GHGL', 'kottayam': 'KTYM', 'panoli': 'PAO', 'takari': 'TKR', 'basharatganj': 'BTG', 'ghanauli': 'GANL', 'kovilpatti': 'CVP', 'panposh': 'PPO', 'takia': 'TQA', 'basmat': 'BMF', 'ghanpur': 'GNP', 'kovvur': 'KVR', 'panruti': 'PRT', 'taku': 'TAKU', 'basni': 'BANE', 'gharaunda': 'GRA', 'kozhikode': 'CLT', 'panskura': 'PKU', 'talakhajuri': 'TLKH', 'bassi': 'BAI', 'ghatampur': 'GTM', 'krishanrajanaga': 'KRNR', 'panvel': 'PNVL', 'talbahat': 'TBT', 'bassi pathanam': 'BSPN', 'ghatera': 'GEA', 'krishna': 'KSN', 'papanasam': 'PML', 'talcher': 'TLHR', 'basta': 'BTS', 'ghatprabha': 'GPB', 'krishna canal': 'KCC', 'paradip': 'PRDP', 'talcher road': 'TLHD', 'basti': 'BST', 'ghatsila': 'GTS', 'krishna ch pura': 'KCV', 'paradol': 'PRDL', 'talchhapar': 'TLC', 'basugaon': 'BSGN', 'ghaziabad': 'GZB', 'krishnarajapurm': 'KJM', 'paraiya': 'PRY', 'talegaon': 'TGN', 'basukinath': 'BSKH', 'ghazipur city': 'GCT', 'krishnashilla': 'KRSL', 'paramakkudi': 'PMK', 'talguppa': 'TLGP', 'baswa': 'BU', 'ghoga': 'GGA', 'krishngr cty jn': 'KNJ', 'paras': 'PS', 'taljhari': 'TLJ', 'batala jn': 'BAT', 'ghoksadanga': 'GDX', 'kuchaman city': 'KMNC', 'parashshala': 'PASA', 'talvadya': 'TLV', 'bawal': 'BWL', 'gholvad': 'GVD', 'kuchman': 'KCA', 'parasia': 'PUX', 'talwandi': 'TWB', 'bayana jn': 'BXN', 'ghonsor': 'GNS', 'kudachi': 'KUD', 'parasnath': 'PNME', 'tambaram': 'TBM', 'baytu': 'BUT', 'ghoradongri': 'GDYA', 'kudal': 'KUDL', 'paravur': 'PVU', 'tamluk': 'TMZ', 'bazarsau': 'BZLE', 'ghorpuri': 'GPR', 'kudalnagar': 'KON', 'parbati': 'PRB', 'tanakpur': 'TPU', 'beas': 'BEAS', 'ghughuli': 'GH', 'kudra': 'KTQ', 'parbhani jn': 'PBN', 'tanda urmar': 'TDO', 'beawar': 'BER', 'ghum': 'GHUM', 'kuhuri': 'KUU', 'pardi': 'PAD', 'tandur': 'TDU', 'begampet': 'BMT', 'ghunghuti': 'GGT', 'kulem': 'QLM', 'parewadi': 'PRWD', 'tangiriapal': 'TGRL', 'begu sarai': 'BGS', 'ghutku': 'GTK', 'kulharia': 'KUA', 'parisal': 'PSL', 'tangla': 'TNL', 'behtagokul': 'BEG', 'giddalur': 'GID', 'kulitalai': 'KLT', 'parli vaijnath': 'PRLI', 'tangra': 'TRA', 'bekal fort': 'BFR', 'giddarbaha': 'GDB', 'kulitthurai': 'KZT', 'parmanandpur': 'PMU', 'tanguturu': 'TNR', 'bela': 'BELA', 'gidhaur': 'GHR', 'kulitturai west': 'KZTW', 'parpanangadi': 'PGI', 'tankuppa': 'TKN', 'bela tal': 'BTX', 'gill': 'GILL', 'kulpahar': 'KLAR', 'parsabad': 'PSB', 'tanuku': 'TNKU', 'belakoba': 'BLK', 'giridih': 'GRD', 'kulti': 'ULT', 'parsipur': 'PRF', 'tanur': 'TA', 'belampalli': 'BPA', 'girimaidan': 'GMDN', 'kumardubi': 'KMME', 'parsoda': 'PSD', 'tapa': 'TAPA', 'belapur': 'BAP', 'girwar': 'GW', 'kumarghat': 'KUGT', 'partapgarh jn': 'PBH', 'tapri': 'TPZ', 'belda': 'BLDA', 'goaldih': 'GADH', 'kumarhatti': 'KMTI', 'partur': 'PTU', 'taradevi': 'TVI', 'beldanga': 'BEB', 'goalpara town': 'GLPT', 'kumbakonam': 'KMU', 'parvatipuram': 'PVP', 'tarana road': 'TAN', 'belgahna': 'BIG', 'godavari': 'GVN', 'kumbhraj': 'KHRJ', 'parvatipuram tn': 'PVPT', 'taraori': 'TRR', 'belgaum': 'BGM', 'godhra jn': 'GDA', 'kumbla': 'KMQ', 'pasraha': 'PSR', 'tarapith road': 'TPF', 'belha': 'BYL', 'gogamukh': 'GOM', 'kumedpur': 'KDPR', 'patara': 'PTRE', 'taregna': 'TEA', 'bellary jn': 'BAY', 'gohad road': 'GOA', 'kumta': 'KT', 'pataudi road': 'PTRD', 'targaon': 'TAZ', 'belpahar': 'BPH', 'gohpur': 'GPZ', 'kunda harnamgnj': 'KHNM', 'pathankot': 'PTK', 'tarigoppula': 'TGU', 'belrayan': 'BXM', 'goilkera': 'GOL', 'kundapura': 'KUDA', 'pathardih jn': 'PEH', 'tarikere jn': 'TKE', 'belthara road': 'BLTR', 'gokak road': 'GKK', 'kuneanganj': 'KVG', 'patharia': 'PHA', 'tarlupadu': 'TLU', 'beohari': 'BEHR', 'gokarna road': 'GOK', 'kup': 'KUP', 'patharkandi': 'PTKD', 'tarsarai': 'TRS', 'berchha': 'BCH', 'gola gokaranath': 'GK', 'kupgal': 'KGL', 'pathri': 'PRI', 'taru': 'TR', 'berhampore crt': 'BPC', 'golaghat': 'GLGT', 'kuppam': 'KPN', 'pathsala': 'PBL', 'tatanagar jn': 'TATA', 'bermo': 'BRMO', 'golakganj jn': 'GKJ', 'kurali': 'KRLI', 'patiala': 'PTA', 'tatibahar': 'TBH', 'betamcherla': 'BMH', 'goldinganj': 'GJH', 'kurduvadi': 'KWV', 'patna jn': 'PNBE', 'tatisilwai': 'TIS', 'bethampurdi': 'BTPD', 'gollaprolu': 'GLP', 'kurgunta': 'KQT', 'patna saheb': 'PNC', 'teghra': 'TGA', 'bethuadahari': 'BTY', 'gomati nagar': 'GTNR', 'kurichedu': 'KCD', 'patranga': 'PTH', 'tehta': 'THA', 'betnoti': 'BTQ', 'gomta': 'GTT', 'kurnool town': 'KRNT', 'patratu': 'PTRU', 'telam': 'TQM', 'bettiah': 'BTH', 'gonda jn': 'GD', 'kursela': 'KUE', 'pattambi': 'PTB', 'teliamura': 'TLMR', 'betul': 'BZU', 'kurseong': 'KGN', 'pattikkad': 'PKQ', 'telo': 'TELO', 'bhabhar': 'BAH', 'gondal': 'GDL', 'kurukshetra jn': 'KKDE', 'pavurchutram': 'PCM', 'telta': 'TETA', 'bhabua road': 'BBU', 'gondia jn': 'G', 'kurumbur': 'KZB', 'pawapuri road': 'PQE', 'tenali jn': 'TEL', 'bhachau bg': 'BCOB', 'gondwanavisapur': 'GNVR', 'kusmhi': 'KHM', 'payagpur': 'PDR', 'tenganmada': 'TGQ', 'bhadan': 'BDN', 'goneana': 'GNA', 'kutralam': 'KTM', 'payangadi': 'PAZ', 'tenkasi jn': 'TSI', 'bhadaura': 'BWH', 'gooty': 'GY', 'kuttippuram': 'KTU', 'payyanur': 'PAY', 'tetulmari': 'TET', 'bhadohi': 'BOY', 'gop jam': 'GOP', 'labha': 'LAV', 'payyoli': 'PYOL', 'thakurganj': 'TKG', 'bhadrachalam rd': 'BDCR', 'gorakhnath': 'GRKN', 'lachhmanpur': 'LMN', 'pedakakani halt': 'PDKN', 'thakurtota': 'TKH', 'bhadrak': 'BHC', 'gorakhpur cant': 'GKC', 'lachyan': 'LHN', 'pedana': 'PAV', 'thalassery': 'TLY', 'bhadravati': 'BDVT', 'gorakhpur jn': 'GKP', 'ladhowal': 'LDW', 'peddapalli': 'PDPL', 'thalwara': 'TLWA', 'bhaga jn': 'VAA', 'goraul': 'GRL', 'ladnun': 'LAU', 'peddavadiapudi': 'PVD', 'than jn': 'THAN', 'bhagalpur': 'BGP', 'goraya': 'GRY', 'laheria sarai': 'LSI', 'peddempet': 'PPZ', 'thana bihpur jn': 'THB', 'bhagat ki kothi': 'BGKT', 'gosalpur': 'GSPR', 'lahli': 'LHLL', 'pembarti': 'PBP', 'thandla rd': 'THDR', 'bhagwangola': 'BQG', 'goshainganj': 'GGJ', 'lakadiya': 'LKZ', 'pencharthal': 'PEC', 'thane': 'TNA', 'bhagwanpur': 'BNR', 'gossaigaon hat': 'GOGH', 'lakheri': 'LKE', 'pendekallu': 'PDL', 'thanjavur': 'TJ', 'bhairoganj': 'BRU', 'gotan': 'GOTN', 'lakhimpur': 'LMP', 'pendra road': 'PND', 'therubali': 'THV', 'bhairongarh': 'BOG', 'govindgarh': 'GVG', 'lakhminia': 'LKN', 'pennadam': 'PNDM', 'thiruvarur jn': 'TVR', 'bhakti nagar': 'BKNG', 'govindpur road': 'GBX', 'lakhtar': 'LTR', 'penukonda': 'PKD', 'thivim': 'THVM', 'bhalki': 'BHLK', 'govindpuri': 'GOY', 'laksar jn': 'LRJ', 'peppeganj': 'PJ', 'thrisur': 'TCR', 'bhalui': 'BFM', 'gowdavalli': 'GWV', 'lakshmibai ngr': 'LMNR', 'peralam jn': 'PEM', 'thuria': 'THUR', 'bhaluka road f': 'BKRD', 'gudivada jn': 'GDV', 'lakswa': 'LXA', 'perambur': 'PER', 'tihu': 'TIHU', 'bhalukmara': 'BLMR', 'gudiyattam': 'GYM', 'lal kuan': 'LKU', 'pernem': 'PERN', 'tikiri': 'TKRI', 'bhalumaska': 'BLMK', 'gudlavalleru': 'GVL', 'lalganj': 'LLJ', 'pettaivayatalai': 'PLI', 'tikunia': 'TQN', 'bhanapur': 'BNP', 'gudur jn': 'GDR', 'lalgarh jn': 'LGH', 'phagwara jn': 'PGW', 'tilak bridge': 'TKJ', 'bhandak': 'BUX', 'gujhandi': 'GJD', 'lalgola': 'LGL', 'phalodi jn': 'PLCJ', 'tilaru': 'TIU', 'bhandara road': 'BRD', 'gulabhganj': 'GLG', 'lalgopalganj': 'LGO', 'phaphamau jn': 'PFM', 'tilaya': 'TIA', 'bhandaridah': 'BHME', 'gulabpura': 'GBP', 'lalgudi': 'LLI', 'phaphund': 'PHD', 'tilda': 'TLD', 'bhanvad': 'BNVD', 'gulaothi': 'GLH', 'lalitpur': 'LAR', 'phephna jn': 'PEP', 'tilhar': 'TLH', 'bhanwar tonk': 'BHTK', 'gulbarga': 'GR', 'lalpur jam': 'LPJ', 'phesar': 'PES', 'tiloniya': 'TL', 'bharat kup': 'BTKP', 'guldhar': 'GUH', 'lambhua': 'LBA', 'phillaur jn': 'PHR', 'timarni': 'TBN', 'bharatpur jn': 'BTE', 'guledagudda rd': 'GED', 'lamta': 'LTA', 'phulera jn': 'FL', 'timmapur': 'TMX', 'bharthana': 'BNT', 'gulzarbagh': 'GZH', 'langting': 'LGT', 'phulpur': 'PLP', 'tindivanam': 'TMV', 'bharuch jn': 'BH', 'gumani': 'GMAN', 'lanjigarh road': 'LJR', 'phulwari sharif': 'PWS', 'tinpahar jn': 'TPH', 'bharwa sumerpur': 'BSZ', 'gumia': 'GMIA', 'lanka': 'LKA', 'phulwartanr': 'PLJE', 'tinsukia jn': 'TSK', 'bharwari': 'BRE', 'gummidipundi': 'GPD', 'lar road': 'LRD', 'phusro': 'PUS', 'tipkai': 'TPK', 'bhatapara': 'BYT', 'guna': 'GUNA', 'lasalgaon': 'LS', 'piduguralla': 'PGRL', 'tiptur': 'TTR', 'bhatinda jn': 'BTI', 'gundardehi': 'GDZ', 'lasur': 'LSR', 'pilamedu': 'PLMD', 'tiraldih': 'TUL', 'bhatiya': 'BHTA', 'guntakal jn': 'GTL', 'latehar': 'LTHR', 'piler': 'PIL', 'tirchrpali fort': 'TP', 'bhatkal': 'BTJL', 'guntur jn': 'GNT', 'lathidad': 'LTD', 'pili bangan': 'PGK', 'tirora': 'TRO', 'bhatni jn': 'BTT', 'guramkhedi': 'GMD', 'latur': 'LUR', 'pilibhit jn': 'PBE', 'tiruchchirapali': 'TPJ', 'bhatpar rani': 'BHTR', 'guraru': 'GRRU', 'latur road': 'LTRR', 'pilkhua': 'PKW', 'tiruchendur': 'TCN', 'bhattu': 'BHT', 'gurdaspur': 'GSP', 'laxmipur road': 'LKMR', 'pimpalkhuti': 'PMKT', 'tiruchrpali twn': 'TPTN', 'bhavanagar para': 'BVP', 'gurgaon': 'GGN', 'ledo': 'LEDO', 'pimpri': 'PMP', 'tirukoilur': 'TRK', 'bhavani nagar': 'BVNR', 'gurla': 'GQL', 'lehra gaga': 'LHA', 'pindlai': 'PQL', 'tirumangalam': 'TMQ', 'bhavnagar trmus': 'BVC', 'gurnay': 'GRN', 'leliguma': 'LLGM', 'pindra road': 'PDRD', 'tirunelveli': 'TEN', 'bhawani mandi': 'BWM', 'gurpa': 'GAP', 'lidhora khurd': 'LDA', 'pindrai': 'PDE', 'tirunnavaya': 'TUA', 'bhawanipatna': 'BWIP', 'gurra': 'GRO', 'liliya mota': 'LMO', 'pipalsana': 'PLS', 'tirupadripulyur': 'TDPR', 'bhayavadar': 'BHY', 'gursahaiganj': 'GHJ', 'limbdi': 'LM', 'pipar road jn': 'PPR', 'tiruparankndrm': 'TDN', 'bhedia': 'BDH', 'guruvayur': 'GUV', 'limkheda': 'LMK', 'pipariya': 'PPI', 'tirupati': 'TPTY', 'bheraghat': 'BRGT', 'guskara': 'GKH', 'lingampalli': 'LPI', 'piplia': 'PIP', 'tirupattur jn': 'TPT', 'bhigwan': 'BGVN', 'guwahati': 'GHY', 'lingti': 'LNT', 'piplod jn': 'PPD', 'tiruppur': 'TUP', 'bhilad': 'BLD', 'gwalior': 'GWL', 'loharu': 'LHU', 'pipraich': 'PPC', 'tirur': 'TIR', 'bhilai': 'BIA', 'gyanpur road': 'GYN', 'lohian khas jn': 'LNK', 'pipraigaon': 'PIA', 'tiruttangal': 'TTL', 'bhilai pwr hs': 'BPHB', 'h nizamuddin': 'NZM', 'loisingha': 'LSX', 'piprala': 'PFL', 'tiruttani': 'TRT', 'bhilainagar': 'BQR', 'h sahib nanded': 'NED', 'lokmanyatilak t': 'LTT', 'piravam road': 'PVRD', 'tiruvalla': 'TRVL', 'bhilavdi': 'BVQ', 'habibganj': 'HBJ', 'lonand': 'LNN', 'pirpainti': 'PPT', 'tiruvallur': 'TRL', 'bhildi': 'BLDI', 'hafizpur': 'HZR', 'lonavala': 'LNL', 'pitambarpur': 'PMR', 'tiruvannamalai': 'TNM', 'bhilwara': 'BHL', 'haflong hill': 'HFG', 'londa jn': 'LD', 'pithapuram': 'PAP', 'tiruverumbur': 'TRB', 'bhimadolu': 'BMD', 'haiaghat': 'HYT', 'lorha': 'LOA', 'plassey': 'PLY', 'tisua': 'TSA', 'bhimasar bg': 'BMSB', 'haidarnagar': 'HDN', 'lower haflong': 'LFG', 'pmbakvl shandy': 'PBKS', 'titabar': 'TTB', 'bhimavaram jn': 'BVRM', 'haidergarh': 'HGH', 'luckeesarai jn': 'LKR', 'pocharam': 'PCZ', 'titlagarh': 'TIG', 'bhimavaram town': 'BVRT', 'hajipur jn': 'HJP', 'lucknow city': 'LC', 'podanur jn': 'PTJ', 'tivari': 'TIW', 'bhimsen': 'BZM', 'haldaur': 'HLDR', 'lucknow ne': 'LJN', 'pokhrayan': 'PHN', 'to darjeeling': 'DJRZ', 'bhind': 'BIX', 'haldi road': 'HLDD', 'lucknow nr': 'LKO', 'pokla': 'PKF', 'todarpur': 'TDP', 'bhira kheri': 'BIK', 'haldia': 'HLZ', 'ludhiana jn': 'LDH', 'pokran': 'POK', 'tohana': 'TUN', 'bhitoni': 'BHTN', 'haldibari': 'HDB', 'lumding jn': 'LMG', 'polur': 'PRL', 'tomka': 'TMKA', 'bhiwandi road': 'BIRD', 'haldipada': 'HIP', 'luni jn': 'LUNI', 'ponduru': 'PDU', 'toranagallu': 'TNGL', 'bhiwani': 'BNW', 'haldwani': 'HDW', 'luni richha': 'LNR', 'ponmlai gld rck': 'GOC', 'torang': 'TRAN', 'bhiwani city': 'BNWC', 'halvad': 'HVD', 'lunkaransar': 'LKS', 'porbandar': 'PBR', 'tori': 'TORI', 'bhojipura jn': 'BPR', 'hamira': 'HMR', 'lusa': 'LUSA', 'porjanpur': 'PRNR', 'trikarpur': 'TKQ', 'bhojo': 'BOJ', 'hamirgarh': 'HMG', 'machelipatnam': 'MTM', 'pothahi': 'PFT', 'triupunittura': 'TRTR', 'bhojudih jn': 'BJE', 'hamirpur road': 'HAR', 'madan mahal': 'MML', 'pothia': 'POT', 'trivandrum cntl': 'TVC', 'bhokar': 'BOKR', 'hamitonganj': 'HOJ', 'madanapalle rd': 'MPL', 'potkapalli': 'PTKP', 'trivandrum pett': 'TVP', 'bhongaon': 'BGQ', 'handia khas': 'HDK', 'madar': 'MD', 'potul': 'POZ', 'tsunduru': 'TSR', 'bhongir': 'BG', 'hansi': 'HNS', 'maddikera': 'MKR', 'powerkheda': 'PRKD', 'tuglakabad': 'TKD', 'bhopal jn': 'BPL', 'hanumangarh jn': 'HMH', 'maddur': 'MAD', 'powerpet': 'PRH', 'tuljapur': 'TGP', 'bhoras budrukh': 'BFJ', 'hapa': 'HAPA', 'madgaon': 'MAO', 'prantik': 'PNE', 'tumkur': 'TK', 'bhubaneswar': 'BBS', 'hapur': 'HPU', 'madha': 'MA', 'prayag': 'PRG', 'tumsar road': 'TMR', 'bhuchchu': 'BCU', 'harangajao': 'HJO', 'madhi': 'MID', 'puducherry': 'PDY', 'tundla jn': 'TDL', 'bhugaon': 'BPK', 'harangul': 'HGL', 'madhira': 'MDR', 'pudukad': 'PUK', 'tung': 'TUNG', 'bhuj': 'BHUJ', 'harchandpur': 'HCP', 'madhopur punjab': 'MDPB', 'pudukkottai': 'PDKT', 'tuni': 'TUNI', 'bhulanpur': 'BHLP', 'harda': 'HD', 'madhosingh': 'MBS', 'pugalur': 'PGR', 'turavur': 'TUVR', 'bhupia mau': 'VPO', 'hardas bigha': 'HDE', 'madhubani': 'MBI', 'pulgaon jn': 'PLO', 'tuti melur': 'TME', 'bhurkunda': 'BHKD', 'hardoi': 'HRI', 'madhupur jn': 'MDP', 'pullampet': 'PMT', 'tuticorin': 'TN', 'bhusandpur': 'BSDP', 'hardua': 'HDU', 'madurai jn': 'MDU', 'punarakh': 'PHK', 'tuvvur': 'TUV', 'bhusaval jn': 'BSL', 'harichandanpur': 'HCNR', 'madurantakam': 'MMK', 'pundhag': 'PNW', 'twining ganj': 'TWG', 'bibinagar': 'BN', 'haridwar jn': 'HW', 'madwarani': 'MWRN', 'pundi': 'PUN', 'uchana': 'UCA', 'bichia': 'BIC', 'harihar': 'HRR', 'maghar': 'MHH', 'pune jn': 'PUNE', 'udaipur city': 'UDZ', 'bidadi': 'BID', 'harinagar': 'HIR', 'mahadanapuram': 'MMH', 'punkunnam': 'PNQ', 'udalguri': 'ULG', 'bidar': 'BIDR', 'harippad': 'HAD', 'mahajan': 'MHJ', 'punpun': 'PPN', 'udalkachar': 'UKR', 'bidhan nagar': 'BNXR', 'haripur': 'HP', 'mahanagar': 'MANG', 'punsia': 'PNSA', 'udgir': 'UDGR', 'bighapur': 'BQP', 'harischandrpur': 'HCR', 'mahasamund': 'MSMD', 'puntamba': 'PB', 'udhampur': 'UHP', 'bihar sharif': 'BEHS', 'harishanker rd': 'HSK', 'mahbubabad': 'MABD', 'puranpur': 'PP', 'udhna jn': 'UDN', 'bihara': 'BHZ', 'harmuti': 'HMY', 'mahbubnagar': 'MBNR', 'puri': 'PURI', 'udupi': 'UD', 'bihiya': 'BEA', 'harnaut': 'HRT', 'mahe': 'MAHE', 'purna jn': 'PAU', 'udvada': 'UVD', 'bihta': 'BTA', 'harpalganj': 'HRPG', 'mahendragarh': 'MHRG', 'purnia jn': 'PRNA', 'ugar khurd': 'UGR', 'bijainagar': 'BJNR', 'harpalpur': 'HPP', 'mahes khunt': 'MSK', 'purulia jn': 'PRR', 'ugrasenpur': 'URPR', 'bijapur': 'BJP', 'harrad': 'HRV', 'mahesana jn': 'MSH', 'puttur': 'PUT', 'ujalvav': 'UJ', 'bijaysota': 'VST', 'harrawala': 'HRW', 'maheshmunda': 'MMD', 'pwn klaknder rd': 'PQN', 'ujhani': 'UJH', 'bijni': 'BJF', 'harri': 'HRB', 'mahidpur road': 'MEP', 'quilandi': 'QLD', 'ujiarpur': 'UJP', 'bijnor': 'BJO', 'harsauli': 'HSI', 'mahmudabad avdh': 'MMB', 'radhanpur': 'RDHP', 'ujjain jn': 'UJN', 'bijoor': 'BIJR', 'hasanparthi rd': 'HSP', 'mahoba': 'MBA', 'radhikapur': 'RDP', 'ukhra': 'UKA', 'bijuri': 'BJRI', 'hasanpur road': 'HPO', 'mahuda': 'MHQ', 'rae bareli jn': 'RBL', 'uklana': 'UKN', 'bijwasan': 'BWSN', 'hasimara': 'HSA', 'mahur': 'MXR', 'rafiganj': 'RFJ', 'ulhasnagar': 'ULNR', 'bikaner jn': 'BKN', 'hassan': 'HAS', 'mahuva jn': 'MHV', 'ragaul': 'RGU', 'ullal': 'ULL', 'bikkavolu': 'BVL', 'hathbandh': 'HN', 'maibang': 'MBG', 'raghavapuram': 'RGPM', 'ulubaria': 'ULB', 'bikram shila': 'BKSL', 'hathidah jn': 'HTZ', 'maihar': 'MYR', 'raghunathpalli': 'RGP', 'umar tali': 'UTA', 'bikrampur': 'BMR', 'hathras city': 'HTC', 'mailani': 'MLN', 'raghunathpur': 'RPR', 'umaria': 'UMR', 'bilaspur jn': 'BSP', 'hathras jn': 'HRS', 'mailongdisa': 'MGX', 'umbargam road': 'UBR', 'bilaspur road': 'BLQR', 'hatia': 'HTE', 'mainpuri': 'MNQ', 'raghuraj singh': 'RRS', 'umdanagar': 'UR', 'bildi': 'BILD', 'hatikhali': 'HTL', 'mairwa': 'MW', 'rahama': 'RHMA', 'umed': 'UMED', 'bilga': 'BZG', 'hatkanagale': 'HTK', 'majbat': 'MJBT', 'rahimabad': 'RBD', 'umri': 'UMRI', 'bilhar ghat': 'BLG', 'hatpuraini': 'HPLE', 'majhagawan': 'MJG', 'rahimatpur': 'RMP', 'una himachal': 'UHL', 'bilhaur': 'BLU', 'haveri': 'HVR', 'majhola pakarya': 'MJZ', 'rahuri': 'RRI', 'unchahar jn': 'UCR', 'bilimora jn': 'BIM', 'hazaribagh rd': 'HZD', 'majhowlia': 'MJL', 'raichur': 'RC', 'unchhera': 'UHR', 'bilpur': 'BLPU', 'helem': 'HML', 'majri jn': 'MJRI', 'raiganj': 'RGJ', 'undasa madhawpu': 'UDM', 'bilwai': 'BWI', 'hijilli': 'HIJ', 'makhdumpur gaya': 'MDE', 'raigarh': 'RIG', 'unjalur': 'URL', 'bina jn': '0', 'hilara': 'HLX', 'makhu': 'MXH', 'raigir': 'RAG', 'unjha': 'UJA', 'bindki road': 'BKO', 'hilsa': 'HIL', 'makrana jn': 'MKN', 'raika bagh': 'RKB', 'unnao jn': 'ON', 'binnaguri': 'BNV', 'himayatnagar': 'HEM', 'makronia': 'MKRN', 'raimehatpur': 'MTPR', 'untare road': 'URD', 'biradhwal': 'BDWL', 'himmatana': 'HMI', 'maksi': 'MKC', 'raipur jn': 'R', 'upleta': 'UA', 'birapatti': 'BRPT', 'himmatnagar': 'HMT', 'makudi': 'MKDI', 'rairakhol': 'RAIR', 'uppal': 'OPL', 'birsinghpur': 'BRS', 'hindaun city': 'HAN', 'makum jn': 'MJN', 'raisi': 'RSI', 'uppala': 'UAA', 'birur jn': 'RRB', 'hindupur': 'HUP', 'malakhera': 'MKH', 'raiwala': 'RWL', 'uren': 'UREN', 'bishnathganj': 'BTJ', 'hinganghat': 'HGT', 'malakpet kcg': 'MXT', 'raj gangpur': 'GP', 'urga': 'URGA', 'bishnupur': 'VSU', 'hingoli deccan': 'HNL', 'malancha': 'MLNH', 'raj nandgaon': 'RJN', 'uruli': 'URI', 'bishrampur': 'BSPR', 'hira nagar': 'HRNR', 'malanpur': 'MLAR', 'raja ka sahaspr': 'RJK', 'usalapur': 'USL', 'bisra': 'BZR', 'hirakud': 'HKG', 'malarna': 'MLZ', 'raja ki mandi': 'RKM', 'usmanabad': 'UMD', 'bissamcuttack': 'BMCK', 'hirdagarh': 'HRG', 'malda town': 'MLDT', 'rajaldesar': 'RJR', 'utarlai': 'UTL', 'bisugirsharif': 'BGSF', 'hirnoda': 'HDA', 'malerkotla': 'MET', 'rajamundry': 'RJY', 'utrahtia': 'UTR', 'biswan': 'BVN', 'hisar': 'HSR', 'malhargarh': 'MLG', 'rajanagar': 'RJA', 'uttukuli': 'UKL', 'bitragunta': 'BTTR', 'hodal': 'HDL', 'malhour': 'ML', 'rajapalayam': 'RJPM', 'vadakara': 'BDJ', 'biyavra rajgarh': 'BRRG', 'hojai': 'HJI', 'malihabad': 'MLD', 'rajapur road': 'RAJP', 'vadgaon': 'VDN', 'bobbili': 'VBL', 'hole alur': 'HLAR', 'malipur': 'MLPR', 'rajgarh': 'RHG', 'vadlamannadu': 'VMD', 'bodhadi bujrug': 'BHBK', 'hole narsipur': 'HLN', 'maliya hatina': 'MLHA', 'rajghat narora': 'RG', 'vadodara jn': 'BRC', 'bodwad': 'BDWD', 'honnavar': 'HNA', 'maliya miyana': 'MALB', 'rajgir': 'RGD', 'vaibhavwadi rd': 'VBW', 'bohali': 'BHLI', 'hoshangabad': 'HBD', 'malkajgiri': 'MJF', 'rajgram': 'RJG', 'vaikom': 'VARD', 'bohani': 'BNE', 'hoshiarpur': 'HSX', 'malkapur': 'MKU', 'rajkharsawan jn': 'RKSN', 'vailapuzha': 'VPZ', 'boinda': 'BONA', 'hospet jn': 'HPT', 'malkapur road': 'MALK', 'rajkot jn': 'RJT', 'valapattanam': 'VAPM', 'boisar': 'BOR', 'hosur': 'HSRA', 'malkhaid road': 'MQR', 'rajmane': 'RM', 'valappadi g hlt': 'VGE', 'bokajan': 'BXJ', 'hotgi': 'HG', 'malkhedi': 'MAKR', 'rajpura jn': 'RPJ', 'valivade': 'VV', 'bokaro stl city': 'BKSC', 'howbadh jablpur': 'HBG', 'mallanwala khas': 'MWX', 'rajula jn': 'RLA', 'vallikunnu': 'VLI', 'bokaro thermal': 'BKRO', 'howrah jn': 'HWH', 'mallapur': 'MLP', 'rakha mines': 'RHE', 'valliyur': 'VLY', 'bolarum': 'BMO', 'hubli jn': 'UBL', 'mallarpur': 'MLV', 'ram chaura road': 'RMC', 'valsad': 'BL', 'bolinna doaba': 'BLND', 'hyderabad decan': 'HYB', 'malleswaram': 'MWM', 'ram nagar j k': 'RMJK', 'vanchimaniyachi': 'MEJ', 'bolpur s niktn': 'BHP', 'ichauli': 'ICL', 'mallickpur hat': 'MKRH', 'raman': 'RMN', 'vangaon': 'VGN', 'bommidi': 'BQI', 'ichchpuram': 'IPM', 'malout': 'MOT', 'ramanagaram': 'RMGM', 'vaniyambadi': 'VN', 'bona kalu': 'BKL', 'idaplli': 'IPL', 'malsian shahkht': 'MQS', 'ramanathapuram': 'RMD', 'vaniyambalam': 'VNB', 'bondamunda': 'BNDM', 'idgah agra jn': 'IDH', 'malur': 'MLO', 'ramannapet': 'RMNP', 'vapi': 'VAPI', 'bongaigaon': 'BNGN', 'igatpuri': 'IGP', 'malwan': 'MWH', 'rambha': 'RBA', 'varahi': 'VRX', 'bordhal': 'BXY', 'ikkar': 'IKK', 'maman': 'MOM', 'rambhaddarpur': 'RBZ', 'varanasi city': 'BCY', 'bordi': 'BIO', 'iklehra': 'IKR', 'mambalam': 'MBM', 'ramdevra': 'RDRA', 'varanasi jn': 'BSB', 'borhat': 'BFD', 'indara jn': 'IAA', 'manaksar': 'MNSR', 'rameswaram': 'RMM', 'varangaon': 'VNA', 'boridand': 'BRND', 'indargarh': 'IDG', 'manamadurai jn': 'MNM', 'ramganj mandi': 'RMA', 'varkala': 'VAK', 'borivali': 'BVI', 'indi road': 'IDR', 'mananpur': 'MNP', 'ramgarh cant': 'RMT', 'vartej': 'VTJ', 'borvihir': 'BRVR', 'indore jn bg': 'INDB', 'mananwala': 'MOW', 'ramgarhwa': 'RGH', 'vasad jn': 'VDA', 'botad jn': 'BTD', 'irinjalakuda': 'IJK', 'manaparai': 'MPA', 'ramgundam': 'RDM', 'vasai road': 'BSR', 'brahmapur': 'BAM', 'irugur': 'IGU', 'manauri': 'MRE', 'ramna': 'RMF', 'vasco da gama': 'VSG', 'brajrajnagar': 'BRJN', 'isarda': 'ISA', 'mancheswar': 'MCS', 'ramnagar': 'RMR', 'vedayapalem': 'VDE', 'budalur': 'BAL', 'isarwara': 'ISH', 'manchiryal': 'MCI', 'ramnagar bengal': 'RMRB', 'veer': 'VEER', 'budaun': 'BEM', 'islampur': 'IPR', 'manda road': 'MNF', 'rampur': 'RMU', 'velankanni': 'VLKN', 'buddireddippati': 'BDY', 'ismaila haryana': 'ISM', 'mandagere': 'MGF', 'rampur bazar': 'RMPB', 'vellankanni': 'VLNK', 'budhi': 'BDHY', 'ismailpur': 'IMGE', 'mandal': 'MDL', 'rampur dumra': 'RDUM', 'vellore cant': 'VLR', 'budhlada': 'BLZ', 'itarsi jn': 'ET', 'mandalgarh': 'MLGH', 'rampur hat': 'RPH', 'vendodu': 'VDD', 'budni': 'BNI', 'itola': 'ITA', 'mandamari': 'MMZ', 'rampura phul': 'PUL', 'venkatagiri': 'VKI', 'budvel': 'BDVL', 'itwari': 'ITR', 'mandapam': 'MMM', 'ranaghat jn': 'RHA', 'venkatnagra': 'VKR', 'bulandshahr': 'BSC', 'izzatnagar': 'IZN', 'mandasa road': 'MMS', 'ranapratapnagar': 'RPZ', 'veraval': 'VRL', 'bundi': 'BUDI', 'jabalpur': 'JBP', 'mandasor': 'MDS', 'ranavav': 'RWO', 'verka jn': 'VKA', 'buniadpur': 'BNDP', 'jadcherla': 'JCL', 'mandavalli': 'MDVL', 'ranchi': 'RNC', 'vetapalemu': 'VTM', 'burhanpur': 'BAU', 'jagadhri': 'JUD', 'mandawar m rd': 'MURD', 'ranchi road': 'RRME', 'vidisha': 'BHS', 'burhar': 'BUH', 'jagadhri wshop': 'JUDW', 'manderdisa': 'MYD', 'rangaliting': 'RNGG', 'vidyapatinagar': 'VPN', 'burhwal': 'BUW', 'jagadishpur': 'JGD', 'mandi adampur': 'ADR', 'rangapara north': 'RPAN', 'vidyasagar': 'VDS', 'burnpur': 'BURN', 'jagatbela': 'JTB', 'mandi bamora': 'MABA', 'rangiya jn': 'RNY', 'vijay pur': 'VJP', 'butari': 'BTR', 'jagdalpur': 'JDB', 'mandi dabwali': 'MBY', 'rani': 'RANI', 'vijayawada jn': 'BZA', 'buti bori': 'BTBR', 'jagesharganj': 'JGJ', 'mandi dhanaura': 'MNDR', 'ranibennur': 'RNR', 'vijiypur jammu': 'VJPJ', 'buxar': 'BXR', 'jagi road': 'JID', 'mandi dip': 'MDDP', 'raniganj': 'RNG', 'vikarabad jn': 'VKB', 'byadgi': 'BYD', 'jagraon': 'JGN', 'mandrak': 'MXK', 'raniwara': 'RNV', 'vikramgarh alot': 'VMA', 'c shahumharaj t': 'KOP', 'jai samand road': 'JYM', 'manduadih': 'MUV', 'ranoli': 'RNO', 'vikramnagar': 'VRG', 'cancona': 'CNO', 'jaipur': 'JP', 'mandya': 'MYA', 'ranpur': 'RUR', 'vilavade': 'VID', 'carmelaram': 'CRLM', 'jairamnagar': 'JRMG', 'manendragarh': 'MDGR', 'raoti': 'RTI', 'vilayatkalan rd': 'VYK', 'castle rock': 'CLR', 'jais': 'JAIS', 'mangal mahudi': 'MAM', 'rasra': 'RSR', 'villuparam jn': 'VM', 'chabua': 'CHB', 'jaisalmer': 'JSM', 'mangalagiri': 'MAG', 'rasulabad': 'RUB', 'vindhyachal': 'BDL', 'chachaura bngj': 'CBK', 'jaithari': 'JTI', 'mangalore cntl': 'MAQ', 'rasuriya': 'RYS', 'vinukonda': 'VKN', 'chaibasa': 'CBSA', 'jaitwar': 'JTW', 'mangalore jn': 'MAJN', 'ratangarh jn': 'RTGH', 'viramgam jn': 'VG', 'chainpur': 'CNPR', 'jajiwal': 'JWL', 'mangaon': 'MNI', 'ratanpur': 'RPUR', 'virar': 'VR', 'chainwa': 'CW', 'jajpur k road': 'JJKR', 'mangliya gaon': 'MGG', 'ratanpura': 'RTP', 'viravasaram': 'VVM', 'chajli': 'CJL', 'jakhal jn': 'JHL', 'mangolpuri': 'MGLP', 'rathdhana': 'RDDE', 'virbhadra': 'VRH', 'chakarpur': 'CKK', 'jakhalabandha': 'JKB', 'manikgarh': 'MAGH', 'ratlam jn': 'RTM', 'virpur': 'VRR', 'chakdayala': 'CKDL', 'jakhalaun': 'JLN', 'manikpur jn': 'MKP', 'ratnagiri': 'RN', 'virudunagar jn': 'VPT', 'chakia': 'CAA', 'jakhanian': 'JKN', 'maninagar': 'MAN', 'rauli': 'RUL', 'visapur': 'VPR', 'chakki bank': 'CHKB', 'jakhapura': 'JKPR', 'manjeshwar': 'MJS', 'raver': 'RV', 'vishakapatnam': 'VSKP', 'chakradharpur': 'CKP', 'jakhim': 'JHN', 'manjhi': 'MHT', 'ravindrakhani': 'RVKH', 'vishnupuram': 'VNUP', 'chakulia': 'CKU', 'jakhvada': 'JKA', 'mankapur jn': 'MUR', 'raxaul jn': 'RXL', 'vishrambag': 'VRB', 'chalakudi': 'CKI', 'jalalganj': 'JLL', 'mankar': 'MNAE', 'ray': 'RAY', 'vishvamitri': 'VS', 'chalisgaon jn': 'CSN', 'jalalpur dhai': 'JPD', 'mankatha': 'MKB', 'rayagada': 'RGDA', 'viswanath chrli': 'VNE', 'champa': 'CPH', 'jalamb jn': 'JM', 'manmad jn': 'MMR', 'rayalcheruvu': 'RLO', 'vithisvarankol': 'VDL', 'champaner rd jn': 'CPN', 'jalandhar cant': 'JRC', 'mannargudi': 'MQ', 'rayanapad': 'RYP', 'viveka vihar': 'VVB', 'chand siau': 'CPS', 'jalandhar city': 'JUC', 'manoharganj': 'MNJ', 'raybag': 'RBG', 'vizianagram jn': 'VZM', 'chanda fort': 'CAF', 'jalesar road': 'JLS', 'manoharpur': 'MOU', 'razampeta': 'RJP', 'vridhachalam jn': 'VRI', 'chandan nagar': 'CGR', 'jaleswar': 'JER', 'mansa': 'MSZ', 'rechni road': 'RECH', 'vyara': 'VYA', 'chandauli mjhwr': 'CDMR', 'jalgaon jn': 'JL', 'mansi jn': 'MNE', 'rejinagar': 'REJ', 'vyasnagar': 'VYN', 'chandausi jn': 'CH', 'jalna': 'J', 'manthralayam rd': 'MALM', 'ren': 'REN', 'wadakancheri': 'WKI', 'chanderiya': 'CNA', 'jalor': 'JOR', 'manuguru': 'MUGR', 'rengali': 'RGL', 'wadhwan city': 'WC', 'chandi mandir': 'CNDM', 'jalpaiguri': 'JPG', 'manwath road': 'MVO', 'renigunta jn': 'RU', 'wadi': 'WADI', 'chandia road': 'CHD', 'jalpaiguri road': 'JPE', 'maramjhiri': 'MJY', 'renukut': 'RNQ', 'wadiaram': 'WDR', 'chandigarh': 'CDG', 'jalsu': 'JAC', 'mararikulam': 'MAKM', 'reoti': 'ROI', 'wadrengdisa': 'WDA', 'chandil jn': 'CNI', 'jam jodhpur jn': 'JDH', 'marauda': 'MXA', 'reoti b khera': 'RBK', 'wadsa': 'WSA', 'chandlodiya': 'CLDY', 'jam wanthali': 'WTJ', 'margherita': 'MRG', 'rewa': 'REWA', 'walajah road jn': 'WJR', 'chandok': 'CNK', 'jama': 'JAMA', 'mariahu': 'MAY', 'rewari': 'RE', 'wani': 'WANI', 'chandrakona rd': 'CDGR', 'jamalpur jn': 'JMP', 'mariani jn': 'MXN', 'ringas jn': 'RGS', 'wankaner jn': 'WKR', 'chandranathpur': 'CNE', 'jambara': 'JMV', 'markapur road': 'MRK', 'risama': 'RSA', 'wanparti road': 'WPR', 'chandrapur': 'CD', 'jamdha': 'JMD', 'markona': 'MKO', 'rishikesh': 'RKSH', 'wansjaliya': 'WSJ', 'chandrapura': 'CRP', 'jamikunta': 'JMKT', 'maroli': 'MRL', 'risia': 'RS', 'warangal': 'WL', 'chandur': 'CND', 'jammu tawi': 'JAT', 'marthipalayam': 'MPLM', 'rithi': 'REI', 'wardha jn': 'WR', 'chandur bazar': 'CNDB', 'jamnagar': 'JAM', 'marwar bhinmal': 'MBNL', 'rjndr ngr bihar': 'RJPB', 'waria': 'OYR', 'changanaseri': 'CGY', 'jamtara': 'JMT', 'marwar jn': 'MJ', 'rningr jlpaigri': 'RQJ', 'waris aleganj': 'WRS', 'channapatna': 'CPT', 'jamui': 'JMU', 'marwar lohwat': 'MWT', 'roberts ganj': 'RBGJ', 'warora': 'WRR', 'chanpatia': 'CAI', 'jamunamukh': 'JMK', 'marwar mathanya': 'MMY', 'roha': 'ROHA', 'washim': 'WHM', 'chaparmukh jn': 'CPK', 'janakpur road': 'JNR', 'marwar mundwa': 'MDW', 'rohtak jn': 'ROK', 'wathar': 'WTR', 'charanmahadevi': 'SMD', 'jandiala': 'JNL', 'marwasgram': 'MWJ', 'roorkee': 'RK', 'wazerganj': 'WZJ', 'charegaon': 'CRN', 'jangaon': 'ZN', 'masit': 'MST', 'roshanpur': 'RHN', 'wena': 'WENA', 'charkhi dadri': 'CKD', 'janghai jn': 'JNH', 'maskanwa': 'MSW', 'rotegaon': 'RGO', 'whitefield': 'WFD', 'charlapalli': 'CHZ', 'jangipur road': 'JRLE', 'masudan': 'MSDN', 'rourkela': 'ROU', 'wihirgaon': 'VHGN', 'charvattur': 'CHV', 'janwal': 'JOA', 'masur': 'MSR', 'rowriah sdg': 'RWH', 'wirur': 'WIRR', 'chata': 'CHJ', 'jaora': 'JAO', 'mathura cant': 'MRT', 'rowta bagan': 'RWTB', 'wyndhamganj': 'WDM', 'chatra': 'CTR', 'japla': 'JPL', 'mathura jn': 'MTJ', 'roza jn': 'ROZA', 'yadgir': 'YG', 'chatrapur': 'CAP', 'jaraikela': 'JRA', 'mathurapur': 'MUW', 'rudauli': 'RDL', 'yalvigi': 'YLG', 'chau mahla': 'CMU', 'jarandeshwar': 'JSV', 'matmari': 'MTU', 'rudrapur city': 'RUPC', 'yamuna bdg agra': 'JAB', 'chauk': 'CHOK', 'jarangdih': 'JAN', 'mau aimma': 'MEM', 'rukadi': 'RKD', 'yelhanka jn': 'YNK', 'chaukhandi': 'CHH', 'jaroli': 'JRLI', 'mau jn': 'MAU', 'runkhera': 'RNH', 'yeola': 'YL', 'chaunrah': 'CNH', 'jarwal road': 'JLD', 'mau ranipur': 'MRPR', 'rupamau': 'RUM', 'yerraguntla': 'YA', 'chaura': 'CUX', 'jasidih jn': 'JSME', 'mauhari': 'MZH', 'rupaund': 'RPD', 'yesvantpur jn': 'YPR', 'chauri chaura': 'CC', 'jasra': 'JSR', 'maula ali': 'MLY', 'rupbas': 'RBS', 'yusufpur': 'YFP', 'chausa': 'CSA', 'jaswantnagar': 'JGR', 'maur': 'MAUR', 'rupnagar': 'RPAR', 'zafarabad jn': 'ZBD', 'chautara': 'CROA', 'jath road': 'JTRD', 'mavelikara': 'MVLK', 'rupnarayanpur': 'RNPR', 'zahirabad': 'ZB', 'chauth ka brwra': 'CKB', 'jatinga': 'JTG', 'mavli jn': 'MVJ', 'rupra road': 'RPRD', 'zamania': 'ZNA', 'chawapall': 'CHA', 'jaunpur city': 'JOP', 'mayiladuturai j': 'MV', 'rupsa jn': 'ROP', 'zawar': 'ZW', 'chengalpattu': 'CGL', 'jaunpur jn': 'JNU'} 

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
'and', 'but', 'if', 'or','to', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'into', 'through', 'above',
'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'why', 'how', 'all', 'any',
'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
"don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 
'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

if __name__ == '__main__':
	application.run(debug=True)
