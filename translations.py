import db

tl_sheet = db.get_sheet("Translations")
tls = tl_sheet.get_all_records()

def get(to_lang, source):
    from_lang = "jp"
    if to_lang == "jp":
        from_lang = "en"
    for tl in tls:
        if tl[from_lang] == source:
            return tl[to_lang]
    return source

def set(jp, en):
    for i in range(len(tls)):
        tl = tls[i]
        if tl["jp"] == jp:
            tl["en"] = en
            tl_sheet.update('A{0}:B{0}'.format(str(i+2)), [[jp, en]])
            return
    tls.append({"jp": jp, "en": en})
    row = len(tl) + 1
    tl_sheet.update('A{0}:B{0}'.format(row), [[jp, en]])
