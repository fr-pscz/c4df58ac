import altair as _al


def _iosevka():
    font = "Iosevka Regular"

    return {
        "config": {
            "title": {"font": font},
            "axis": {"labelFont": font, "titleFont": font},
            "header": {"labelFont": font, "titleFont": font},
            "legend": {"labelFont": font, "titleFont": font},
            "text": {"font": font},
        }
    }


_al.themes.register("iosevka", _iosevka)
_al.themes.enable("iosevka")
