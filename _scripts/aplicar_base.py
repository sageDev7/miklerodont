"""Aplica tokens del cliente al kit, suma propio.css + internas.css y configura main.js (una sola vez)."""
from pathlib import Path
D = Path(__file__).resolve().parent.parent

css = (D / "styles.css").read_text(encoding="utf8")
for old, new in [
    ("--bg-alt:#E8EBEE;", "--bg-alt:#EAF1F6;"),
    ("--dark:#182A38;", "--dark:#1E3A52;"),
    ("--dark-2:#0F1E29;", "--dark-2:#142A3C;"),
    ("--accent:#A4865C;", "--accent:#3F729A;"),
    ("--accent-l:#C2A06E;", "--accent-l:#8FB6D3;"),
    ("--text:#1E2A33;", "--text:#1B2730;"),
    ("--muted:#5D646B;", "--muted:#56626C;"),
    ("--line:rgba(24,42,56,.12);", "--line:rgba(30,58,82,.13);"),
    ('--head:"Cormorant Garamond",Georgia,serif;', '--head:"Urbanist",system-ui,sans-serif;'),
    ('--body:"Montserrat",system-ui,-apple-system,"Segoe UI",sans-serif;', '--body:"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif;'),
    (".sec-alt .lead,.sec-alt .muted{color:#444C54}", ".sec-alt .lead,.sec-alt .muted{color:#414D57}"),
]:
    assert old in css, old
    css = css.replace(old, new)
propio = (D / "_scripts" / "propio.css").read_text(encoding="utf8") + (D / "_scripts" / "internas.css").read_text(encoding="utf8")
marca = "/* Anti modo oscuro forzado"
assert marca in css
css = css.replace(marca, propio.strip() + "\n\n" + marca)
(D / "styles.css").write_text(css, encoding="utf8")

js = (D / "main.js").read_text(encoding="utf8")
old = 'var WA_NUMBER = "549XXXXXXXXXX"; // REEMPLAZAR (formato 549 + característica sin 0 + número sin 15)'
assert old in js
js = js.replace(old, 'var WA_NUMBER = ""; // su web no publica WhatsApp: los CTA llaman (tel:) y el formulario va por email')
old = '  var yr = document.getElementById("yr");'
assert old in js
js = js.replace(old, '''  /* ---------- horario del consultorio en vivo (hora de Buenos Aires) ---------- */
  var est = document.getElementById("estado");
  if (est && window.Intl) {
    var H = { 1: [14, 19], 2: [9, 19], 3: [9, 19], 4: [9, 19], 5: [14, 19] };
    var DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
    var p = {};
    new Intl.DateTimeFormat("en-US", { timeZone: "America/Argentina/Buenos_Aires", weekday: "short", hour: "numeric", minute: "numeric", hourCycle: "h23" })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var d = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(p.weekday);
    var h = (parseInt(p.hour, 10) % 24) + parseInt(p.minute, 10) / 60, r = H[d], tit, sub;
    if (d >= 0) {
      if (r && h >= r[0] && h < r[1]) { tit = "Abierto ahora"; sub = "Hoy atendemos hasta las " + r[1] + " h"; est.classList.add("on"); }
      else if (r && h < r[0]) { tit = "Cerrado ahora"; sub = "Hoy abrimos a las " + r[0] + " h"; }
      else {
        var k = d, n = 0;
        do { k = (k + 1) % 7; n++; } while (!H[k]);
        tit = "Cerrado ahora"; sub = "Abrimos " + (n === 1 ? "mañana" : "el " + DIAS[k]) + " a las " + H[k][0] + " h";
      }
      document.getElementById("estadoTit").textContent = tit;
      document.getElementById("estadoSub").textContent = sub;
    }
  }

  var yr = document.getElementById("yr");''')
(D / "main.js").write_text(js, encoding="utf8")
print("ok")
