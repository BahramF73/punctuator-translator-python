import os

from googletrans import Translator
from deepmultilingualpunctuation import PunctuationModel
import pathlib

files = list(pathlib.Path().glob("*.txt"))
files = [file.stem for file in files if
         (file.name.find("-translated.txt") == -1 and file.name.find("-edited.txt") == -1)]


def start(files_name):
    for file_name in files_name:
        print(f"\n\n****{file_name}.txt Started!****")

        if not os.path.isfile(f"{file_name}-edited.txt"):
            model = PunctuationModel()
            with open(f"{file_name}.txt", "r") as file:
                text = file.read()
                text = text.replace("[Music]\n", "")
                text = text.replace("\n\n", " ")
                result = model.restore_punctuation(text)
                with open(f"{file_name}-edited.txt", "w") as edited_file:
                    lined = result.replace(". ", ".\n")
                    edited_file.write(lined)
            lines = result.split(". ")
            lines = [f"{line}." for line in lines]
            print(f"Example line: {lines[0]}")
        else:
            with open(f"{file_name}-edited.txt", "r") as edited_file:
                edited_text = edited_file.readlines()
                lines = [line.replace("\n", "") for line in edited_text]

        #######################################################
        #                                                     #
        #                                                     #
        #                     Translating                     #
        #                                                     #
        #                                                     #
        #######################################################
        if not os.path.isfile(f"{file_name}-translated.txt"):
            open(f"{file_name}-translated.txt", "w").close()
            for index, line in enumerate(lines):
                translator = Translator()
                translated = translator.translate(line, dest="de", src="en")

                with open(f"{file_name}-translated.txt", "a") as translated_file:
                    translated_file.write(f"{line}\n{translated.text}\n\n")
                print(f'\rTranslated line: {index + 1} ==> "{line[:10]}".', end='')
        else:
            line_number = int(input("\n\nEnter line number: "))
            start_index = line_number - 1
            for i in range(start_index, len(lines)):
                translator = Translator()
                translated = translator.translate(lines[i], dest="de", src="en")
                with open(f"{file_name}-translated.txt", "a") as translated_file:
                    translated_file.write(f"{lines[i]}\n{translated.text}\n\n")
                print(f'\rTranslated line: {i + 1} ==> "{lines[i][:10]}".', end='')

        print(f"\n\n****{file_name} Finished!****")


def ask():
    for index, file in enumerate(files):
        print(f"{index}) {file}.txt")
    choice = input("Select number of file or 'a' for all files:")
    if choice.lower() == "a":
        start(files)
    else:
        try:
            choice = int(choice)
            start([files[choice]])
        except (ValueError, IndexError) as e:
            print("Invalid choice!")
            ask()


if __name__ == "__main__":
    ask()
