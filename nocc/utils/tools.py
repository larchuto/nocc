import re

def substitute_pattern_from_subtitles(pattern, replacement, subtitles):
    compiled_pattern = re.compile(pattern)
    for subtitle in subtitles:
        subtitle.text = re.sub(compiled_pattern, replacement, subtitle.text)

def remove_pattern_from_subtitles(pattern, subtitles):
    substitute_pattern_from_subtitles(pattern, '', subtitles)
