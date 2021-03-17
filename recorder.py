import wave
import pyaudio

def record_audio(duration, filename):

    FORMAT = pyaudio.paInt16 
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()
     
    stream = audio.open(format=FORMAT,channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)


    print("Listening...")

    frames = []

    for i in range(int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")
      
    stream.stop_stream() 
    stream.close() 
    audio.terminate()

    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()


def read_audio(filename):
    with open(filename, 'rb') as file:
        audio = file.read()
    return audio
