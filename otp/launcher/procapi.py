# File: p (Python 2.4)

import ctypes
from ctypes.wintypes import *
TH32CS_SNAPPROCESS = 2
INVALID_HANDLE_VALUE = -1
cwk = ctypes.windll.kernel32

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('cntUsage', DWORD),
        ('th32ProcessID', DWORD),
        ('th32DefaultHeapId', HANDLE),
        ('th32ModuleID', DWORD),
        ('cntThreads', DWORD),
        ('th32ParentProcessID', DWORD),
        ('pcPriClassBase', LONG),
        ('dwFlags', DWORD),
        ('szExeFile', c_char * MAX_PATH)]


class ProcessEntryPY:
    
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid



def getProcessList():
    hProcessSnap = cwk.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    processList = []
    if hProcessSnap != INVALID_HANDLE_VALUE:
        pe32 = PROCESSENTRY32()
        pe32.dwSize = sizeof(pe32)
        if cwk.Process32First(hProcessSnap, ctypes.byref(pe32)):
            while None:
                if not cwk.Process32Next(hProcessSnap, ctypes.byref(pe32)):
                    break
                    continue
        
        cwk.CloseHandle(hProcessSnap)
    
    return processList

