import re
from .utils import remove_context_content
from .utils import remove_character_names
from .utils import remove_lyrics

__all__ = ['clean_subtitles',]


def detect_dialog_marker(subtitles, dialog_marker_candidates):
    candidate_count = {}
    for candidate in dialog_marker_candidates:
        candidate_count[candidate] = 0
        candidate_count[candidate+"\s"] = 0

    for subtitle in subtitles:
        for key in candidate_count.keys():
            count = len(re.findall("(?m)^" + re.escape(key), subtitle.text))
            candidate_count[key] += count

    # get dictionary key with maximum count
    marker = max(candidate_count, key=candidate_count.get)
    marker = re.sub("\\\s", " ", marker)
    return marker


def uniformize_dialog_marker(subtitle_text,
                             possible_dialog_markers,
                             dialog_marker_to_use):
    pattern = "(?m)^[{}]\s?".format(re.escape(''.join(possible_dialog_markers)))
    subtitle_text = re.sub(pattern, dialog_marker_to_use, subtitle_text)
    return subtitle_text

def clean_single_dialog(subtitle_text, dialog_marker):
    dialog_marker = re.escape(dialog_marker)
    pattern = "(?m)^{}".format(dialog_marker)
    if len(re.findall(pattern, subtitle_text)) == 1:
        pattern = "{}(.*)".format(pattern)
        subtitle_text = re.sub(pattern, "\g<1>", subtitle_text)
    return subtitle_text

def normalize_newlines(subtitle_text):
    return re.sub("\r", '', subtitle_text)


def delete_empty_subtitles(subtitles, dialog_marker):
    empty_subtitles = []
    for i, subtitle in enumerate(subtitles):
        subtitle.text = clean_single_dialog(subtitle.text, dialog_marker)
        if len(subtitle.text) == 0:
            empty_subtitles.append(i)

    for i in reversed(empty_subtitles):
        del subtitles[i]


def clean_subtitles(subtitles, tokens, lyrics_tokens, character_name_regex):
    dialog_marker_list = ["‐", "-", "—"]
    dialog_marker = detect_dialog_marker(subtitles, dialog_marker_list)
    for subtitle in subtitles:
        subtitle.text = normalize_newlines(subtitle.text)
        subtitle.text = uniformize_dialog_marker(subtitle.text,
                                                 dialog_marker_list,
                                                 dialog_marker)

    remove_context_content(subtitles, tokens + lyrics_tokens, dialog_marker)
    remove_character_names(subtitles, character_name_regex, dialog_marker)
    remove_lyrics(subtitles, lyrics_tokens)

    delete_empty_subtitles(subtitles, dialog_marker)

    # clean stuff a bit
    subtitles.sort()
    subtitles.clean_indexes()
