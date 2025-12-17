# components/styles.py
STATE_COLORS = {
    "bozza": "#f0ad4e",
    "confermato": "#5cb85c",
    "cancellato": "#d9534f"
}

def status_badge(text):
    color = STATE_COLORS.get(text, "#777")
    return f"<span style='background:{color};color:#fff;padding:4px 8px;border-radius:6px;font-size:12px'>{text}</span>"
