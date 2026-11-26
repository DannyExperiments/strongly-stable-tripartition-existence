"""Render the Boolean arm-label cube and build the offline explorer archive."""

import math
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("Q621_FONT_DIR", "/System/Library/Fonts/Supplemental"))
BG, PANEL, TEXT, MUTED, GRID = "#121a2b", "#202f48", "#f5f8ff", "#c7d8f0", "#536687"
GOOD, BAD, REPAIR = "#b8b1ff", "#ffbf78", "#69edc3"
VERTICES = [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]
EDGES = [(a,b) for i,a in enumerate(VERTICES) for b in VERTICES[i+1:]
         if sum(abs(x-y) for x,y in zip(a,b))==1]
STAGES = [
    (0, 1, "No repair at y = 1", "Both Bad modes are maximal.", "The ranking for x = 0 fails."),
    (1, 1, "A repair at y = 1", "Repair adds C to {A}.", "Good and Repair are maximal."),
    (1, 0, "The same x repairs y = 0", "Both y choices have a repair.", "The ranking for x = 1 is stable."),
]


def font(size, bold=False):
    name="Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(str(FONT_DIR/name),size)


def project(point, angle):
    a,b,c=(2*v-1 for v in point)
    u,v=math.cos(angle),math.sin(angle)
    return round(352+122*(u*a-v*b)), round(337+67*(v*a+u*b)-95*c)


def frame(stage, angle):
    x,y,title,caption,outcome=STAGES[stage]
    repair_exists=bool(x or not y)
    image=Image.new("RGB",(704,835),BG)
    d=ImageDraw.Draw(image)
    d.text((34,30),"Repair and stability",font=font(53,True),fill=TEXT)
    d.text((35,96),f"Test x = {x} against y = {y}",font=font(34),fill=MUTED)
    d.rounded_rectangle((30,151,674,585),radius=25,fill=PANEL)
    for a,b in EDGES:
        d.line((project(a,angle),project(b,angle)),fill=GRID,width=3)

    good=project((0,1,0),angle)
    bad=project((1,0,0),angle)
    repair=project((1,0,1),angle)
    if repair_exists:
        sx,sy=repair
        d.line((bad,(sx,sy+17)),fill=REPAIR,width=7)
        d.polygon(((sx,sy+4),(sx-11,sy+29),(sx+11,sy+29)),fill=REPAIR)
        d.ellipse((sx-11,sy-11,sx+11,sy+11),fill=REPAIR,outline=BG,width=2)
        d.text((sx,sy-50),"Repair",font=font(31,True),fill=REPAIR,anchor="mm")
        d.text((sx,sy-23),"{A, C}",font=font(26),fill=TEXT,anchor="mm")

    gx,gy=good
    d.ellipse((gx-11,gy-11,gx+11,gy+11),fill=GOOD,outline=BG,width=2)
    d.text((gx,gy+32),"Good",font=font(32,True),fill=GOOD,anchor="mm")
    d.text((gx,gy+60),"{A′}",font=font(26),fill=TEXT,anchor="mm")
    sx,sy=bad
    bad_color=MUTED if repair_exists else BAD
    d.rounded_rectangle((sx-11,sy-11,sx+11,sy+11),radius=3,fill=bad_color,outline=BG,width=2)
    d.text((sx,sy+32),"Bad0, Bad1",font=font(31,True),fill=bad_color,anchor="mm")
    d.text((sx,sy+60),"{A}",font=font(26),fill=TEXT,anchor="mm")
    d.text((350,555),"Arm formulas in the middle block",font=font(29),fill=MUTED,anchor="mm")

    d.text((34,611),title,font=font(43,True),fill=TEXT)
    d.line(((35,673),(669,673)),fill=GRID,width=2)
    d.text((36,692),caption,font=font(33),fill=TEXT)
    d.text((36,749),outcome,font=font(30,True),fill=REPAIR if stage==2 else TEXT)
    return image.quantize(colors=48,method=Image.Quantize.MEDIANCUT)


def main():
    frames,delays=[],[]
    for stage in range(3):
        for i in range(20):
            angle=.45+.15*math.sin(math.tau*i/20)
            frames.append(frame(stage,angle))
            delays.append(300 if i==0 else 170)
    frames[0].save(HERE/"repair-stability.gif",save_all=True,append_images=frames[1:],
                   duration=delays,disposal=1,loop=0,optimize=True)
    item=ZipInfo("index.html",(1980,1,1,0,0,0))
    item.create_system=3
    item.external_attr=0o100644<<16
    with ZipFile(HERE/"repair-stability-explorer.zip","w") as archive:
        archive.writestr(item,(HERE/"index.html").read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__=="__main__":
    main()
