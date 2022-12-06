class Logger():
    def __init__(self, fileName) -> None:
        self.fileName = fileName
        self.initFile()
    
    def initFile(self):
        try:
            open(self.fileName, "x")
        except:
            print(f"[LOGGER] {self.fileName} file was already there")

    def addLog(self, log):
        with open(self.fileName, 'a') as file:
            file.write('[LOG]'+str(log)+'\n')
    
    def addWarn(self, log):
        with open(self.fileName, 'a') as file:
            file.write('[WARN]'+str(log)+'\n')

    def addError(self, log):
        with open(self.fileName, 'a') as file:
            file.write('[ERROR]'+str(log)+'\n')