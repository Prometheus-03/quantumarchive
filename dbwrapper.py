from databasestuff import GuildDB
class Guild:
    def __init__(self):
        self.id=None
        self.prefix=None
        self.autorole=None
        self.db=GuildDB()

    def load(self,data:dict):
        self.db.set_collection("guilds")
        for attribute in data.keys():
            if attribute == "id":
                self.id = data["id"]
            elif attribute == "prefix":
                self.prefix = data["prefix"]
            elif attribute == "autorole":
                self.autorole = data["autorole"]

    def change(self,attribute:str,newval):
        if attribute=="prefix":
            self.prefix=newval
        elif attribute=="autorole":
            self.autorole=newval

    async def send(self):
        await self.db.add_collection("guilds")
        await self.db.delete(id=self.id)
        await self.db.insert(id=self.id,prefix=self.prefix,autorole=self.autorole)

    def __str__(self):
        return ("<Guild id={},prefix={},autorole={}>".format(self.id,self.prefix,self.autorole))

class Member:
    def __init__(self):
        self.author=None
        self.bumps=0
        self.premium=False
        self.db=GuildDB()

    def load(self,data:dict):
        self.db.set_collection("bumps")
        for attribute in data.keys():
            if attribute == "author":
                self.author = data["author"]
            elif attribute == "bumps":
                self.prefix = data["bumps"]
            elif attribute == "premium":
                self.autorole = data["premium"]

    def change(self,attribute:str,newval):
        if attribute == "author":
            self.author = newval
        elif attribute == "bumps":
            self.prefix = newval
        elif attribute == "premium":
            self.autorole = newval

    async def send(self):
        await self.db.add_collection("bumps")
        await self.db.delete(author=self.author)
        await self.db.insert(author=self.author,bumps=self.prefix,premium=self.premium)

    def __str__(self):
        return ("<Member author={},bump count={},premium={}>".format(self.author,self.bumps,self.premium))