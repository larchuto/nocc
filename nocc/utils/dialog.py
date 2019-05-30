import re

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


def uniformize_dialog_marker(subtitles,
                             possible_dialog_markers,
                             dialog_marker_to_use):
    markers = re.escape(''.join(possible_dialog_markers))
    pattern = "(?m)^[{}]\s?".format(markers)
    for subtitle in subtitles:
        subtitle.text = re.sub(pattern, dialog_marker_to_use, subtitle.text)


def cleanup_single_dialog_marker(subtitles, dialog_marker):
    dialog_marker = re.escape(dialog_marker)
    pattern_marker = "(?m)^{}".format(dialog_marker)
    pattern_all = "{}(.*)".format(pattern_marker)
    for subtitle in subtitles:
        if len(re.findall(pattern_marker, subtitle.text)) == 1:
            subtitle.text = re.sub(pattern_all, "\g<1>", subtitle.text)
