import os
import pysrt
import cchardet as chardet


def load_subtitles(filename, file_encoding):
    if file_encoding == None:
        content = open(filename, "rb").read()
        file_encoding = chardet.detect(content)['encoding']
    subtitles = pysrt.open(filename, encoding = file_encoding)
    return subtitles, file_encoding

def save_subtitles(subtitles,
                  output_filename, output_encoding,
                  input_filename, input_encoding):
    if output_filename == None:
        splited_name = os.path.splitext(input_filename)
        output_filename = splited_name[0] + ".noTAG" + splited_name[1]
    if output_encoding == None:
        output_encoding = input_encoding
    subtitles.save(output_filename, encoding = output_encoding)
