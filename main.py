from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from pyzbar.pyzbar import decode
import webbrowser

class QrScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.ids.qr_image  # Get the image widget from the KV file
        self.scan_button = self.ids.scan_button  # Get the scan button
        self.capture = cv2.VideoCapture(0)  # Open camera
        self.scanning = True  # Flag to control scanning
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update at 30 FPS

    def update(self, dt):
        if not self.scanning:
            return  # Stop scanning if QR is already detected

        ret, frame = self.capture.read()
        if ret:
            # Decode QR code
            decoded_objects = decode(frame)
            if decoded_objects:
                url = decoded_objects[0].data.decode('utf-8')
                webbrowser.open(url)  # Open link in browser
                print(f"Scanned: {url}")
                self.scanning = False  # Stop scanning once a QR is found

            # Convert frame to Kivy texture
            frame = cv2.flip(frame, 0)  # Flip for correct orientation
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture  # Update the UI image

    def scan_another(self):
        """Resets scanning so a new QR code can be detected."""
        self.scanning = True  # Restart scanning
        print("Ready to scan another QR code!")

class QrScannerApp(App):
    def build(self):
        return QrScanner()

if __name__ == "__main__":
    QrScannerApp().run()
 