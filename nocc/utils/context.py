import re
from .tools import remove_pattern_from_subtitles

def remove_context_content(subtitles, tokens, dialog_marker):
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
