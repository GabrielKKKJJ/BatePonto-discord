import pytz
import discord
from discord.ext import commands
from datetime import datetime, timedelta

class DateTimeConverter:
    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction

    async def date(self):
        fuso_origem = pytz.utc
        fuso_br = pytz.timezone('America/Sao_Paulo')

        if(self.ctx):
            time = self.ctx.message.created_at.replace(tzinfo=fuso_origem)

        elif(self.interaction):
            time = self.interaction.created_at.replace(tzinfo=fuso_origem)

        time = time.astimezone(fuso_br)
        time = time.strftime("%d/%m/%Y")
        return time

    async def hours(self):
        fuso_origem = pytz.utc
        fuso_br = pytz.timezone('America/Sao_Paulo')

        if(self.ctx):
            time = self.ctx.message.created_at.replace(tzinfo=fuso_origem)

        elif(self.interaction):
            time = self.interaction.created_at.replace(tzinfo=fuso_origem)

        time = time.astimezone(fuso_br)
        hour = time.strftime("%H:%M")
        
        return hour
    
    async def dateCalculate(self, date1, hour1, pause_time=None):
        self.pause_time = pause_time
        fuso_origem = pytz.utc
        fuso_br = pytz.timezone('America/Sao_Paulo')
        
        print(self.pause_time)

        if self.ctx:
            date2 = self.ctx.message.created_at.replace(tzinfo=fuso_origem)
        elif self.interaction:
            date2 = self.interaction.created_at.replace(tzinfo=fuso_origem)

        convertedDate1 = datetime.strptime(date1, "%d/%m/%Y")
        convertedHour1 = datetime.strptime(hour1, "%H:%M")

        date2 = date2.astimezone(fuso_br)

        datetime1 = datetime.combine(convertedDate1, convertedHour1.time())
        datetime2 = datetime.combine(date2, date2.time())

        if not self.pause_time:
            diff = datetime2 - datetime1
        else:
            self.pause_time = timedelta(seconds=self.pause_time)
            diff = (datetime2 - datetime1) - self.pause_time

        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        date = {
            "hours": hours, 
            "minutes": minutes, 
            "seconds": seconds} 

        return date
    
    def convert_to_time(self, total_seconds):

        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        total_seconds %= 60
        seconds = total_seconds
        
        return hours, minutes, seconds