import requests
from Lib.LucasClass.LucasLogManager import LogManager

class CollegeNetLogIn():
    def __init__(self, LogManage: LogManager) -> None:
        self.LogManage: LogManager = LogManage

class TZCNetLogIn(CollegeNetLogIn):
    def __init__(self, LogManage):
        super().__init__(LogManage)

        self.Logged: bool = False

        self.URLS: dict[str] = {
            'URL_LogInRequest': '', # 此地址仅仅用于响应登录请求, 不返回完整 HTML 页面, 仅返回一个字典.
            'URL_LogOutRequest': '',    # 此地址仅仅用于响应登出请求, 但是返回来自 URL_AuthResult 的完整 HTML 页面.
            'URL_AuthResult': ''    # 此地址用于验证认证登录结果, 返回完整的 HTML 页面.
        }

        self.LogInRequest_Data: dict = {
            'username': '', # 即用户账号.
            'pwd': '',  # 即用户密码.
            # 下面这俩貌似是不变的, 但是不应该啊, MD为什么IP地址还要加个密.
            'nasip': '',   # Nas IP 才疏学浅, 不知道是啥...
            'wlanuserip': ''  # WALN User IP 局域网内IP地址吗?
        }

        self.Cookies_JSESSIONID: dict = {
            'JSESSIONID': ''
        }

    def LogIn(self):
        try:
            # 正确的回复应该是: 
            # {"message":"","nextPage":"goToAuthResult","result":"success"}
            # {"message":"您已经在线！请不要重复认证","nextPage":"goToAuthResult","result":"online"}
            # {"message":"Authentication failed!","nextPage":"","result":"fail"}
            # 表示两种情况, 其中 nextPage 里的 goToAuthResult 是正常网页端登陆后会跳转到的网页地址: http://10.191.250.104:9090/zportal/goToAuthResult
            # 这个地址是用来验证登录结果的?
            response = requests.post(url=self.URLS['URL_LogInRequest'], data=self.LogInRequest_Data, timeout=2)
        except Exception as E:
            Result = [False, 114514, E]
            OutPut = ['Failed', 114514, f'Error({E})']
        else:
            if response.status_code == 200:
                # 貌似是服务器对这次登录请求标记的标识符, 登出的时候要用
                self.Cookies_JSESSIONID['JSESSIONID'] = response.cookies.get('JSESSIONID')
                if response.json()['result'] == 'success':
                    Result = [True, response.status_code, response.json()['message']]   # 认证登录成功
                    OutPut = ['Succeed', response.status_code, response.text]
                if response.json()['result'] == 'online':
                    Result = [True, response.status_code, response.json()['message']]   # 已经处于认证状态
                    OutPut = ['Succeed', response.status_code, response.text]
                if response.json()['result'] == 'fail':
                    Result = [False, response.status_code, response.json()['message']]  # 认证登录失败, 账户或者密码错误
                    OutPut = ['Failed', response.status_code, response.text]
            else:
                Result = [False, response.status_code, response.json()['message']]
                OutPut = ['Failed', response.status_code, response.text]
        finally:
            self.LogManage.LogOutput(Type='LogIn', LogMassage=f'LogInState -> {OutPut[0]}, Status Code -> {OutPut[1]}, Detailed -> {OutPut[2]}.')
            return Result

    def LogOut(self):
        try:
            response = requests.post(url=self.URLS['URL_LogOutRequest'], cookies=self.Cookies_JSESSIONID, timeout=2)
        except Exception as E:
            Result = [False, 114514, E]
            OutPut = ['Failed', 114514, f'Error({E})']
        else:
            if response.status_code == 200 and response.text.find('已下线') != -1:
                Result = [True, response.status_code, '已下线']
                OutPut = ['Succeed', response.status_code, '已下线']
            else:
                Result = [False, response.status_code, 'UnKnow Error']
                OutPut = ['Failed', response.status_code, response.text]
        finally:
            self.LogManage.LogOutput(Type='LogOut', LogMassage=f'LogOutState -> {OutPut[0]}, Status Code -> {OutPut[1]}, Detailed -> {OutPut[2]}.')
            return Result

    def AuthResult(self):
        try:
            response = requests.post(url=self.URLS['URL_AuthResult'], cookies=self.Cookies_JSESSIONID, timeout=2)
        except Exception as E:
            Result = [False, 114514, E]
            OutPut = ['Failed', 114514, f'Error({E})']
        else:
            if response.status_code == 200:
                if response.text.find('欢迎您') != -1:
                    IPStartPos: int = response.text.find('您的IP地址')
                    IPEndPos: int = response.text[IPStartPos:].find('\n') + IPStartPos
                    Detailed: str = response.text[IPStartPos+7: IPEndPos]
                    Result = [True, response.status_code, Detailed]
                    OutPut = ['Succeed', response.status_code, f'IP: {Detailed}']
                elif response.text.find('您已离线，请尝试重新登陆') != -1:
                    Result = [True, response.status_code, '已离线']
                    OutPut = ['Succeed', response.status_code, '已离线']
                else:
                    Result = [False, response.status_code, 'UnKnow Error.']
                    OutPut = ['Failed', response.status_code, response.text]
            else:
                Result = [False, response.status_code, 'UnKnow Error.']
                OutPut = ['Failed', response.status_code, response.text]
        finally:
            self.LogManage.LogOutput(Type='AuthResult', LogMassage=f'GetAuthResult -> {OutPut[0]}, Status Code -> {OutPut[1]}, Detailed -> {OutPut[2]}.')
            return Result


if __name__ == "__main__":
    TestAccount: dict = {
            "ProjectName": "TZC-2161130009",

            "username": "2161130009",
            "pwd": "TMDxiangbudaomima114514",
            "nasip": "db0af31d225781cd152c704281b7e5c6",
            "wlanuserip": "4dc9a7d2aafb54c78b7f23082668127f",
            
            "URL_LogInRequest": "http://10.191.250.104:9090/zportal/login/do",
            "URL_LogOutRequest": "http://10.191.250.104:9090/zportal/logout",
            "URL_AuthResult": "http://10.191.250.104:9090/zportal/goToAuthResult"
        }


    LogManage = LogManager(OutPutPath_Root='Log')
    _TZCNetLogIn = TZCNetLogIn(LogManage=LogManage)
    
    for Key in _TZCNetLogIn.URLS.keys():
        _TZCNetLogIn.URLS[str(Key)] = TestAccount[str(Key)]

    for Key in _TZCNetLogIn.LogInRequest_Data.keys():
        _TZCNetLogIn.LogInRequest_Data[str(Key)] = TestAccount[str(Key)]

    _TZCNetLogIn.LogIn()
    _TZCNetLogIn.AuthResult()
    _TZCNetLogIn.LogOut()
    _TZCNetLogIn.AuthResult()
    _TZCNetLogIn.LogIn()
    _TZCNetLogIn.AuthResult()
