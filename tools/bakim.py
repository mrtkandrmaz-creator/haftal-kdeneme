#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gece bakımı: testler, tutarlılık taraması, ölü kod raporu ve resmî MEB müfredatı karşılaştırması.
Çıktı: BAKIM_RAPORU.md (depo kökü). Çıkış kodu: test/tarama başarısızsa 1.
Kod otomatik SİLİNMEZ (yalnız raporlanır); müfredat farkı yalnız raporlanır, yerleşik liste elle güncellenir.
Kullanım: python tools/bakim.py [--hizli] [--ag-yok]"""
import ast, collections, datetime, glob, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app.py")
sys.path.insert(0, os.path.join(ROOT, "tools"))
args = sys.argv[1:]
rep, fail = [], []


def run(cmd, timeout=1800):
    try:
        p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return 1, "ZAMAN AŞIMI"


def step_tests():
    rc, out = run(["tools/run_checks.py"])
    last = [l for l in out.splitlines() if "test geçti" in l]
    rep.append(f"- Regresyon testleri: **{'GEÇTİ' if rc == 0 else 'KALDI'}** ({last[-1].strip() if last else '?'})")
    if rc:
        fail.append("run_checks")
        rep.append("```\n" + "\n".join(out.strip().splitlines()[-25:]) + "\n```")


def step_scans():
    for name, script in (("Tutarlılık taraması (5. sınıf havuzu)", "tools/tutarlilik_taramasi.py"),
                         ("Şekil–metin denetimi", "tools/check_figures.py")):
        if not os.path.exists(os.path.join(ROOT, script)):
            continue
        rc, out = run([script])
        rep.append(f"- {name}: **{'temiz' if rc == 0 else 'SORUN'}**")
        if rc:
            fail.append(script)
            rep.append("```\n" + "\n".join(out.strip().splitlines()[-20:]) + "\n```")


def modules():
    src = open(APP, encoding="utf-8").read()
    return src, {n: b for n, b in re.findall(r"MODULES\['(\w+/\w+)'\] = r'''(.*?)\n'''", src, re.S)}


# Dolaylı kullanıldığı (takma ad / eski kayıt) doğrulanmış, silinmemesi gerekenler
KEEP = {"_alan_sh", "_od6", "_par_draw", "_poly", "_regular", "_rot", "_geo", "_bio_icon"}


def step_dead(src, mods):
    T = lambda s: set(re.findall(r"\w+", s))
    main = src
    for b in mods.values():
        main = main.replace(b, "")
    extra = ""
    for f in glob.glob(os.path.join(ROOT, "tools", "**", "*.py"), recursive=True):
        extra += open(f, encoding="utf-8").read()
    root = T(main) | T(extra)
    defs = {}
    for m, s in mods.items():
        try:
            t = ast.parse(s)
        except SyntaxError:
            continue
        L = s.split("\n")
        for n in t.body:
            seg = "\n".join(L[n.lineno - 1:n.end_lineno])
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                defs[(m, n.name)] = (n.end_lineno - n.lineno + 1, T(seg) - {n.name})
                for x in ast.walk(n):
                    if isinstance(x, ast.Constant) and isinstance(x.value, str):
                        root |= T(x.value)
            else:
                root |= T(seg)
    byname = collections.defaultdict(list)
    for k in defs:
        byname[k[1]].append(k)
    reach, st = set(), [k for nm in root for k in byname.get(nm, [])]
    while st:
        k = st.pop()
        if k in reach:
            continue
        reach.add(k)
        st += [k2 for tk in defs[k][1] for k2 in byname.get(tk, []) if k2 not in reach]
    dead = sorted(k for k in defs if k not in reach and k[1] not in KEEP)
    rep.append(f"- Ölü kod adayı: **{len(dead)}** işlev ({sum(defs[k][0] for k in dead)} satır). Otomatik silinmez; aynı adlı eski tanımlar ve takma adlar yanlış alarm verebilir, silmeden önce testle doğrulayın.")
    if dead:
        rep.append("  " + ", ".join(f"`{m}:{n}`" for m, n in dead[:40]) + (" …" if len(dead) > 40 else ""))
    dd = len(re.findall(r"\bif False\b|\band False\b|\bor True\b", src))
    rep.append(f"- `if False` / `and False` / `or True` ölü dal sayısı: **{dd}**")
    rep.append(f"- app.py satır sayısı: {src.count(chr(10)) + 1}")


CODE = re.compile(r"\b[A-ZÇĞİÖŞÜ]{2,4}\.\d{1,2}(?:\.\d{1,2}){1,3}\b")


def step_curriculum(src, mods):
    if "--ag-yok" in args:
        rep.append("- MEB müfredat karşılaştırması: atlandı (--ag-yok)")
        return
    try:
        import build_pool as bp
        ai, cur, store = bp.load_pkg(APP)
        from core import meb_live
        n, errs = meb_live.refresh(deadline=240)
        live = dict(getattr(cur, "LIVE", {}) or {})
        if not live:
            import json
            p = os.path.join(store.DATA, getattr(meb_live, "CACHE", "meb_live.json"))
            if os.path.exists(p):
                live = (json.load(open(p, encoding="utf-8")) or {}).get("data", {})
    except Exception as e:
        rep.append(f"- MEB müfredat karşılaştırması: **çalışmadı** ({type(e).__name__}: {str(e)[:120]})")
        return
    known = set(CODE.findall(mods.get("core/curriculum", "") + mods.get("core/ai_engine", "")))
    rep.append(f"- MEB resmî programları çekildi: {n} kayıt, {len(errs or [])} hata")
    if not live:
        rep.append("  - **Karşılaştırılamadı:** hiç program indirilemedi (ağ/MEB sitesi); fark yok anlamına gelmez.")
        return
    miss_total = 0
    for k, units in sorted(live.items()):
        codes = set()
        for _u, items in units:
            for it in items:
                codes |= set(CODE.findall(str(it)))
        miss = sorted(codes - known)
        miss_total += len(miss)
        if miss:
            rep.append(f"  - `{k}`: yerleşik listede olmayan {len(miss)} kazanım kodu: {', '.join(miss[:15])}")
    if not miss_total:
        rep.append("  - Çekilen programlardaki tüm kazanım kodları yerleşik müfredatta var (fark yok).")
    for e in (errs or [])[:5]:
        rep.append(f"  - indirme hatası: {str(e)[:120]}")


def main():
    src, mods = modules()
    rep.append(f"# Gece bakım raporu\n\n_{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC_\n")
    rep.append("## Kontroller")
    if "--hizli" not in args:
        step_tests()
        step_scans()
    rep.append("\n## Kod bakımı")
    step_dead(src, mods)
    rep.append("\n## Müfredat")
    step_curriculum(src, mods)
    rep.append("\n## Sonuç\n" + ("**BAŞARISIZ:** " + ", ".join(fail) if fail else "Tüm kontroller geçti."))
    open(os.path.join(ROOT, "BAKIM_RAPORU.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
