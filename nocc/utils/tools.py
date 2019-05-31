import re

def substitute_pattern_from_subtitles(pattern, replacement, subtitles):
    compiled_pattern = re.compile(pattern)
    for subtitle in subtitles:
        subtitle.text = re.sub(compiled_pattern, replacement, subtitle.text)

def remove_pattern_from_subtitles(pattern, subtitles):
    substitute_pattern_from_subtitles(pattern, '', subtitles)


def normalize_newlines(subtitles):
    for subtitle in subtitles:
        subtitle.text = '\n'.join(subtitle.text.splitlines())

def delete_empty_subtitles(subtitles, dialog_marker):
    empty_subtitles = []
    for i, subtitle in enumerate(subtitles):
        if len(subtitle.text) == 0:
            empty_subtitles.append(i)

    for i in reversed(empty_subtitles):
        del subtitles[i]
