import platform

def get_print_time():
    import time
    return time.strftime(r'%m.%d.%Y %H:%M:%S', time.localtime())


sys_platform = platform.system()

if sys_platform == 'Darwin':
    from webdriver_manager.chrome import ChromeDriverManager

    PATH = '/Users/yichizhang/Documents/Code/quick_escape'
    CHROMEDRIVER_PATH = ChromeDriverManager().install()

elif sys_platform == 'Linux':
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(1600, 1200))
    display.start()

    PATH = '/root/QuickEscape'
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'

else:
    PATH = ''
    CHROMEDRIVER_PATH = ''
    print(f"Unknown platform {sys_platform}")
