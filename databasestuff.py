import motor.motor_asyncio as amotor
import asyncio
class GuildDB:
    def __init__(self):
        self.client=amotor.AsyncIOMotorClient("mongodb+srv://quantum:dZ8cy4LU7FcSsTzp@quantumpy-k5ws8.gcp.mongodb.net/test?retryWrites=true")
        self.db=self.client['Guildstore']
        self.collections=[]
        self.collection=""
    async def add_collection(self,name:str):
        self.collections+=[name]
        self.collection=name
        if name not in (await self.db.list_collection_names()):
            await self.db.create_collection(name=name)
    async def remove_collection(self,name:str):
        self.collections.remove(name)
        await self.db.drop_collection(name)
    def set_collection(self,name:str):
        self.collection=name
    async def insert(self,**kwargs):
        await self.db[self.collection].insert_one(kwargs)
    async def insert_many(self,*items):
        for i in items:
            await self.insert(**i)
    async def delete(self,**kwargs):
        await self.db[self.collection].delete_many(kwargs)
    async def find(self,length=1000,**kwargs):
        cursor=self.db[self.collection].find(kwargs)
        res=[]
        for doc in await cursor.to_list(length=length):
            res.append(doc)
        return res
    async def print_db(self):
        res=[]
        for i in (await self.find()):
            temp=[]
            for x in i.keys():
                if i!="_id":temp+=[x+":"+str(i[x])]
            res+=[",".join(temp)]
        return "\n".join(res)

'''async def main():
    db=GuildDB()
    await db.add_collection("guilds")
    await db.insert(name="Test",content="woop")
    await db.insert_many({"name":"sebi","content":"gay"},{"name":"agg","content":"gayer"})
    await db.delete()
    m=await db.print_db()

if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(main())'''