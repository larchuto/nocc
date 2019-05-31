import re
from .tools import remove_pattern_from_subtitles, \
                   substitute_pattern_from_subtitles

def remove_character_names(subtitles, character_name_regex, dialog_marker):
    top_pattern = "^{}(\n|\Z)".format(character_name_regex)
    dialog_pattern = "(?m)^({})?{}".format(re.escape(dialog_marker),
                                           character_name_regex)

    remove_pattern_from_subtitles(top_pattern, subtitles)
    substitute_pattern_from_subtitles(dialog_pattern, dialog_marker, subtitles)
