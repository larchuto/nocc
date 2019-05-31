from .utils import *

__all__ = ['clean_subtitles',]


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
