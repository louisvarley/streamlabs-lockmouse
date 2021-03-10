import clr
import sys
import json
import os
import ctypes
import codecs
import time
from ctypes import *



ScriptName = "Lock Mouse"
Website = "https://github.com/louisvarley/streamlabs-lockmouse"
Description = "Lock Mouse"
Creator = "Louis Varley"
Version = "1.0.2"

configFile = "config.json"
settings = {}
commandLength = 0
voiceParams = ""

def ScriptToggled(state):
	return

def Init():
	global settings, commandLength, ScriptName
 
	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!swap",
			"permission": "Everyone",
			"costs": 100,
			"voiceVolume": 50,
			"voiceRate": 0,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 1,
            "lockDuration": 2,
			"onCooldown": "$user, $command is still on cooldown for $cd  seconds!",
			"userCooldown": 300,
			"onUserCooldown": "$user $command is still on user cooldown for $cd seconds!",
			"responseNotEnoughPoints": "$user you need $cost $currency to use $command.",
			"responseOnSuccess": "$user has locked the mouse for $lockDuration seconds.",			
		}
	
	commandLength = len(settings["command"]) + 1
	
def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		costs = settings["costs"]

		if (costs > Parent.GetPoints(userId)):
			outputMessage = settings["responseNotEnoughPoints"]
		elif settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
			if settings["useCooldownMessages"]:
				if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
					cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onCooldown"]
				else:
					cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
			else:
				outputMessage = ""
		else:
			Parent.RemovePoints(userId, username, costs)

			outputMessage = settings["responseOnSuccess"]
			
			userMessage = data.Message[commandLength:]

			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

		outputMessage = outputMessage.replace("$cost", str(costs))
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$lockDuration", str(settings["lockDuration"]))
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])

		Parent.SendStreamMessage(outputMessage)

		Tick()
        
		ok = windll.user32.BlockInput(True) #enable block
		time.sleep(int(settings["lockDuration"]))
		ok = windll.user32.BlockInput(False) #disable block         
        
        
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def Tick():
	return
