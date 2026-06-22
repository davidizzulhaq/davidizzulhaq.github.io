# Convert the David Izzulhaq website from dark green/gold theme to light MONO (black & white) system.
# Backs up the original first. Verify in browser before trusting.
import re, os, shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
BAK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index_darkbak.html")
if not os.path.exists(BAK):
    shutil.copy(SRC, BAK); print("backup ->", BAK)

html = open(SRC, encoding="utf-8").read()

# --- exact hex swaps (dark -> light mono) ---
swaps = {
 # backgrounds (dark -> light)
 "#0B0E0D":"#FFFFFF", "#0F1513":"#F7F7F7", "#121A17":"#F4F4F4",
 "#0F3A30":"#F0F0F0", "#0f3a30":"#F0F0F0", "#123b30":"#F0F0F0",
 "#16463B":"#EDEDED", "#2a6151":"#DADADA", "#1d5f4e":"#D2D2D2",
 "#1DBF73":"#0A0A0A",
 # mid green / chart accents -> ink / grey
 "#3fa07e":"#0A0A0A", "#3FA07E":"#0A0A0A",
 # main light text -> ink
 "#ECEAE2":"#0A0A0A", "#FBFBF8":"#FFFFFF",
 # muted green-grey text -> neutral greys
 "#D7DDD5":"#3A3A3A", "#C8D2CB":"#474747", "#A9B6AE":"#6B6B6B",
 "#BBC7BF":"#6B6B6B", "#8b9990":"#8A8A8A", "#6f7d75":"#9A9A9A",
 # gold accents -> black/near-black
 "#C99A3C":"#0A0A0A", "#E2B65A":"#333333",
 "#b07d2a":"#1A1A1A", "#8a6320":"#1A1A1A", "#6e4d18":"#262626", "#3f2d10":"#262626",
 # whatsapp green -> mono (keep recognizable via icon shape)
 "#25D366":"#0A0A0A",
}
for a,b in swaps.items():
    html = html.replace(a,b)

# --- rgba family swaps via regex ---
# teal borders rgba(33,86,74,A) -> subtle black border (reduced alpha)
def teal(m):
    a=float(m.group(1)); return f"rgba(10,10,10,{round(min(a*0.32,0.16),3)})"
html = re.sub(r"rgba\(33, ?86, ?74, ?([\d.]+)\)", teal, html)
# gold alphas rgba(201,154,60,A) -> black alpha (same alpha)
html = re.sub(r"rgba\(201, ?154, ?60, ?([\d.]+)\)", lambda m:f"rgba(10,10,10,{m.group(1)})", html)
# whatsapp green alpha
html = re.sub(r"rgba\(37, ?211, ?102, ?([\d.]+)\)", lambda m:f"rgba(10,10,10,{m.group(1)})", html)
# fiverr green alpha
html = re.sub(r"rgba\(29, ?191, ?115, ?([\d.]+)\)", lambda m:f"rgba(10,10,10,{m.group(1)})", html)
# dark green overlays -> light/neutral
html = re.sub(r"rgba\(22, ?70, ?59, ?([\d.]+)\)", lambda m:f"rgba(0,0,0,{round(float(m.group(1))*0.3,3)})", html)
html = re.sub(r"rgba\(15, ?21, ?19, ?([\d.]+)\)", lambda m:f"rgba(0,0,0,{m.group(1)})", html)
html = re.sub(r"rgba\(11, ?14, ?13, ?([\d.]+)\)", lambda m:f"rgba(0,0,0,{m.group(1)})", html)
html = re.sub(r"rgba\(16, ?70, ?59, ?([\d.]+)\)", lambda m:f"rgba(0,0,0,{round(float(m.group(1))*0.3,3)})", html)

# --- fonts: Fraunces -> Archivo ---
html = html.replace(
 "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500;1,9..144,600",
 "family=Archivo:wght@400;500;600;700;800")
html = html.replace("'Fraunces', Georgia, serif", "'Archivo', system-ui, sans-serif")
html = html.replace("'Fraunces', serif", "'Archivo', system-ui, sans-serif")
html = html.replace("Fraunces", "Archivo")
# headings were weight 500 in serif; bump to 700 for grotesk presence
html = html.replace("font-family: 'Archivo', system-ui, sans-serif; font-weight: 500;",
                    "font-family: 'Archivo', system-ui, sans-serif; font-weight: 700;")
# italic emphasis -> upright bold (mono has no elegant italic)
html = html.replace("font-style: italic; font-weight: 500;", "font-weight: 800;")
html = html.replace("font-style: italic; font-weight: 600;", "font-weight: 800;")

open(SRC,"w",encoding="utf-8").write(html)
# report leftover greens/golds
left = re.findall(r"#C99A3C|#E2B65A|#ECEAE2|#0B0E0D|Fraunces|rgba\(33, ?86", html)
print("converted. leftover brand tokens:", len(left))
print("done")
