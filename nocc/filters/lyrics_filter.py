import re

def remove_lyrics_from_text(subtitle_text, lyrics_tokens_pair, in_lyrics):
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

def remove_lyrics(subtitles, lyrics_tokens):
    for lyrics_tokens_pair in lyrics_tokens:
        in_lyrics = False
        for subtitle in subtitles:
            subtitle.text, in_lyrics = remove_lyrics_from_text(subtitle.text,
                                                        lyrics_tokens_pair,
                                                        in_lyrics)
