from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

def crop_music(src):

    sound = AudioSegment.from_file(BytesIO(src))
    output = []

    if (sound.duration_seconds > 60):

        dst = [['audio.mp3',"0:30",'0:50'],['audio2.mp3','1:10','1:30']]

        for x in dst:
            try:
                sound = AudioSegment.from_file(BytesIO(src))
                start_time = (int(x[1].split(':')[0])*60+int(x[1].split(':')[1]))*1000
                stop_time = (int(x[2].split(':')[0])*60+int(x[2].split(':')[1]))*1000
                sound = sound[start_time:stop_time]

                result = './static/query/' + x[0]
                sound.export(result, format="mp3")
                output.append(result)

            except:
                pass
    else:
        result = './static/query/audio.mp3'
        sound.export(result, format='mp3')
        output.append(result)
    return output

# if __name__ == '__main__':
#     src = './music/ALL9.mp3'
#     crop_music(src)
