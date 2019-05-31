import os
import pysrt
import cchardet as chardet

from .utils import *

__all__ = ['load_subtitles',
           'save_subtitles',
           'clean_subtitles']


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


def clean_subtitles(subtitles, tokens, lyrics_tokens, character_name_regex):
    normalize_newlines(subtitles)

    dialog_marker_list = ["‐", "-", "—"]
    dialog_marker = detect_dialog_marker(subtitles, dialog_marker_list)
    uniformize_dialog_marker(subtitles, dialog_marker_list, dialog_marker)

    filter_out_context_content(subtitles, tokens + lyrics_tokens, dialog_marker)
    filter_out_character_names(subtitles, character_name_regex, dialog_marker)
    filter_out_lyrics(subtitles, lyrics_tokens)

    cleanup_single_dialog_marker(subtitles, dialog_marker)
    delete_empty_subtitles(subtitles, dialog_marker)

    subtitles.sort()
    subtitles.clean_indexes()
