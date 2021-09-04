import vk_api
from time import sleep

class vk_collection:
    sessions=[]
    ind=0
    sleep_t=0
    
    def __init__(self,**kwargs):
        if('sleep' in kwargs):
            self.sleep_t=kwargs['sleep']
        with open('temp/data.txt','r') as f:
            print('initing vk accounts')
            for line in f:
                login,password = line.split()
                print('initing '+login)
                self.sessions.append(vk_api.VkApi(login,password))
                self.sessions[-1].auth()
            print('done initing vk accounts')
   
    def get_session(self):
        if (len(self.sessions) == 0):
            print("No more sessions")
            quit()
        self.ind+=1
        self.ind%=len(self.sessions)
        return self.sessions[self.ind]

    def call(self,method,method_args,res,**kwargs):
        if(self.sleep_t!=0):
            sleep(self.sleep_t)
        while(True):
            try:
                return res(self.get_session().method(method,values=method_args), **kwargs)
            except Exception as ex:
                print(ex.error['error_msg'])
                if(ex.code in (29,6,14,)):
                    print("LOG: Changing session")
                    del self.sessions[self.ind-1] #get_session увеличила ind
                    self.ind%=len(self.sessions)
                else:
                    print("LOG: Skip the request")
                    return None
