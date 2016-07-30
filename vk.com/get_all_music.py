import requests
import os
import vk
import time


class AudioUtils:
    def save_audios_list(self, audios):
        filename = input("Enter filename for the list: ")
        lines = []
        for audio in audios:
            lines.append("{} - {} {}\n".format(audio['artist'], audio['title'], audio['url']))
        with open(filename, "w") as file:
            file.writelines(lines)
            print('Audios list was saved')

    def download_audio(self, audio, path):
        name = '{} - {}'.format(audio['artist'], audio['title'])
        print('Downloading %s ...' % name)
        r = requests.get(audio['url'])

        filename = "{path}/{name}.mp3".format(path=path, name=name)
        try:
            file = open(filename, "wb")
            response = requests.get(audio['url'])
            file.write(response.content)
            file.close()
        except:
            print("Failed to download %s" % name)



class VKApp:
    def __init__(self):
        self.app_id = '5568867'
        self.acess_token = 'bcJejGASHS5XDZ2xnuku'
        self.session = None
        self.api = None
        self.scope = ['offline', 'audio']

    def login(self):

        self.session = vk.InteractiveAuthSession(app_id = self.app_id, access_token = self.acess_token, scope=self.scope)
        self.api = vk.API(self.session)

    def download_user_music(self):
        user_id = input("User ID:")
        print("Fetching audios")

        audios = self.api.audio.get(owner_id=user_id, need_user=0, offset=0, count=6000)
        count = audios[0]
        offset = len(audios) - 1

        if offset < 0:
            print("Cannot get audio list.")
            return False

        audios = audios[1:]

        last_fetched = offset
        print("Fetched {} audios from {}".format(offset, count))

        while count > offset > 0:
            time.sleep(1)
            tmp_audios = self.api.audio.get(owner_id=user_id, need_user=0, offset=offset, count=count)
            last_fetched = len(tmp_audios) - 1
            if last_fetched > 0:
                audios = audios + tmp_audios[1:]
                offset += last_fetched
                print("Fetched {} audios from {}".format(offset, count))

        utils = AudioUtils()
        utils.save_audios_list(audios)

        path = input("Where to download files:")
        while os.path.exists(path) == False:
            print("Path should exists.")
            path = input("Where to download files:")

        for audio in audios:
            utils.download_audio(audio, path)

        return True




app = VKApp()
app.login()

count_tries = 0
while count_tries < 5 and app.download_user_music() == False:
    count_tries += 1
    print("Trying adain...")

if count_tries == 5:
    print("Try again later.")