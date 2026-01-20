import qrcode
from qrcode.image.svg import SvgPathImage
import xml.etree.ElementTree as ET

# ======================
# KONFIGURATION
# ======================

DATA = "https://gbs-property-services-beerlin.github.io/QR-Redirect/link1.html"
LOGO_SVG_PATH = "logo.svg"
OUTPUT_FILE = "qr_mit_logo.svg"

QR_COLOR = "rgb(220,49,44)"   # Firmenfarbe
LOGO_SCALE = 0.22             # 22 % der QR-Größe

# ======================
# QR-CODE ALS SVG
# ======================

img = qrcode.make(
    DATA,
    image_factory=SvgPathImage,
    box_size=10,
    border=4
)

svg_string = img.to_string().decode("utf-8")

# ======================
# SVG PARSEN
# ======================

svg_root = ET.fromstring(svg_string)

# Farbe setzen
for elem in svg_root.iter():
    if "fill" in elem.attrib and elem.attrib["fill"] == "black":
        elem.attrib["fill"] = QR_COLOR

# ======================
# LOGO-SVG LADEN
# ======================

logo_tree = ET.parse(LOGO_SVG_PATH)
logo_root = logo_tree.getroot()

# viewBox auslesen
viewbox = logo_root.attrib.get("viewBox", "0 0 100 100")
_, _, vw, vh = map(float, viewbox.split())

# ======================
# LOGO GRUPPIEREN & SKALIEREN
# ======================

logo_group = ET.Element("g")

scale = LOGO_SCALE
translate_x = 0.5 - scale / 2
translate_y = 0.5 - scale / 2

logo_group.attrib["transform"] = (
    f"translate({translate_x * 100}%, {translate_y * 100}%) "
    f"scale({scale})"
)

for child in list(logo_root):
    logo_group.append(child)

# ======================
# LOGO IN QR EINBETTEN
# ======================

svg_root.append(logo_group)

# ======================
# SPEICHERN
# ======================

ET.ElementTree(svg_root).write(
    OUTPUT_FILE,
    encoding="utf-8",
    xml_declaration=True
)

print(f"SVG QR-Code mit SVG-Logo gespeichert: {OUTPUT_FILE}")
