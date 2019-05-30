import re

def remove_context_content_from_text(subtitle_text, tokens, dialog_marker):
    dialog_marker = re.escape(dialog_marker)
    for token_pair in tokens:
        # escaping special characters
        opening_token = re.escape(token_pair[0])
        closing_token = re.escape(token_pair[1])

        dialog_pattern = "(?:^|\n){}(?:{})+(?:.|\n)*?(?:{})+\s*(?:\n|\Z)" \
                          .format(dialog_marker, opening_token, closing_token)
        no_dialog_pattern = "(?:{})+(?:.|\n)*?(?:{})+\s*" \
                             .format(opening_token, closing_token)

        subtitle_text = re.sub(dialog_pattern, '', subtitle_text)
        subtitle_text = re.sub(no_dialog_pattern, '', subtitle_text)

    return subtitle_text

def remove_context_content(subtitles, tokens, dialog_marker):
    for subtitle in subtitles:
        subtitle.text = remove_context_content_from_text(subtitle.text,
                                                         tokens,
                                                         dialog_marker)
