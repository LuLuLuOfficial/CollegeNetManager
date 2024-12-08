class RetrieveNetworkInfo():
    def __init__(self) -> None:
        self.RNI_Origin: str = None
        self.RNI_OriginList: list[str] = []
        self.RNI_InfoDict: dict = {}
        self.RNI_Networks: list = []
        self.RNI_WorkedNetworks: list = []
        self.Refresh()
    
    def Refresh(self)->None:
        self.GetRNI_OriginInfo()
        self.FormatRNI_ToList()
        self.FormatRNI_ToDict()

    def GetRNI_OriginInfo(self)-> None:
        import subprocess
        self.RNI_Origin = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True).stdout

    def FormatRNI_ToList(self)-> None:
        RNI_Origin = '\n' + self.RNI_Origin

        SingleRNI_Start = -1
        SingleRNI_End = -1
        for n in range(len(RNI_Origin)):
            num = n
            if RNI_Origin[n: n+5] == '\n\n   ':
                if SingleRNI_Start == -1:
                    while num >= 0:
                        num -= 1
                        if RNI_Origin[num-1] == '\n':
                            SingleRNI_Start = num
                            break
                else:
                    while num >= 0:
                        num -= 1
                        if RNI_Origin[num: num+2] == '\n\n':
                            SingleRNI_End = num
                            self.RNI_OriginList.append(RNI_Origin[SingleRNI_Start: SingleRNI_End])
                            SingleRNI_Start = SingleRNI_End + 2
                            break
            if (num+1) == len(RNI_Origin):
                    SingleRNI_End = num
                    self.RNI_OriginList.append(RNI_Origin[SingleRNI_Start: SingleRNI_End])

    def FormatRNI_ToDict(self, language: str = None)-> None:
        # system_language = en|zh
        import locale

        def POPKeyWords(Origin: list[str], KeyWords: str):
            for n in range(len(Origin)):
                if Origin[n].find(KeyWords) != -1:
                    Origin[n] = Origin[n][: Origin[n].find(KeyWords)]
        def Get_TargetInfo(SingleNetworkInfo: str, KeyWord: str)-> list[str]:
            TargetInfo: list[str] = []
            SingleInfo_Start: int = -1
            SingleInfo_End: int = -1
            SearchAnchor = SingleNetworkInfo.find(KeyWord)
            if SearchAnchor != -1 and SingleNetworkInfo[SearchAnchor-4: SearchAnchor] == '\n   ':
                for n in range(SearchAnchor+len(KeyWord), len(SingleNetworkInfo)):
                    if SingleInfo_Start == -1:
                        if SingleNetworkInfo[n: n+2] == ': ' and SingleNetworkInfo[n+2] != '\n':
                            SingleInfo_Start = n+2
                    if SingleInfo_Start != -1:
                        if SingleNetworkInfo[n] == '\n':
                            SingleInfo_End = n
                            TargetInfo.append(SingleNetworkInfo[SingleInfo_Start: SingleInfo_End])
                            SingleInfo_Start = -1
                    if SingleInfo_End != -1:
                        if SingleNetworkInfo[SingleInfo_End: SingleInfo_End+5] == '\n    ':
                            SearchAnchor = SingleInfo_End+5
                            while SingleNetworkInfo[SearchAnchor] == ' ':
                                SearchAnchor += 1
                            if SingleNetworkInfo[SearchAnchor] != ' ':
                                SingleInfo_Start = SearchAnchor
                        else:
                            break
            return TargetInfo
        '''
        CMD_ipconfig[NIC_Name] = {
            'NIC_Name': NIC_Name,
            'IPv6_Address': NIC_IPv6Address,
            'IPv4_Address': NIC_IPv4Address,
            'Default_Gateway': NIC_DefaultGateway
        }
        '''
        zh: list[str] = ['IPv6 地址', 'IPv4 地址', '默认网关', '(首选)']
        en: list[str] = ['IPv6 Address', 'IPv4 Address', 'Default Gateway', '(Preferred)']
        language: dict = {'Chinese (Simplified)_China': zh, 'English_United Kingdom': en}
        system_language = locale.getlocale()
        Lang = language[system_language[0]]

        SearchAnchor: int = -1

        RNI_OriginList = self.RNI_OriginList[1:]
        for SingleNetworkInfo in RNI_OriginList:
            NIC_Name: str = None
            IPv6_Address: list[str] = []
            IPv4_Address: list[str] = []
            Default_Gateway: list[str] = []

            # NIC_Name
            SearchAnchor = SingleNetworkInfo.find(':\n\n   ')
            if SearchAnchor != -1:
                NIC_Name = SingleNetworkInfo[0: SearchAnchor]

            # IPv6_Address
            IPv6_Address = Get_TargetInfo(SingleNetworkInfo, Lang[0])

            # IPv4_Address
            IPv4_Address = Get_TargetInfo(SingleNetworkInfo, Lang[1])

            # Default_Gateway
            Default_Gateway = Get_TargetInfo(SingleNetworkInfo, Lang[2])

            for n in [IPv6_Address, IPv4_Address, Default_Gateway]:
                POPKeyWords(n, Lang[3])

            self.RNI_InfoDict[NIC_Name] = {
            'IPv6_Address':  IPv6_Address,
            'IPv4_Address':  IPv4_Address,
            'Default_Gateway':  Default_Gateway
            }
            
        self.RNI_Networks = list(self.RNI_InfoDict.keys())
        self.Get_WorkedNetworks()

    def Get_WorkedNetworks(self):
        self.RNI_WorkedNetworks = []
        for Network in self.RNI_Networks:
            if self.RNI_InfoDict[Network]['IPv6_Address'] == True or self.RNI_InfoDict[Network]['IPv4_Address']:
                if self.RNI_InfoDict[Network]['Default_Gateway']:
                    self.RNI_WorkedNetworks.append(Network)

if __name__ == '__main__':
    Test = RetrieveNetworkInfo()
    for n in Test.RNI_WorkedNetworks:
        print(n)
        print(Test.RNI_InfoDict[n])
        print('----------------------------------------------------------------------------------------------------')
    print(Test.RNI_WorkedNetworks)