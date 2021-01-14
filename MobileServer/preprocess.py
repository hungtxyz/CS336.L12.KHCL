from pydub import AudioSegment
from pydub.playback import play

def crop_music(src):

    sound = AudioSegment.from_file(src)
    output = []

    if (sound.duration_seconds > 60):

        dst = [['audio.mp3',"0:30",'1:00'],['audio2.mp3','1:10','1:50']]

        for x in dst:
            try:
                sound = AudioSegment.from_file(src)
                start_time = (int(x[1].split(':')[0])*60+int(x[1].split(':')[1]))*1000
                stop_time = (int(x[2].split(':')[0])*60+int(x[2].split(':')[1]))*1000
                sound = sound[start_time:stop_time]

                result = src.replace('.mp3','.wav')
                sound.export(result, format="wav")
                output.append(result)

            except:
                pass
    else:
        result = src.replace('.mp3','.wav')
        sound.export(result, format="wav")
        output.append(result)
        output.append(src)
    return output

if __name__ == '__main__':
    src = './music/ALL9.mp3'
    crop_music(src)
