from asyncio import tasks
import json
import discord
import requests
from datetime import datetime
from discord.ext import tasks
settings = json.load(open("settings.json"))
class Bot(discord.Client):
    lastmessage = None
    async def on_ready(self):
        print("Connected")
        self.currentWallet.start()

    async def on_message(self, message):
        if message.author == client.user:
            return
        await self.currentWallet()
        
    @tasks.loop(hours=1)
    async def currentWallet(self):
        message = ""
        kanal = self.get_channel(849781234318049331)
        gesamt = 0
        lastGesamt = 0
        for price in settings["LastPrice"]:
            response = requests.get(f"https://api.coinbase.com/v2/prices/{price}-EUR/spot")
            response = json.loads(response.text)
            amount = settings["wallet"][price]
            currentPrice = round(float(response["data"]["amount"])*amount,2)
            lastPrice = round(settings["LastPrice"][price]*amount,2)
            message += f"{self.getEmoji(currentPrice, lastPrice)} **{price}**: {lastPrice} ---> {currentPrice}\n"
            settings["LastPrice"][price] = float(response["data"]["amount"])
            gesamt+=currentPrice
            lastGesamt+=lastPrice
        message += "------------------------------------------------\n"
        message += f"{self.getEmoji(gesamt, lastGesamt)} **Total**: {round(lastGesamt,2)} ---> {round(gesamt,2)}\n"
        json.dump(settings, open("settings.json", "w"))
        if self.lastmessage != None:
            await self.lastmessage.delete()
        self.lastmessage = await kanal.send(message)
    def getEmoji(self, currentPrice, lastPrice):
        if lastPrice < currentPrice:
            return "📈"
        elif lastPrice > currentPrice:
            return "📉"
        else:
            return "=="

client = Bot()
client.run(settings["token"])