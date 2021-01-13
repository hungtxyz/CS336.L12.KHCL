import speech_recognition as sr
from spleeter.separator import Separator

def Speech_to_Text(filename):
    r = sr.Recognizer()
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(filename,'./static/query/')
    filename = filename[:-4] + '/vocals.wav'
    harvard = sr.AudioFile(filename)
    try:
        with harvard as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)

        output=r.recognize_google(audio,language="vi-VN")
        print(output.lower())
        return output.lower()
    except:
        print('Không nhận dạng được!')
        return ""

# if __name__ == '__main__':
#     filename= './query/audio.wav'
#     print(Speech_to_Text(filename))
