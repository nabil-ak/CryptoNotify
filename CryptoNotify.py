from asyncio import tasks
import json
import discord
import requests
from datetime import datetime
from discord.ext import tasks
settings = json.load(open("settings.json"))
class Bot(discord.Client):

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
        kanal = self.get_channel(settings["channelID"])
        total = 0
        lastTotal = 0
        message += "------------------------------------------------------------------\n"
        for price in settings["LastPrice"]:
            response = requests.get(f"https://api.coinbase.com/v2/prices/{price}-EUR/spot")
            response = json.loads(response.text)

            amount = settings["wallet"][price]
            lastExchangerate = settings["LastPrice"][price]
            currentExchangerate = float(response["data"]["amount"])
            currentPrice = round(currentExchangerate*amount,2)
            lastPrice = round(lastExchangerate*amount,2)

            message += f"{self.getEmoji(currentPrice, lastPrice)} **{price}**: {lastPrice}€ ---> {currentPrice}€ | {lastExchangerate}€ ---> {currentExchangerate}€ | **{self.getPercent(lastPrice,currentPrice)}%**\n"
            settings["LastPrice"][price] = float(response["data"]["amount"])
            total+=currentPrice
            lastTotal+=lastPrice
        message += "------------------------------------------------------------------\n"
        message += f"{self.getEmoji(total, lastTotal)} **Total**: {round(lastTotal,2)}€ ---> {round(total,2)}€ | **{self.getPercent(lastTotal,total)}%**\n"
        json.dump(settings, open("settings.json", "w"))
        messages = await kanal.history(limit=200).flatten()
        await kanal.delete_messages(messages)
        await kanal.send(message)

    def getEmoji(self, currentPrice, lastPrice):
        if lastPrice < currentPrice:
            return "📈"
        elif lastPrice > currentPrice:
            return "📉"
        else:
            return "=="
    def getPercent(self, lastprice, newprice):
        return round((100/lastprice)*(newprice-lastprice),2)

client = Bot()
client.run(settings["token"])