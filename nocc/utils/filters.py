import re
from .tools import substitute_pattern_from_subtitles, \
                   remove_pattern_from_subtitles

__all__ = ['filter_out_context_content',
           'filter_out_character_names',
           'filter_out_lyrics']

def filter_out_context_content(subtitles, tokens, dialog_marker):
    dialog_marker = re.escape(dialog_marker)
    for token_pair in tokens:
        # escaping special characters
        opening_token = re.escape(token_pair[0])
        closing_token = re.escape(token_pair[1])

        dialog_pattern = "(?:^|\n){}(?:{})+(?:.|\n)*?(?:{})+\s*(?:\n|\Z)" \
                          .format(dialog_marker, opening_token, closing_token)
        no_dialog_pattern = "(?:{})+(?:.|\n)*?(?:{})+\s*" \
                             .format(opening_token, closing_token)

        remove_pattern_from_subtitles(dialog_pattern, subtitles)
        remove_pattern_from_subtitles(no_dialog_pattern, subtitles)

def filter_out_character_names(subtitles, character_name_regex, dialog_marker):
    top_pattern = "^{}(\n|\Z)".format(character_name_regex)
    dialog_pattern = "(?m)^({})?{}".format(re.escape(dialog_marker),
                                           character_name_regex)

    remove_pattern_from_subtitles(top_pattern, subtitles)
    substitute_pattern_from_subtitles(dialog_pattern, dialog_marker, subtitles)


def _filter_out_lyrics_in_text(subtitle_text, lyrics_tokens_pair, in_lyrics):
    if not in_lyrics:
        regexp = "(?:{})+(?:.|\n)*".format(re.escape(lyrics_tokens_pair[0]))
        subtitle_text, nb_match = re.subn(regexp, "", subtitle_text, count = 1)
        if nb_match > 0:
            in_lyrics = True
    else: # in lyrics
        regexp = "(?:.|\n)*(?:{})+".format(re.escape(lyrics_tokens_pair[1]))
        subtitle_text, nb_match = re.subn(regexp, "", subtitle_text, count = 1)
        if nb_match > 0:
            in_lyrics = False
        else:
            subtitle_text = ""
    return subtitle_text, in_lyrics

def filter_out_lyrics(subtitles, lyrics_tokens):
    for lyrics_tokens_pair in lyrics_tokens:
        in_lyrics = False
        for subtitle in subtitles:
            subtitle.text, in_lyrics = _filter_out_lyrics_in_text(
                                                            subtitle.text,
                                                            lyrics_tokens_pair,
                                                            in_lyrics)
