from os import path

from youtube_dl import YoutubeDL

from VCsMusicBot.config import DURATION_LIMIT
from VCsMusicBot.helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 لايمكنك تنزيل فيديوهات التي تزيد مدتها {DURATION_LIMIT} دقيقه, "
            f"الفيديو المقدم هو {duration} دقيقه",
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"🛑 لايمكنك تنزيل فيديوهات التي تزيد مدتها {DURATION_LIMIT} دقيقه, "
            f"the provided video is {duration} minute(s)",
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
