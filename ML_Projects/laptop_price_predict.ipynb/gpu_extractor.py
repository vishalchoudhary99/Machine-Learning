import re
import pandas as pd

def _clean(s):
    s = str(s).lower()
    repl = {
        "â\x80\x8e":"", "®":"", "â®":"", "ge force":"geforce",
        "nvdia":"nvidia","inte ":"intel ","integarted":"integrated",
        "intergrated":"integrated","raedon":"radeon","readon":"radeon",
        "intelhd":"intel hd","irix":"iris","graphicss":"graphics"
    }
    for k,v in repl.items():
        s=s.replace(k,v)
    return " ".join(s.split())

def company(s):
    if any(x in s for x in ["nvidia","geforce","quadro","rtx","gtx","mx "]): return "NVIDIA"
    if any(x in s for x in ["intel","uhd","iris","arc","hd graphics","gma"]): return "Intel"
    if any(x in s for x in ["amd","radeon","vega"]): return "AMD"
    if "ati" in s: return "ATI"
    if "apple" in s or "core gpu" in s: return "Apple"
    if "adreno" in s or "qualcomm" in s: return "Qualcomm"
    if "mali" in s or "immortalis" in s: return "ARM"
    if "powervr" in s: return "PowerVR"
    if "mediatek" in s: return "MediaTek"
    return "Unknown"

def family(s):
    for k,v in [("rtx","RTX"),("gtx","GTX"),(" mx","MX"),("quadro","Quadro"),
                (" gt ","GT"),("arc","Arc"),("iris xe","Iris Xe"),
                ("iris plus","Iris Plus"),("iris","Iris"),("uhd","UHD"),
                ("hd graphics","HD Graphics"),("rx","RX"),
                ("vega","Vega"),("radeon","Radeon"),("adreno","Adreno"),
                ("mali","Mali"),("core gpu","Apple GPU")]:
        if k in s: return v
    return "Other"

patterns=[
r'RTX\s*A?\d{3,4}\s*TI',r'RTX\s*A?\d{3,4}',r'GTX\s*\d{3,4}\s*TI',
r'GTX\s*\d{3,4}',r'MX\s*\d{2,4}',r'GT\s*\d{3,4}[A-Z]?',
r'QUADRO\s*[A-Z]*\d+',r'ARC\s*[A-Z]?\d+[A-Z]*',
r'UHD\s*\d+',r'HD\s*GRAPHICS\s*\d+',r'IRIS\s*XE',
r'IRIS\s*PLUS\s*\d*',r'RX\s*\d{3,4}[A-Z]*',r'VEGA\s*\d+',
r'RADEON\s*R\d',r'RADEON\s*\d+[A-Z]*',r'ADRENO\s*\d+',
r'MALI[- ]?[A-Z0-9]+',r'IMMORTALIS[- ]?[A-Z0-9]+'
]

def model(s):
    u=s.upper()
    for p in patterns:
        m=re.search(p,u)
        if m: return re.sub(r"\s+"," ",m.group()).strip()
    return "Unknown"

def gtype(s):
    if any(x in s for x in ["rtx","gtx","mx","quadro","rx ","rx6","rx5","gt "]):
        return "Dedicated"
    if any(x in s for x in ["uhd","iris","hd graphics","arc","vega","adreno","mali","integrated","apple"]):
        return "Integrated"
    return "Unknown"

def extract_gpu(df,col="GPU"):
    c=df[col].fillna("").apply(_clean)
    df[col]=c
    df["GPU_Company"]=c.apply(company)
    df["GPU_Family"]=c.apply(family)
    df["GPU_Model"]=c.apply(model)
    df["GPU_Type"]=c.apply(gtype)
    return df
