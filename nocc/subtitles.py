from .utils import remove_context_content, \
                   remove_character_names, \
                   remove_lyrics, \
                   detect_dialog_marker, \
                   uniformize_dialog_marker, \
                   cleanup_single_dialog_marker

__all__ = ['clean_subtitles',]


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


def clean_subtitles(subtitles, tokens, lyrics_tokens, character_name_regex):
    normalize_newlines(subtitles)

    dialog_marker_list = ["‐", "-", "—"]
    dialog_marker = detect_dialog_marker(subtitles, dialog_marker_list)
    uniformize_dialog_marker(subtitles, dialog_marker_list, dialog_marker)

    remove_context_content(subtitles, tokens + lyrics_tokens, dialog_marker)
    remove_character_names(subtitles, character_name_regex, dialog_marker)
    remove_lyrics(subtitles, lyrics_tokens)

    cleanup_single_dialog_marker(subtitles, dialog_marker)
    delete_empty_subtitles(subtitles, dialog_marker)

    subtitles.sort()
    subtitles.clean_indexes()
