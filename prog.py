import pystray, array, math, pyaudio, threading

from PIL import Image, ImageDraw
from pystray import Menu as menu, MenuItem as item
from pyaudio import paFloat32 as paf32

class GenerateSinewave(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.p = pyaudio.PyAudio()
        self.data = data
    
    def run(self):
        if (not self.data): return

        stream = self.p.open(format=paf32,
                        channels=1,
                        rate=44100,
                        output=True)
        while(output_enabled):
            stream.write(self.data)
        stream.close()
        self.p.terminate()

    def set_data(self, data):
        self.data = data


def create_sinewave(frequency, volume, fs=44100, duration=0.1):
    # generate samples, note conversion to float32 array
    num_samples = int(fs * duration)
    samples = [volume * math.sin(2 * math.pi * k * frequency / fs) for k in range(0, num_samples)]
    output_bytes = array.array('f', samples).tobytes()
    return output_bytes


output_enabled = False
state_freq = 25
state_vol = 1

def on_clicked(icon, item):
    global output_enabled
    output_enabled = not item.checked
    
    icon.icon = create_image(64, 64, "green") if output_enabled else create_image(64, 64, "red")
    output_bytes = create_sinewave(state_freq*1000, state_vol*0.01)
    GenerateSinewave(output_bytes).start()

def create_image(width, height, color1):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)

    return image

def destroy_all():
    global output_enabled
    output_enabled = False
    icon.stop()


def main():

    def set_state_freq(v):
        def inner(icon, item):
            global state_freq
            state_freq = v
        return inner

    def get_state_freq(v):
        def inner(item):
            return state_freq == v
        return inner
    
    def set_state_vol(v):
        def inner(icon, item):
            global state_vol
            state_vol = v
        return inner

    def get_state_vol(v):
        def inner(item):
            return state_vol == v
        return inner
    
    global icon
    icon = pystray.Icon('test', create_image(64, 64, 'red'), menu=menu(
        item(
            'Enable keepalive output',
            on_clicked,
            checked=lambda item: output_enabled),
        item(
            'Frequency',
            menu(
                item(
                    '20 kHz',
                    set_state_freq(20),
                    checked=get_state_freq(20),
                    radio=True),
                item(
                    '22 kHz',
                    set_state_freq(22),
                    checked=get_state_freq(22),
                    radio=True),
                item(
                    '25 kHz',
                    set_state_freq(25),
                    checked=get_state_freq(25),
                    radio=True),
                item(
                    '1 kHz (test)',
                    set_state_freq(1),
                    checked=get_state_freq(1),
                    radio=True),
            )),
        item(
            'Volume',
            menu(
                item(
                    '0.01%',
                    set_state_vol(1),
                    checked=get_state_vol(1),
                    radio=True),
                item(
                    '0.1%',
                    set_state_vol(10),
                    checked=get_state_vol(10),
                    radio=True),
                item(
                    '0.5%',
                    set_state_vol(50),
                    checked=get_state_vol(50),
                    radio=True),
                item(
                    '1%',
                    set_state_vol(100),
                    checked=get_state_vol(100),
                    radio=True),
            )),
        item(
            'Quit',
            action=destroy_all)
    ))
    icon.run()

if __name__ == "__main__":
    main()