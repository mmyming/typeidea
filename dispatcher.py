
class Dispatcher:
    cmds ={}
    def reg(self,cmd,fn):
        self.cmds[cmd] =fn

    def run(self):

        while True:
            cmd = input('>>>').strip()
            if cmd == 'quit':
                break
            getattr(self,cmd,self.defaultfn)()

    def defaultfn(self):

        print('Not Found')

if __name__ == '__main__':

    Dispatcher().run()
