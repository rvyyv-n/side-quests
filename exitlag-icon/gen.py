"""render the exitlag taskbar icon: svg -> 1024px png (headless chrome) -> multi-size .ico."""
import pathlib, os, subprocess
from PIL import Image

HERE = pathlib.Path(__file__).parent
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)

# the x is two halves: red ">" chevrons on the left (speed), a white "<" on the right.
SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#26262a"/><stop offset="1" stop-color="#0f0f11"/>
  </linearGradient>
  <linearGradient id="red" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff4a4a"/><stop offset="1" stop-color="#d4141c"/>
  </linearGradient>
</defs>
<rect x="24" y="24" width="976" height="976" rx="236" fill="url(#bg)"/>
<g fill="none" stroke-width="104" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="4">
  <path d="M150 292 L370 512 L150 732" stroke="url(#red)" opacity=".55"/>
  <path d="M330 292 L550 512 L330 732" stroke="url(#red)"/>
  <path d="M874 292 L654 512 L874 732" stroke="#f4f4f5"/>
</g>
</svg>"""

(HERE / "exitlag.svg").write_text(SVG)
png = HERE / "exitlag.png"
subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                "--window-size=1024,1024", f"--screenshot={png}", (HERE / "exitlag.svg").as_uri()], check=True)
Image.open(png).convert("RGBA").save(HERE / "exitlag.ico", sizes=[(s, s) for s in ICO_SIZES])
