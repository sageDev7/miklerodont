"""Páginas internas de Mikler Odontología. Toma head, header/menú y footer del index (se puede volver a correr).
Uso: python _scripts/gen_paginas.py"""
import re
from pathlib import Path
D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")

head = idx[:idx.index("</head>")]
head = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
hdr = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
ftr = idx[idx.index("<!-- ============ FOOTER ============ -->"):idx.index('<div class="modal"')]
def local(h):  # anclas del index -> ./index.html#ancla
    h = h.replace('href="#inicio"', 'href="./index.html"')
    return re.sub(r'href="#([a-z][\w-]*)"', r'href="./index.html#\1"', h)
hdr, ftr = local(hdr), local(ftr)

def ph(titulo, sub, foto, nombre):
    return f'''<section class="ph" style="--ph:url('./img/{foto}')">
  <div class="wrap ph-in">
    <nav class="crumb rise" aria-label="Ruta"><a href="./index.html">Inicio</a><i class="ti ti-chevron-right" aria-hidden="true"></i><span>{nombre}</span></nav>
    <h1 class="ph-h1 rise d1">{titulo}</h1>
    <p class="ph-sub rise d2">{sub}</p>
  </div>
</section>'''

BTNS = '<div class="cta-btns"><a class="btn btn-lima" href="tel:+541148246496">Llamar para un turno</a><a class="btn btn-line" href="./index.html#contacto">Enviar una consulta</a></div>'

def cta(t, p, alt=False):
    return f'''<section class="sec{' sec-alt' if alt else ''}">
  <div class="wrap cta-in reveal">
    <h2 class="h2">{t}</h2>
    <p class="lead">{p}</p>
    {BTNS}
  </div>
</section>'''

def rows(items):
    return "\n".join(f'          <li><h3>{t}</h3><p>{d}</p></li>' for t, d in items)

# ---------------- TRATAMIENTOS ----------------
GRUPOS = [
 ("implantes", "ti-dental", "Implantes dentales", "Reemplazan una pieza, varias o la arcada completa, con prótesis fijas o removibles. Elegir el tratamiento correcto empieza por un buen estudio.", [
   ("Qué es un implante", "Un pequeño tornillo de titanio que reemplaza la raíz del diente. Se coloca en el hueso del maxilar o la mandíbula, que crece a su alrededor y lo fija."),
   ("Cuándo se indica", "Ante la pérdida de dientes por enfermedad o traumatismo, dientes que no se desarrollaron o dentaduras que se mueven o causan dolor."),
   ("Cirugías peri-implantarias", "Levantamiento de seno o injerto de hueso, cuando falta hueso o hay estructuras cercanas como el nervio dentario o el seno maxilar."),
   ("Cómo es el tratamiento", "En dos etapas: la cirugía de colocación, con anestesia local y prótesis provisoria, y entre 3 y 6 meses después, la prótesis definitiva.")]),
 ("protesis", "ti-crown", "Prótesis dentales", "Fijas o removibles, definitivas o provisorias, para resolver la falta o el desgaste de piezas dentales.", [
   ("Coronas de porcelana", "Restauran, protegen y fortalecen dientes debilitados. En los dientes anteriores se usa porcelana pura, que reproduce la forma y el color originales."),
   ("Perno y corona", "Para dientes con tratamiento de conducto, que quedan debilitados. Ambos se hacen a medida."),
   ("Puentes", "Una opción cuando falta más de una pieza."),
   ("Prótesis removibles", "Cuando no se puede usar una prótesis fija. Se hacen a medida, en acrílico con dientes de acrílico o porcelana.")]),
 ("cirugia-oral", "ti-dental-broken", "Cirugía oral", "Diagnóstico y tratamiento quirúrgico de los tejidos de la boca, los dientes, las encías y los maxilares.", [
   ("Muelas del juicio", "Extracción con anestesia local, después de una consulta con evaluación clínica y radiológica. Suele durar menos de una hora."),
   ("Piezas retenidas", "Dientes que no llegan a su lugar en la arcada, como los caninos superiores. Muchas veces se trabaja junto con la ortodoncia."),
   ("Remoción de quistes", "En general con una biopsia previa, que se analiza en el laboratorio."),
   ("Frenectomía y patología oral", "Otras intervenciones de la cirugía oral."),
   ("Cirugías previas a un implante", "Levantamiento de seno e injertos de hueso.")]),
 ("maxilofacial", "ti-face-id", "Cirugía maxilofacial", "Cirugía de mayor complejidad para alteraciones funcionales y estéticas congénitas, posteriores a un traumatismo o a otra cirugía.", [
   ("Cirugía ortognática", "Corrige problemas en el desarrollo de los maxilares. Se planifica junto con el ortodoncista."),
   ("Prognatismo y retrognatismo", "Mandíbula adelantada o retrasada respecto del maxilar superior."),
   ("Asimetrías faciales", "Desarrollo desparejo de los maxilares."),
   ("Traumatismos", "Fracturas y lesiones de los maxilares."),
   ("Secuelas de cirugía tumoral", "Reconstrucción después de una cirugía oncológica.")]),
 ("estetica", "ti-sparkles", "Estética dental", "Tratamientos para mejorar la apariencia de los dientes y la sonrisa, que también pueden restaurar piezas dañadas.", [
   ("Carillas de porcelana", "Láminas delgadas hechas a medida que cubren el frente de los dientes. Se colocan en dos visitas."),
   ("Blanqueamiento dental", "Aclara el color de los dientes con un método no invasivo. Cuánto dura depende de los hábitos y la higiene de cada persona."),
   ("Rellenos de composite", "Reparan dientes astillados, rotos o descoloridos con un material del color del esmalte."),
   ("Incrustaciones", "De porcelana o composite, hechas en el laboratorio para piezas con deterioro estructural.")]),
 ("ortodoncia", "ti-mood-smile", "Ortodoncia", "Para chicos y adultos. Además de la estética, mejora la mordida y facilita la higiene. El tratamiento habitual dura de uno a dos años.", [
   ("Brackets metálicos", "La técnica tradicional, con brackets unidos por un alambre que se ajusta periódicamente."),
   ("Brackets estéticos", "De porcelana o zafiro, menos visibles."),
   ("Ortodoncia lingual o invisible", "Para transitar el tratamiento sin que los brackets se noten tanto."),
   ("Ortodoncia prequirúrgica", "Preparación para la cirugía ortognática, en mordidas abiertas o cruzadas y asimetrías.")]),
]
chips = "".join(f'<a href="#{k}">{t}</a>' for k, _, t, _, _ in GRUPOS)
FONDOS = ["", " sec-alt", "", " sec-dark", "", " sec-alt"]  # la especialidad del Dr. va oscura
bloques = ""
for n, (k, ic, t, intro, items) in enumerate(GRUPOS):
    bloques += f'''
<section class="sec grupo{FONDOS[n]}" id="{k}">
  <div class="wrap grupo-grid">
    <div class="grupo-head reveal">
      <span class="ic-box" aria-hidden="true"><i class="ti {ic}"></i></span>
      <h2 class="h2">{t}</h2>
      <p class="lead">{intro}</p>
      <a class="link-arrow" href="./index.html#contacto">Consultar por este tratamiento <i class="ti ti-arrow-right" aria-hidden="true"></i></a>
    </div>
    <ul class="filas reveal">
{rows(items)}
    </ul>
  </div>
</section>
'''
tratamientos = ph("Tratamientos", "Implantes, prótesis, cirugía, estética dental y ortodoncia en un mismo consultorio.", "instrumental.jpg", "Tratamientos") + f'''

<nav class="chips" aria-label="Tratamientos"><div class="wrap chips-in">{chips}</div></nav>
{bloques}
''' + cta("¿Querés saber qué opción te corresponde?", "Cada tratamiento se indica después de una consulta de evaluación y los estudios necesarios.")

# ---------------- EL CONSULTORIO ----------------
ESP = [("ti-dental", "Implantes dentales"), ("ti-crown", "Prótesis"), ("ti-face-id", "Cirugía oral y maxilofacial"), ("ti-dental-broken", "Endodoncia"),
       ("ti-heart-handshake", "Periodoncia"), ("ti-mood-smile", "Ortodoncia"), ("ti-stethoscope", "Odontología general")]
esp = "".join(f'<li><i class="ti {i}" aria-hidden="true"></i>{t}</li>' for i, t in ESP)
consultorio = ph("El consultorio", "Odontología general y especializada en Palermo, con el Dr. Amit Mikler.", "modelo.jpg", "El consultorio") + f'''

<section class="sec" id="equipo">
  <div class="wrap dr-grid">
    <div class="retrato reveal"><figure><img src="./img/dr-mikler.jpg" alt="Dr. Amit Mikler" width="425" height="450" loading="lazy"></figure></div>
    <div class="reveal">
      <p class="eyebrow">Equipo profesional</p>
      <h2 class="h2">Dr. Amit Mikler</h2>
      <p class="lead">Odontólogo especialista en cirugía maxilofacial.</p>
      <!-- Matrícula: no figura en su web actual. Pedirla y sumarla acá (M.N.). -->
      <p>Te atiende junto a un equipo de profesionales de prótesis, ortodoncia, endodoncia y periodoncia, con trato personalizado: te explicamos las opciones y te recomendamos la más adecuada para tu caso.</p>
    </div>
  </div>
</section>

<section class="sec sec-dark" id="especialidades">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Especialidades</p>
      <h2 class="h2">Todo el tratamiento, <em>en un lugar</em></h2>
    </div>
    <ul class="esp reveal">{esp}</ul>
  </div>
</section>

<section class="sec sec-alt" id="instalaciones">
  <div class="wrap inst-grid">
    <div class="reveal">
      <p class="eyebrow">Instalaciones</p>
      <h2 class="h2">Habilitados por el <em>Ministerio de Salud</em></h2>
      <p class="lead">El consultorio está equipado con tecnología actual y cumple las normas de higiene y bioseguridad, en una zona de Palermo de fácil acceso.</p>
      <p class="os-tit">Atención particular y obras sociales</p>
      <ul class="os"><li>OSDE</li><li>OMINT</li><li>SIMECO</li><li>William Hope</li></ul>
    </div>
    <div class="horario reveal">
      <h3>Horario de atención</h3>
      <ul>
        <li><b>Lunes</b><span>14 a 19 h</span></li>
        <li><b>Martes a jueves</b><span>9 a 19 h</span></li>
        <li><b>Viernes</b><span>14 a 19 h</span></li>
      </ul>
      <p class="dir">Av. Santa Fe 3546, piso 1, depto. 12 · Palermo, CABA</p>
    </div>
  </div>
</section>

''' + cta("Pedí tu consulta de evaluación", "Llamanos al (011) 4824-6496 o escribinos con tu caso.")

# ---------------- PREGUNTAS ----------------
FAQ = [
 ("Implantes dentales", [
   ("¿Cualquier persona puede ponerse un implante?", "Se pueden usar en la mayoría de los pacientes, siempre que se haga un estudio previo adecuado. En pocos casos falta hueso o hay estructuras cercanas, como el nervio dentario o el seno maxilar, y antes se necesita una cirugía peri-implantaria."),
   ("¿Cuánto tarda el tratamiento?", "Se hace en dos etapas. Primero se colocan los implantes y una prótesis provisoria. Entre 3 y 6 meses después, según el caso, se confecciona la prótesis definitiva, que se prueba y ajusta en varias consultas."),
   ("¿Duele la colocación?", "Se hace con anestesia local y de forma ambulatoria. Las molestias posteriores suelen compararse con las de una extracción, y se indica medicación por unos días."),
   ("¿Qué ventajas tiene frente a otras opciones?", "No afecta a los dientes vecinos y ayuda a mantener el hueso del maxilar, que se reabsorbe cuando falta una pieza durante mucho tiempo.")]),
 ("Muelas del juicio", [
   ("¿Cuándo hay que extraerlas?", "Cuando hay infecciones repetidas, caries que no se pueden tratar, quistes o la muela interfiere con una prótesis o un implante. No se indica si se prevé que va a crecer normalmente o si el riesgo para la salud supera el beneficio."),
   ("¿Qué es una muela retenida?", "Una muela que no llega a salir por falta de espacio o porque la frena el tejido, el hueso u otro diente. Puede estar parcial o totalmente retenida."),
   ("¿Cómo es la cirugía?", "Con anestesia local y, en general, en menos de una hora. Si hace falta, se pueden extraer las cuatro en una sola sesión."),
   ("¿Conviene esperar?", "Una vez indicada la extracción, se recomienda hacerla a corto plazo: la posibilidad de complicaciones es menor en pacientes jóvenes."),
   ("¿Qué cuidados hay que tener después?", "Reposo el día siguiente y nada de actividad física intensa durante una semana, hasta el control.")]),
 ("Estética y ortodoncia", [
   ("¿Cuántas visitas llevan las carillas de porcelana?", "Dos. En la primera se preparan los dientes y se toma una impresión para el laboratorio, que tarda entre 5 y 7 días. En la segunda se adhieren las carillas."),
   ("¿La ortodoncia es solo para chicos?", "No. Los brackets ya no están reservados a los chicos, y hay técnicas lingual o invisible para que el tratamiento se note menos."),
   ("¿Cuánto dura un tratamiento de ortodoncia?", "El tiempo habitual es de uno a dos años, con controles en general una vez por mes y un período de contención al final.")]),
 ("La consulta", [
   ("¿Me pueden operar el mismo día de la consulta?", "Muy raramente. Antes hace falta una evaluación clínica, en general un estudio radiológico, tus antecedentes médicos y la medicación que tomás, para planificar la cirugía."),
   ("¿Atienden obras sociales?", "Sí: OSDE, OMINT, SIMECO y William Hope, además de la atención particular."),
   ("Vivo en otra provincia o en el exterior, ¿me pueden atender?", "Sí. Podemos organizar tratamientos de corta duración durante tu estadía. Escribinos con tu caso.")]),
]
faq = ""
for g, qs in FAQ:
    det = "\n".join(f'        <details><summary>{q}</summary><p>{a}</p></details>' for q, a in qs)
    faq += f'''
    <div class="faq-grupo reveal">
      <h2>{g}</h2>
      <div class="faq">
{det}
      </div>
    </div>'''
preguntas = ph("Preguntas frecuentes", "Lo que más nos consultan sobre implantes, muelas del juicio, estética y ortodoncia.", "sonrisa.jpg", "Preguntas") + f'''

<section class="sec" id="faq">
  <div class="wrap faq-wrap">{faq}
  </div>
</section>

''' + cta("¿Tenés otra pregunta?", "Escribinos con tu caso o llamanos para coordinar una consulta.", alt=True)

PAGES = {
 "tratamientos.html": ("Tratamientos | Mikler Odontología · Palermo", "Implantes dentales, prótesis, cirugía oral y muelas del juicio, cirugía maxilofacial, estética dental y ortodoncia en Palermo, CABA.", tratamientos),
 "consultorio.html": ("El consultorio | Mikler Odontología · Palermo", "Consultorio odontológico en Av. Santa Fe 3546, Palermo. Dr. Amit Mikler, especialista en cirugía maxilofacial. OSDE, OMINT, SIMECO y William Hope.", consultorio),
 "preguntas.html": ("Preguntas frecuentes | Mikler Odontología · Palermo", "Respuestas sobre implantes dentales, extracción de muelas del juicio, carillas, ortodoncia y la primera consulta en Mikler Odontología.", preguntas),
}
for f, (title, desc, body) in PAGES.items():
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', h, flags=re.S)
    h = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', h)
    h = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc}">', h)
    h = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{title}">', h)
    h = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{desc}">', h)
    hh = hdr.replace(f'href="./{f}"', f'href="./{f}" aria-current="page"')
    html = f'''{h}</head>
<body class="pg">

{hh}<main>

{body}

</main>

{ftr}<script src="./main.js"></script>
</body>
</html>
'''
    (D / f).write_text(html, encoding="utf8")
    print("ok", f)
