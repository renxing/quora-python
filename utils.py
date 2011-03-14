# coding: utf-8
def truncate_lines(body, lines = 4, max_chars = 400):
    if not body: return ""
    body_lines = body.splitlines()
    summary = "\n".join(body_lines[0:lines])
    return summary
    summary = _truncate_lines(body_lines, lines - 1, summary, max_chars)
    return summary

def _truncate_lines(body_lines, lines, summary, max_chars):
    if len(summary) > max_chars:
        lines -= 1
        if lines > 1:
            body_lines = body_lines[0:lines]
            summary = "\n".join(body_lines)
            return _truncate_lines(body_lines, lines, summary, max_chars)
        else:
            summary = body_lines[0][0:max_chars]
            return summary
    else:
        return summary
