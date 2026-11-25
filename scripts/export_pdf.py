"""Export PDF 16:9 du HTML de présentation, sans dépendance à un navigateur ouvert."""
import argparse
from pathlib import Path


def export(source, output):
    from weasyprint import HTML
    # Géométrie fixe pour les moteurs PDF ne prenant pas en charge vh/vw/clamp.
    css = '''@page {size: 1280px 720px; margin: 0}
    html,body {margin:0; padding:0; background:#101c29; color:#f2f6f8}
    .slide,.slide.active {display:flex; flex-direction:column; justify-content:center;
      position:relative; width:1280px; height:720px; min-height:720px;
      padding:65px 100px 85px; break-after:page; box-sizing:border-box}
    .kicker {font-size:25px; margin:0 0 26px; color:#74dece}
    h1 {font-size:58px; line-height:1.08; margin:0 0 38px; max-width:1080px}
    .body {font-size:34px; line-height:1.5; white-space:pre-line; margin:0; max-width:1080px}
    .foot {position:absolute; left:100px; right:100px; bottom:28px;
      font-size:14px; display:flex; justify-content:space-between; color:#aabdc8}
    aside,nav {display:none!important}
    '''
    source = Path(source).resolve()
    text = source.read_text(encoding="utf-8").replace("</head>", f"<style>{css}</style></head>")
    HTML(string=text, base_url=str(source.parent)).write_pdf(output)
    print(f"PDF : {output}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="presentation/index.html")
    p.add_argument("--output", default="presentation/presentation.pdf")
    export(**vars(p.parse_args()))
