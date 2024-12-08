from json import load, dump

from Lib.LucasClass.LucasLogManager import LogManager
from Lib.LucasClass.LucasException import KeyNotExists, KeyAlreadyExists
from Lib.LucasFunc.LucasFunc import PathCheck

'''
只能处理需要的结构层级只有一层的Json文件(示例如下)
{
    "Key": "Value"
}
对于相对"Value"更低的层级的键值对需要在外部处理
'''

# 为保证数据最新,对Json的任何写操作都会优先进行一次对Json的读取

class ConfigRW():
    '''By json'''
    def __init__(self, LogManage: LogManager, Path_Config: str):
        if not PathCheck(Path_Config): return 

        self.__LogManage: LogManager =LogManage

        self.__Path_Config: str = Path_Config

        self.__Data: dict = {}
        self.__Keys: list = []

        self.ReadConfig()

    @property
    def Data(self): return self.__Data

    @property
    def Keys(self): return self.__Keys

    def ReadConfig(self, Path_Config: str = None, Mode: int = 1):    
        '''Mode = 1 -> First Time To Read The Profile.\n
           Mode = 0 -> Read To Refresh The Profile.'''
        if Path_Config: self.__Path_Config: str = Path_Config
        with open(self.__Path_Config, 'r', encoding='utf-8') as file:
            self.__Data = load(file)
        self.__Keys: list = list(self.__Data.keys())
        if Mode: self.__LogManage.LogOutput(Type='ConfigRW', LogMassage='Profile Data Has Been Loaded.')
        else: self.__LogManage.LogOutput(Type='ConfigRW', LogMassage='Profile Data Has Been Refresh.')

    def SaveConfig(self):
        '''Saved The Contents Of self.__Data To Config File.'''
        with open(self.__Path_Config, 'w', encoding='utf-8') as file:
            dump(self.__Data, file, indent=4, ensure_ascii=False)
        self.__LogManage.LogOutput(Type='ConfigRW', LogMassage='Saved Data To Config File.')

    def Read_ByKey(self, Key: str):
        if Key in self.__Keys: return self.__Data[Key]
        else: raise KeyNotExists()

    def Add_KaV(self, Key: str, Value: dict|str):
        self.ReadConfig(Mode=0) # 数据更新
        if Key in self.__Keys: raise KeyAlreadyExists()
        else:
            self.__Data[Key] = Value
            self.__Keys = self.__Data.keys()
            self.SaveConfig()
        self.__LogManage.LogOutput(Type='ConfigRW', LogMassage='Adding New Key-Value Pairs To Config.')
    
    def Change_KoV(self, OriginKey: str, NewKey: str = '', NewValue: dict|str = ''):
        self.ReadConfig(Mode=0) # 数据更新
        if OriginKey in self.__Keys:
            if NewKey:
                NewData: dict = {}
                for Key in self.__Keys:
                    if Key == OriginKey:
                        if NewValue: NewData[NewKey] = NewValue
                        else: NewData[NewKey] = self.__Data[Key]
                    else:
                        NewData[Key] = self.__Data[Key]
                self.__Data = NewData
                self.__Keys = self.__Data.keys()
            elif NewValue:
                self.__Data[OriginKey] = NewValue
        else: raise KeyNotExists()
        self.SaveConfig()

    def Change_Key(self, OriginKey: str, NewKey: str):
        self.ReadConfig(Mode=0) # 数据更新
        if OriginKey in self.__Keys:
            NewData: dict = {}
            for Key in self.__Keys:
                if Key == OriginKey:
                    NewData[NewKey] = self.__Data[Key]
                else:
                    NewData[Key] = self.__Data[Key]
            self.__Data = NewData
            self.__Keys = self.__Data.keys()
        else: raise KeyNotExists()
        self.SaveConfig()

    def Change_Value(self, Key: str = None, Value: dict|str = None):
        self.ReadConfig(Mode=0) # 数据更新
        if Key in self.__Keys:
            self.__Data[Key] = Value
            with open(self.__Path_Config, 'w', encoding='utf-8') as file:
                dump(self.__Data, file, indent=4, ensure_ascii=False)
        else: raise KeyNotExists()
        self.SaveConfig()

    def Delete_KaV(self, Key: str):
        self.ReadConfig(Mode=0) # 数据更新
        if Key in self.__Keys:
            self.__Data.pop(Key)
            self.__Keys = self.__Data.keys()
        else: raise KeyNotExists()
        self.SaveConfig()
        
if __name__ == '__main__':
    Path_Config: str = r'Ztest\Config_Test.json'
    LogManage = LogManager(OutPutPath_Root=r'Log')
    Test_ConfigRW = ConfigRW(LogManage=LogManage, Path_Config=Path_Config)
    print(f'Keys:\n\t{Test_ConfigRW.Keys}\nData\n\t{Test_ConfigRW.Data}')
    Test_ConfigRW.Add_KaV('Test_Add_KaV', 'Test_Add_KaV_Value')
    Test_ConfigRW.Change_Key('Config', 'Test_Change_Key')
    Test_ConfigRW.Change_KoV('Icon', 'Test_Change_KoV_1')
    Test_ConfigRW.Change_KoV('Lang', 'Test_Change_KoV_2', 'Test_Change_KoV_2_Value')
    Test_ConfigRW.Change_Value('RequestHeaders', 'Test_Change_Value')
    Test_ConfigRW.Delete_KaV('User')
    print(f'Keys:\n\t{Test_ConfigRW.Keys}\nData\n\t{Test_ConfigRW.Data}')
