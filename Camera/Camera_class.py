import numpy as np 
import cv2
import time
import sys

class Camera:

    def __init__(self, address, res, fps, mjpeg=True):
        '''Инициализация камеры
        ### Args
            address: str/int адрес камеры (/dev/video*); (0)
            res: int разрешение камеры (H, W)
            fps: int FPS камеры
            mjpeg: bool получать кадр в MJPEG или RAW
        '''

        if sys.platform.startswith("linux"):
            self.camera = cv2.VideoCapture(address, cv2.CAP_V4L2)
            print(f"Camera: OS type Linux")
        elif sys.platform.startswith("win32"):
            self.camera = cv2.VideoCapture(address, cv2.CAP_DSHOW)
            print(f"Camera: OS type Win32")
        else:
            print(f"Camera: unknown OS type")

        if mjpeg:
            self.camera.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc('M','J','P','G'))
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.camera.set(3, res[0])
        self.camera.set(4, res[1])

        # Вывод информации о разрешении
        print(f"Camera: Init")
        print(f"Camera: Resolution {str(self.camera.get(3))} x {str(self.camera.get(4))}")
        print(f"Camera: FPS {str(self.camera.get(cv2.CAP_PROP_FPS))}")

        # Создание дополнительных переменных
        self.zerosFrame = np.zeros((res[1], res[0], 3), np.uint8)
        self.frame = self.zerosFrame.copy()
        self.cam_mistake = False


    def read_frame(self):
        '''Получение кадра с камеры
        ### Returns
            ret, frame: bool, int8 numpy array (3, H, W)
        '''

        # Пытаемся получить кадр
        try:
            ret, self.frame = self.camera.read() 
            # Проверка, что получили кадр 
            if ret:
                self.cam_mistake = False
            else:
                self.cam_mistake = True
                print(f"Camera: Not Grabbed")
                time.sleep(0.01)
        # Ошибка
        except:
            self.cam_mistake = True
            print(f'Camera: Read Mistake')
            time.sleep(0.01)

        # Нет ошибки, возвращаем True и кадр
        if not self.cam_mistake:
            return(True, self.frame)
        else: # Ошибка, возвращаем False и пустой кадр
            return(False, self.zerosFrame)
           

    def exit(self):
        '''Деинициализация камеры'''
        self.camera.release()
        print(f"Camera: Close")


def check_class():
    '''Проверка работы класса'''

    ADDRESS = 0
    CAM_RES = (640, 480)
    FPS = 30
    MJPEG = True
    camera = Camera(ADDRESS, CAM_RES, FPS, MJPEG)

    try:
        while True:
            ret, frame = camera.read_frame()
            cv2.imshow('Frame', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'): 
                break
    except KeyboardInterrupt:
        pass

    camera.exit()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    check_class()