import platform
import os
from dotenv import load_dotenv


def get_print_time():
    import time
    return time.strftime(r'%m.%d.%Y %H:%M:%S', time.localtime())


sys_platform = platform.system()

if sys_platform == 'Darwin':
    PATH = '/Users/yichizhang/Documents/Code/quick_escape'

elif sys_platform == 'Linux':
    PATH = '/root/QuickEscape'

else:
    PATH = ''
    print(f"Unknown platform {sys_platform}")


load_dotenv()
BOOKING_COM_API_HOST = os.getenv('BOOKING_COM_API_HOST')
BOOKING_COM_API_KEY = os.getenv('BOOKING_COM_API_KEY')