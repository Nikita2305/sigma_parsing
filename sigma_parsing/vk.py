import vk_api
from time import sleep
# ОСТОРОЖНО!!!!!!!!!!!!!!!!!!! ЗАХАРДХОЖЕНО НАЗВАНИЕ ФАЙЛА НА 3 СТРОЧКИ НИЖЕ!!!!!!!!!!!!!!!!
class vk_collection:
    sessions=[]
    ind=0
    sleep_t=0
    def __init__(self,**kwargs):
        if('sleep' in kwargs):
            self.sleep_t=kwargs['sleep']
        with open('accounts.secret.txt','r') as f:
            print('initing vk accounts')
            for line in f:
                login,password = line.split()
                print('initing '+login)
                self.sessions.append(vk_api.VkApi(login,password))
                self.sessions[-1].auth()
            print('done initing vk accounts')
    def get_session(self):
        self.ind+=1
        self.ind%=len(self.sessions)
        return self.sessions[self.ind]
    def call(self,f,method,*args,**kwargs):
        if(self.sleep_t!=0):
            sleep(self.sleep_t)
        repl=None
        while(repl==None):
            try:
                repl=self.get_session().method(method,values=args[-1])
            except Exception as ex:
                print('Error ',ex.code)
                print(ex.error['error_msg'])
                if(ex.code in (29,)):
                    del self.sessions[self.ind-1] #get_session увеличила ind
                    self.ind%=len(self.sessions)
        return repl

def shit():
    pass

vk = vk_collection()
print(vk.call(shit,'users.get',{'user_id':5634918762784}))
