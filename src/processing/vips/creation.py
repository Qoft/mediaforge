import typing

import pyvips

from processing.vips.caption import twemoji
from processing.vips.vipsutils import escape
from utils.tempfiles import TempFile


def yskysn(captions: typing.Sequence[str]):
    captions = escape(captions)
    # load stuff
    im = pyvips.Image.new_from_file("rendering/images/yskysn.png")
    # here for my sanity, dimensions of text area
    w = 500
    h = 582
    # technically redundant but adds twemoji font
    text = pyvips.Image.text(".", fontfile=twemoji)
    # generate text
    text = pyvips.Image.text(
        f"<span foreground='white'>"
        f"{captions[0]}\n<span size='150%'>{captions[1]}</span>"
        f"</span>",
        font=f"Twemoji Color Emoji,Tahoma Bold 56px",
        rgba=True,
        fontfile="rendering/fonts/TAHOMABD.TTF",
        align=pyvips.Align.CENTRE,
        width=w,
        height=h
    )
    # pad to expected size, 48 is margin
    text = text.gravity(pyvips.CompassDirection.CENTRE, w + 48, h + 48, extend=pyvips.Extend.BLACK)
    # add glow, similar technique to shadow
    mask = pyvips.Image.gaussmat(5 / 2, 0.0001, separable=True)
    glow = text[3].convsep(mask).cast(pyvips.BandFormat.UCHAR)
    glow = glow.new_from_image((255, 255, 255)) \
        .bandjoin(glow) \
        .copy(interpretation=pyvips.Interpretation.SRGB)

    text = glow.composite2(text, pyvips.BlendMode.OVER)

    out = im.composite2(text, pyvips.BlendMode.OVER)
    # save and return
    outfile = TempFile("png")
    out.pngsave(outfile)
    return outfile


def f1984(captions: typing.Sequence[str]):
    captions = escape(captions)

    originaldate = captions[1].lower() == "january 1984"

    if originaldate:
        im = pyvips.Image.new_from_file("rendering/images/1984/1984originaldate.png")
    else:
        im = pyvips.Image.new_from_file("rendering/images/1984/1984.png")

    # technically redundant but adds twemoji font
    speech_bubble = pyvips.Image.text(".", fontfile=twemoji)
    # generate text
    speech_bubble = pyvips.Image.text(
        captions[0],
        font=f"Twemoji Color Emoji,Atkinson Hyperlegible Bold",
        rgba=True,
        fontfile="rendering/fonts/AtkinsonHyperlegible-Bold.ttf",
        align=pyvips.Align.CENTRE,
        width=290,
        height=90
    )
    # pad to expected size
    speech_bubble = speech_bubble.gravity(pyvips.CompassDirection.CENTRE, 290, 90, extend=pyvips.Extend.BLACK)
    # add speech bubble
    im = im.composite2(speech_bubble, pyvips.BlendMode.OVER, x=60, y=20)

    if not originaldate:
        # technically redundant but adds twemoji font
        date = pyvips.Image.text(".", fontfile=twemoji)
        # generate text
        date = pyvips.Image.text(
            captions[1],
            font=f"Twemoji Color Emoji,Impact",
            rgba=True,
            fontfile="rendering/fonts/ImpactMix.ttf",
            align=pyvips.Align.CENTRE,
            width=124,
            height=34
        )
        # pad to expected size
        date = date.gravity(pyvips.CompassDirection.CENTRE, 124, 34, extend=pyvips.Extend.BLACK)
        # equivelant to skewY(10deg)
        date = date.affine([1, 0, 0.176327, 1])
        # add date
        im = im.composite2(date, pyvips.BlendMode.OVER, x=454, y=138)
        # add cover
        im = im.composite2(pyvips.Image.new_from_file("rendering/images/1984/1984cover.png"), pyvips.BlendMode.OVER)

    outfile = TempFile("png")
    im.pngsave(outfile)
    return outfile