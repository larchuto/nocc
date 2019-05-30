import re


__all__ = ['clean_subtitles',]

def remove_non_dialog(subtitle_text, tokens):
    for token_pair in tokens:
        # escaping special characters
        opening_token = re.escape(token_pair[0])
        closing_token = re.escape(token_pair[1])

        hyphen_patern = "(?:^|\n)\s?[\-‐]\s?(?:{})+(?:.|\n)*?(?:{})+\s*(?:\n|\Z)" \
                            .format(opening_token, closing_token)
        no_hyphen_patern = "(?:{})+(?:.|\n)*?(?:{})+\s*" \
                            .format(opening_token, closing_token)

        subtitle_text = re.sub(hyphen_patern, '', subtitle_text)
        subtitle_text = re.sub(no_hyphen_patern, '', subtitle_text)

    return subtitle_text

def remove_lyrics(subtitle_text, lyrics_tokens_pair, start):
    if start:
        remove_lyrics.in_lyrics = False
    if not remove_lyrics.in_lyrics:
        regexp = "(?:{})+(?:.|\n)*".format(re.escape(lyrics_tokens_pair[0]))
        subtitle_text, nb_match = re.subn(regexp, "", subtitle_text, count = 1)
        if nb_match > 0:
            remove_lyrics.in_lyrics = True
    else: # in lyrics
        regexp = "(?:.|\n)*(?:{})+".format(re.escape(lyrics_tokens_pair[1]))
        subtitle_text, nb_match = re.subn(regexp, "", subtitle_text, count = 1)
        if nb_match > 0:
            remove_lyrics.in_lyrics = False
        else:
            subtitle_text = ""
    return subtitle_text


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


def clean_dialog_marker(subtitle_text,
                        possible_dialog_markers,
                        dialog_marker_to_use):
    pattern = "(?m)^[{}]\s?".format(re.escape(''.join(possible_dialog_markers)))
    subtitle_text = re.sub(pattern, dialog_marker_to_use, subtitle_text)
    return subtitle_text

def clean_single_dialog(subtitle_text):
    return re.sub("^\s?[\-‐]\s?(.*)\Z", "\g<1>", subtitle_text)

def clean_newlines(subtitle_text):
    return re.sub("\r", '', subtitle_text)


def clean_subtitles(subtitles, tokens, lyrics_tokens):
    dialog_marker_list = ["‐", "-", "—"]
    dialog_marker = detect_dialog_marker(subtitles, dialog_marker_list)
    for subtitle in subtitles:
        subtitle.text = clean_newlines(subtitle.text)
        subtitle.text = clean_dialog_marker(subtitle.text,
                                            dialog_marker_list,
                                            dialog_marker)
        subtitle.text = remove_non_dialog(subtitle.text, tokens + lyrics_tokens)

    for lyrics_tokens_pair in lyrics_tokens:
        start = True
        for subtitle in subtitles:
            subtitle.text = remove_lyrics(subtitle.text,
                                          lyrics_tokens_pair,
                                          start)
            start = False

    empty_subtitles = []
    for i, subtitle in enumerate(subtitles):
        subtitle.text = clean_single_dialog(subtitle.text)
        if len(subtitle.text) == 0:
            empty_subtitles.append(i)

    for i in reversed(empty_subtitles):
        del subtitles[i]

    # clean stuff a bit
    subtitles.sort()
    subtitles.clean_indexes()
