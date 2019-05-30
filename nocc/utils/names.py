import re

def remove_character_names_from_text(subtitle_text,
                                     character_name_regex,
                                     dialog_marker):
    top_pattern = "^{}(\n|\Z)".format(character_name_regex)
    dialog_pattern = "(?m)^({})?{}".format(re.escape(dialog_marker),
                                           character_name_regex)

    subtitle_text = re.sub(top_pattern, '', subtitle_text)
    subtitle_text = re.sub(dialog_pattern, dialog_marker, subtitle_text)

    return subtitle_text


def remove_character_names(subtitles, character_name_regex, dialog_marker):
    for subtitle in subtitles:
        subtitle.text = remove_character_names_from_text(subtitle.text,
                                                         character_name_regex,
                                                         dialog_marker)
