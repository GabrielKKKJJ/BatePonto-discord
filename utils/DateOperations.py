import pytz
import discord
from discord.ext import commands
from datetime import datetime, timedelta

class DateTimeConverter:
    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction

    async def date(self):
        """
        returns the current date in Brazil
        """

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
        """
        returns the current hour in Brazil
        """
        
        fuso_origem = pytz.utc
        fuso_br = pytz.timezone('America/Sao_Paulo')

        if(self.ctx):
            time = self.ctx.message.created_at.replace(tzinfo=fuso_origem)

        elif(self.interaction):
            time = self.interaction.created_at.replace(tzinfo=fuso_origem)

        time = time.astimezone(fuso_br)
        hour = time.strftime("%H:%M")
        
        return hour
    
    async def dateCalculate(self, DataInicial, HoraInicial, DataFinal, HoraFinal ,pause_time=None):
        """
        Calculates the time and returns it in hours, minutes, and seconds
        """

        self.pause_time = pause_time

        initial_date = datetime.strptime(DataInicial, "%d/%m/%Y")
        initial_hour = datetime.strptime(HoraInicial, "%H:%M")

        final_date = datetime.strptime(DataFinal, "%d/%m/%Y")
        final_hour = datetime.strptime(HoraFinal, "%H:%M")



        initial_datetime = datetime.combine(initial_date, initial_hour.time())
        final_datetime = datetime.combine(final_date, final_hour.time())
        
        if not self.pause_time or final_date == initial_date:
            diff = final_datetime - initial_datetime
        else:
            self.pause_time = timedelta(seconds=self.pause_time)
            diff = (final_datetime - initial_datetime) - self.pause_time

        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        date = {
            "hours": hours, 
            "minutes": minutes, 
            "seconds": seconds} 

        return date
    
    def convert_to_time(self, total_seconds):
        """
        Convert seconds to hours, minutes, and seconds
        """

        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        total_seconds %= 60
        seconds = total_seconds
        
        return hours, minutes, seconds