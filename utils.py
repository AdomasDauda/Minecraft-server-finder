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
        try:
            with open(self.fileName, 'a') as file:
                file.write('[LOG]'+str(log)+'\n')
        except FileNotFoundError:
            self.initFile()

    def addWarn(self, log):
        try:
            with open(self.fileName, 'a') as file:
                file.write('[WARN]'+str(log)+'\n')
        except FileNotFoundError:
            self.initFile()

    def addError(self, log):
        try:
            with open(self.fileName, 'a') as file:
                file.write('[ERROR]'+str(log)+'\n')
        except FileNotFoundError:
            self.initFile()