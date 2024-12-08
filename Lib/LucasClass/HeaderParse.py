from Lib.LucasClass.LucasLogManager import LogManager

class HeaderParse():
    def __init__(self, LogManage: LogManager):
        self.LogManage: LogManager = LogManage

        self.Path_RequestHeaders: str = ''
        self.Path_Account: str = ''

        self.Name_RequestHeader: str = ''   # File Name was f'{Name_RequestHeader}.txt'
        self.School: str = ''

        self.RequestHeaders: dict = {}

    def SetBase(self, Name_RequestHeader: str, School: str):
        self.Name_RequestHeader = Name_RequestHeader
        self.School = School

    def GetHeader(self):
        pass

    def SaveToHeaders(self):
        pass

    def ParseHeader(self):
        pass

    def SaveToAccount(self):
        pass

class HeaderParse_TZC(HeaderParse):
    def __init__(self, LogManage):
        super().__init__(LogManage)

        self.RequestHeaders: dict[dict[str]] = {
                "goToAuthResult": {
                    "Routine": "",
                    "RequestHeader": "",
                    "ResponseHeader": ""
                },
                "login": {
                    "Routine": "",
                    "RequestHeader": "",
                    "ResponseHeader": ""
                },
                "logout": {
                    "Routine": "",
                    "RequestHeader": "",
                    "ResponseHeader": ""
                }
        }

    def GetHeader(self, Mode: str, RequestHeader: dict):
        self.RequestHeaders[Mode] = RequestHeader
        LogManage.LogOutput()

    def SaveToHeaders(self):
        pass

    def ParseHeader(self):
        pass

    def SaveToAccount(self):
        pass

if __name__ == "__main__":
    LogManage = LogManager(OutPutPath_Root='Log')
    _HeaderParse_TZC = HeaderParse_TZC(LogManage)
    _HeaderParse_TZC.SetHeader()
