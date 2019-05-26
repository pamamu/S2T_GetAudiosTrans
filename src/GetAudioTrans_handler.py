import Pyro4

from ContainerHandler import ContainerHandler
from utils import *


@Pyro4.expose
class GetAudioTransHandler(ContainerHandler):

    def __init__(self, container_name, main_uri):
        super().__init__(container_name, main_uri)

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            print("Container {}: Runned with {}".format(self.container_name, kwargs))
            self.running = True
            result = self.download_files(kwargs['input_json'], kwargs['output_folder'])
            print(result)
            self.running = False
            return result
        else:
            raise TypeError('input_json and output_folder required')

    def info(self):
        return self.running

    def download_files(self, input_json, output_folder):
        """
        TODO DOCUMENTATION
        :param input_json:
        :param output_folder:
        :return:
        """
        try:
            response = []
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)
            programs = simplejson.load(open(input_json))
            for program in programs:
                path = os.path.join(output_folder, program['name'].replace('/', '-').replace(' ', '_'))
                if not os.path.isdir(path):
                    os.mkdir(path)
                html_tree = get_html_tree(program['uri'])

                audio_url = get_audio_url(html_tree)
                audio_path = get_audio_file(audio_url, path)
                # audio_path = ""

                trans = get_audio_trans(html_tree)
                trans_path = save_trans(trans, path)
                print((audio_path, trans_path))
                response.append((audio_path, trans_path))
                response_json = save_json(response, os.path.join(output_folder, 'audios.json'))
            return response_json
        except Exception as e:
            print(e)


if __name__ == '__main__':
    a = GetAudioTransHandler("GetAudiosTrans", "PYRO:MainController@localhost:4040")
    print(a.run(input_json='resources/programs.json',
                output_folder='/Users/pablomaciasmunoz/Dev/WS_TFG/S2T/shared_folder'))
