import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path

BASE = Path(__file__).parent

st.set_page_config(page_title="Convivencia digital UNAL", page_icon=str(BASE / "U.png"))

st.markdown(
    """
    <style>
    div[role="radiogroup"] { gap: 1rem; }
    div[role="radiogroup"] > label {
        margin-bottom: 0.6rem;
        line-height: 1.5;
    }

    iframe[srcdoc*="window.parent"] {
    position: absolute;
    width: 0;
    height: 0;
    border: 0;
    opacity: 0;
    pointer-events: none;
}
    </style>
    """,
    unsafe_allow_html=True,
)

def subir_al_inicio(pagina):
    codigo = f"""
    <!-- {pagina} -->
    <script>
        const doc = window.parent.document;
        const zonas = [
            doc.querySelector('[data-testid="stMain"]'),
            doc.querySelector('section.main'),
            doc.querySelector('.stMain'),
        ];
        zonas.forEach(z => {{ if (z) z.scrollTo({{top: 0, behavior: 'instant'}}); }});
        window.parent.scrollTo(0, 0);
    </script>
    """
    if hasattr(st, "iframe"):
        st.iframe(codigo, height=1)
    else:
        components.html(codigo, height=0)

def menu_barra():
    with st.sidebar:
        st.title(":green[Índice de la página]")
        st.button("Menú principal", icon="🏠", on_click=ir, args=("menu",), key="sb_menu")
        st.button("¿Qué es?", icon=":material/question_mark:", on_click=ir, args=("Que es",), key="sb_que_es")
        st.button("Formas de agresión", icon=":material/front_hand:", on_click=ir, args=("Agresion",), key="sb_agresion")
        st.button("Consecuencias", icon=":material/warning:", on_click=ir, args=("Consecuencias",), key="sb_consecuencias")
        st.button("Práctica: casos", icon=":material/settings_accessibility:", on_click=ir, args=("Casos",), key="sb_casos")
        st.button(":red[**RUTAS DE ATENCIÓN**]", icon="📞", on_click=ir, args=("Rutas",), key="sb_rutas")

def menu_prin(bv):
    m1, m2, m3 = st.columns([1, bv, 1])
    with m2:
        st.button("Regresar al menú principal", icon="🏠", on_click=ir, args=("menu",), key="prin_menu")

@st.cache_data
def leer_txt(ruta, etiqueta):
    lineas = []
    leyendo = False
    
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea_l = linea.rstrip("\n")

            #1 encontrar etiqueta
            if linea_l.strip() == etiqueta:
                leyendo = True
                continue

            #2 En caso de toparse con otra etiqueta en la lectura
            if leyendo and linea_l.strip().startswith("==="):
                break

            #3 SI estamos en la seccion guardamos lo que haya
            if leyendo:
                lineas.append(linea_l)

    return "\n".join(lineas).strip()

def ir(pagina):
    st.session_state.pg = pagina

tabla = {
    "Mitos": [
        '"Es solo una broma"',
        '"Si en internet, no es tan grave."',
        '"Es libertad de expresión"',
        '"En la universidad esto no pasa"'
    ],
    "Realidad": [
        "Si la otra persona se siente humillada o asustada, el efecto es real, aunque la intención haya sido bromear.",
        "El daño emocional, social y académico es real, y lo publicado puede quedar disponible por mucho tiempo.",
        """La libertad de expresión (art. 20 de la Constitución) convive con el derecho a la intimidad, al buen nombre y a la honra (arts. 15 y 21).
        No ampara agresiones que afecten la dignidad de otros.""",
        "Hay estudios con universitarios en Colombia que encuentran casos de ciberacoso y señalan la necesidad de prevenirlo y atenderlo."
    ],
}

ARCHIVO = BASE / "datos.txt"

introtxt = leer_txt(ARCHIVO, "=== INTRO")
datostxt = leer_txt(ARCHIVO, "=== DATOS")
vlctxt = leer_txt(ARCHIVO, "=== VIOLENCIA")
cibtxt = leer_txt(ARCHIVO, "=== CIBER")
convtxt = leer_txt(ARCHIVO, "=== CONVIVENCIA")
dgtaltxt = leer_txt(ARCHIVO, "=== DIGITAL")
marcotxt = leer_txt(ARCHIVO, "=== MARCO")

cons = {}
for i in range(4):
    cons[f"cons{i+1}"] = leer_txt(ARCHIVO, f"=== CONS{i+1}")


#Esto inicia el estado de la pagina
if "pg" not in st.session_state:
    st.session_state.pg = "menu"

# Sube al inicio solo cuando la sección cambió
if st.session_state.get("pg_anterior") != st.session_state.pg:
    st.session_state.pg_anterior = st.session_state.pg
    subir_al_inicio(st.session_state.pg)


#Pagina de menu
if st.session_state.pg == "menu":
    st.title("Convivencia digital en la  :green[UNAL]", text_alignment="center")
    st.header("Aprende a reconocer una agresión en redes, entender por qué ocurre y saber a quién acudir.", text_alignment="center")
    st.divider()
    menu_barra()
    st.write(introtxt)
    st.error("Si estas viviendo una agresion, ve directo a las rutas de atención.", icon=":material/warning:")
    st.divider()
    st.subheader(":green[**Datos para tener en cuenta:**]", text_alignment="center")
    st.markdown(datostxt)
    st.divider()
    izq1, cent1, cent2, der1 = st.columns(4, gap=20, vertical_alignment="bottom")
    izq3, cent3, der3 = st.columns(3, gap=100)
    

    with izq1:
        st.button("¿Qué es?", icon=":material/question_mark:", type="tertiary",
                  on_click=ir, args=("Que es",), key="main_que_es")
        st.space()

    with cent1:
        st.button("Formas de agresión", icon=":material/front_hand:", type="tertiary",
                  on_click=ir, args=("Agresion",), key="main_agresion")
        st.space()

    with cent2:
        st.button("Consecuencias", icon=":material/warning:", type="tertiary",
                  on_click=ir, args=("Consecuencias",), key="main_consecuencias")
        st.space()

    with der1:
        st.button("Práctica: casos", icon=":material/settings_accessibility:", type="tertiary",
                  on_click=ir, args=("Casos",), key="main_casos")
        st.space()

    with cent3:
        st.button(":red[**RUTAS DE ATENCIÓN**]", icon="📞",
                  on_click=ir, args=("Rutas",), key="main_rutas")
        st.space()

elif st.session_state.pg == "Que es": #Se inicia la opcion consultar saldo si se detecta que la sesion es Consultar saldo
    st.title("¿Qué es?", text_alignment="center")
    st.badge("A continuacion se explica un poco mas acerca de las definiciones clave de la convivencia digital",icon=":material/question_mark:", color="gray")
    st.header(":red[Violencia digital]", divider="red")
    st.markdown(vlctxt)
    st.divider()
    st.header(":orange[Ciberacoso o ciberbullying]", divider="orange")
    st.markdown(cibtxt)
    st.subheader(":blue[¿Cuando se considera ciberacoso?]")
    st.markdown("Para distinguir el acoso de una discusión puntual, se usan los siguientes tres criterios (Olweus, 1993):")
    cb1 = st.checkbox("1.  Intención: la conducta busca hacer daño.")
    cb2 = st.checkbox("2.  Repetición: pasa varias veces, no es un hecho aislado.")
    cb3 = st.checkbox("3.  Desequilibrio de poder: la persona afectada no puede defenderse con facilidad.")
    if cb1 and cb2 and cb3:
        st.markdown("Es muy probable que se trate de ciberacoso, guarda pruebas/evidencia y revisa las rutas de atención")
    elif cb1 and cb2 or cb1 and cb3 or cb2 and cb3 or cb1 or cb2 or cb3:
        st.markdown("Aunque no cumpla todos los criterios, puede ser una agresión digital que merece atención. Un hecho aislado también puede dañar")
    else:
        st.markdown("Selecciona las opciones para poder lograr la distincion")
    st.divider()
    st.header(":green[Convivencia digital]", divider="green")
    st.markdown(convtxt)
    st.divider()
    st.header("¿Por qué pasa?", divider="gray")
    st.markdown(dgtaltxt)
    st.divider()
    st.header("Mitos y realidades", text_alignment="center")
    st.table(tabla, border=True)
    menu_barra()
    menu_prin(1.1)

elif st.session_state.pg == "Agresion": #Se inicia la opcion consignar si se detecta que la sesion es Consignar
    st.title("Formas de agresión", text_alignment="center")
    tit1, tit2 = st.columns(2, gap=100)
    tit3, tit4 = st.columns(2, gap=100)
    tit5, tit6 = st.columns(2, gap=100)
    tit7, tit8 = st.columns(2, gap=100)
    with tit1:
        st.header("Insultos y burlas", text_alignment="left")
        st.markdown("• Qué es: mensajes, comentarios o memes para ofender o ridiculizar a alguien, en público o en chats.")
        st.markdown("• Ejemplo: un chat de curso donde se burlan una y otra vez de la forma de hablar de un compañero.")
        st.markdown("• Señal de alerta: la persona evita escribir o participar en el grupo.")
        st.divider()
    with tit2:
        st.header("Amenazas")
        st.markdown("• Qué es: mensajes que buscan asustar o intimidar, aunque se presenten como 'broma'.")
        st.markdown('• Ejemplo: mensajes directos que dicen "sé dónde estudias, ten cuidado".')
        st.markdown("• Señal de alerta: la persona siente miedo de ir a la universidad. Las amenazas pueden constituir un delito.")
        st.divider()
    with tit3:
        st.header("Discriminación")
        st.markdown("• Qué es: ataques por origen, género, orientación sexual, creencias, apariencia, discapacidad u opinión política.")
        st.markdown("• Ejemplo: comentarios que ridiculizan a una estudiante por su lugar de origen.")
        st.markdown("• Señal de alerta: los ataques se dirigen a una característica de la persona, no a lo que dijo o hizo.")
        st.divider()
    with tit4:
        st.header("Acoso")
        st.markdown("• Qué es: contacto insistente y no deseado, o presión repetida, por mensajes, llamadas o perfiles.")
        st.markdown("• Ejemplo: alguien escribe todos los días a una compañera, aunque ella ya pidió que no lo haga.")
        st.markdown("• Señal de alerta: la persona deja de contestar o cambia sus hábitos para evitar el contacto.")
        st.divider()
    
    with tit5:
        st.header("Humillación pública")
        st.markdown("• Qué es: publicar fotos, videos o capturas vergonzosas de alguien, o difundir mentiras sobre esa persona.")
        st.markdown("• Ejemplo: se publica una captura de un error de alguien en una videollamada con comentarios burlones.")
        st.markdown("• Señal de alerta: el contenido se comparte rápido y sin permiso de la persona.")
        st.divider()
    with tit6:
        st.header("Suplantación de identidad")
        st.markdown("• Qué es: usar el nombre o la foto de alguien, o crear cuentas falsas, para agredir en su nombre.")
        st.markdown("• Ejemplo: una cuenta con la foto de un estudiante escribe mensajes ofensivos a otros.")
        st.markdown("• Señal de alerta: otras personas empiezan a reclamar por mensajes que la víctima nunca envió.")
        st.divider()

    with tit7:
        st.header("Difusión de contenido sin consentimiento")
        st.markdown("• Qué es: compartir imágenes, datos o conversaciones privadas de otra persona sin su permiso.")
        st.markdown("• Ejemplo: reenviar a otros grupos una conversación privada para dejar mal a alguien.")
        st.markdown("• Señal de alerta: la persona se entera por terceros de que su información circula.")
        st.divider()
    with tit8:
        st.header("Uso de inteligencia artificial para el acoso")
        st.markdown("• Qué es: crear o alterar imágenes, audios o textos con herramientas de IA para intimidar, humillar o acosar sexualmente.")
        st.markdown("• Ejemplo: una imagen de una compañera modificada con IA para ridiculizarla.")
        st.markdown("• Señal de alerta: contenido falso muy realista que se reenvía como si fuera verdadero.")
        st.divider()

    menu_barra()
    menu_prin(1.1)


elif st.session_state.pg == "Consecuencias": #Se inicia la opcion retirar si se detecta que la sesion es Retirar
    st.title(":red[Consecuencias]", text_alignment="center")
    st.subheader("Las agresiones digitales tienen efectos que van más allá de lo virtual. Estos son los principales.", text_alignment="center", divider="red")
    con1, con2 = st.columns(2, gap=100)
    con3, con4 = st.columns(2, gap=100)

    with con1:
        st.subheader("**Salud emocional**")
        st.markdown(cons[f"cons{1}"])
        st.divider()
    
    with con2:
        st.subheader("**Vida academica**")
        st.markdown(cons[f"cons{2}"])
        st.divider()
    
    with con3:
        st.subheader("**Relaciones sociales**")
        st.markdown(cons[f"cons{3}"])
        st.divider()
    
    with con4:
        st.subheader("**Convivencia en el campus**")
        st.markdown(cons[f"cons{4}"])
        st.divider()

    menu_barra()
    menu_prin(1.1)

elif st.session_state.pg == "Casos":
    st.title(":blue[Casos practicos]", text_alignment="center")
    st.subheader("A continuacion haremos una pequeña practica con casos inventados. Elige lo que harias y lee la explicación, no hay puntaje que te juzgue, es unicamente para pensar")
    st.subheader("Cada opcion se clasifica como :green[Más útil], :orange[Regular], :red[Poco útil]")
    st.divider()
    conteo = 0
    cs1, cs2 = st.columns(2, gap=100)
    st.divider()
    cs3, cs4 = st.columns(2, gap=100)
    st.divider()
    cs5, cs6 = st.columns(2, gap=100)
    st.divider()
    resultado = st.empty()

    with cs1:
        st.markdown("***En el chat del curso, alguien comparte una foto de un compañero con un texto burlón. Varias personas ponen risas y la foto empieza a circular fuera del grupo.***")
        caso1 = st.radio(
            "Caso1",
            ["1. Reaccionar con una risa para no quedar mal con el grupo.",
            "2. No hacer absolutamente nada porque 'no es mi problema'.",
            "3. Escribirle en privado al compañero para ofrecerle apoyo y pedir al grupo que borren la foto."],
            index=None,
            key="caso1",
            label_visibility="collapsed"
        )
        if caso1 == "1. Reaccionar con una risa para no quedar mal con el grupo.":
            st.markdown(":red[***(Poco útil) Reaccionar da aprobación y hace que la conducta se repita.***]")
        if caso1 == "2. No hacer absolutamente nada porque 'no es mi problema'.":
            st.markdown(":orange[***(Regular) No participar ayuda un poco, pero quien es agredido sigue solo.***]")
        if caso1 == "3. Escribirle en privado al compañero para ofrecerle apoyo y pedir al grupo que borren la foto.":
            st.markdown(":green[***(Más útil) Acompañar a la persona afectada y cuestionar la conducta con calma es de lo más útil. Guardar una captura sirve como evidencia.***]")
            conteo += 1
    
    with cs2:
        st.markdown("***Una cuenta sin nombre publica insultos contra una estudiante por una opinión que dio en clase sobre política. Los comentarios se vuelven cada vez más agresivos.***")
        caso2 = st.radio(
            "Caso 2",
            ["1. Responder con insultos para defenderla.",
            "2. Guardar capturas, reportar la cuenta en la plataforma y avisar a la estudiante.",
            "3. Bloquear la cuenta y seguir de largo."],
            index=None,
            key="caso2",
            label_visibility="collapsed"
        )
        if caso2 == "1. Responder con insultos para defenderla.":
            st.markdown(":red[***(Poco útil) Responder con agresión alimenta la discusión y puede ponerte en riesgo.***]")
        if caso2 == "2. Guardar capturas, reportar la cuenta en la plataforma y avisar a la estudiante.":
            st.markdown(":green[***(Más útil) Dejar evidencia y usar los canales de reporte es lo recomendado.***]")
            conteo += 1
        if caso2 == "3. Bloquear la cuenta y seguir de largo.":
            st.markdown(":orange[***(Regular) Te protege a ti, pero la agresión continúa para ella.***]")
    
    with cs3:
        st.markdown("***Una persona recibe mensajes directos que dicen 'sé dónde estudias, ten cuidado'. Pasan varios días y llegan más mensajes.***")
        caso3 = st.radio(
            "Caso 3",
            ["1. Borrar los mensajes para no pensar en eso.",
            "2. Guardar las capturas, contarlo a alguien de confianza y acudir a Bienestar Universitario.",
            "3. Responder para que el remitente se detenga."],
            index=None,
            key="caso3",
            label_visibility="collapsed"
        )
        if caso3 == "1. Borrar los mensajes para no pensar en eso.":
            st.markdown(":red[***(Poco útil) Los mensajes son evidencia: conviene guardarlos con fecha y hora antes de bloquear o reportar.***]")
        if caso3 == "2. Guardar las capturas, contarlo a alguien de confianza y acudir a Bienestar Universitario.":
            st.markdown(":green[***(Más útil) Las amenazas pueden ser delito y la universidad tiene dependencias para orientar. Si hay peligro inmediato, llama al 123.***]")
            conteo += 1
        if caso3 == "3. Responder para que el remitente se detenga.":
            st.markdown(":orange[***(Regular) Responder rara vez detiene la conducta y puede escalar la situación.***]")
    
    with cs4:
        st.markdown("***Circula una imagen de una compañera modificada con una herramienta de IA para ridiculizarla. Te llega por un grupo y todo el mundo la reenvía.***")
        caso4 = st.radio(
            "Caso 4",
            ["1. Reenviarla para preguntar si es real.",
            "2. No reenviarla, reportarla en la plataforma y avisar a la compañera.",
            "3. Ignorarla porque es obvio que es falsa."],
            index=None,
            key="caso4",
            label_visibility="collapsed"
        )
        if caso4 == "1. Reenviarla para preguntar si es real.":
            st.markdown(":red[***(Poco útil) Reenviarla la multiplica, aunque sea con buena intención.***]")
        if caso4 == "2. No reenviarla, reportarla en la plataforma y avisar a la compañera.":
            st.markdown(":green[***(Más útil) Cortar la cadena de difusión le da a la persona afectada la oportunidad de actuar y pedir apoyo.***]")        
            conteo += 1    
        if caso4 == "3. Ignorarla porque es obvio que es falsa.":
            st.markdown(":orange[***(Regular) Que sea falsa no evita el daño: la humillación existe igual.***]")

    with cs5:
        st.markdown("***Un compañero le escribe varias veces al día a una estudiante, aunque ella ya le dijo que no quiere hablar con él. Ahora también comenta todas sus publicaciones.***")
        caso5 = st.radio(
            "Caso 5",
            ["1. Decirle a ella que 'no se ponga así', que seguro es un gesto de amistad.",
            "2. Ofrecerle acompañarla a Bienestar y ayudarle a guardar los mensajes.",
            "3. Pedirle al compañero que pare, sin más."],
            index=None,
            key="caso5",
            label_visibility="collapsed"
        )
        if caso5 == "1. Decirle a ella que 'no se ponga así', que seguro es un gesto de amistad.":
            st.markdown(":red[***(Poco útil) Minimiza el malestar de quien lo vive. Si la persona dijo que no, la respuesta es no.***]")
        if caso5 == "2. Ofrecerle acompañarla a Bienestar y ayudarle a guardar los mensajes.":
            st.markdown(":green[***(Más útil) Acompañar y documentar le da herramientas para actuar.***]")
            conteo += 1
        if caso5 == "3. Pedirle al compañero que pare, sin más.":
            st.markdown(":orange[***(Regular) Puede ayudar si hay confianza, pero no reemplaza reportar y buscar apoyo institucional si continúa.***]")
    with cs6:
        st.markdown("***Alguien comparte capturas de una conversación privada de un grupo de estudio para dejar mal a un compañero. Tú estás en esa conversación.***")
        caso6 = st.radio(
            "Caso 6",
            ["1. Comentar en el grupo que 'se lo merecía'.",
            "2. Decirle a quien la filtró que eso no está bien y avisar al compañero afectado.",
            "3. Salirte del grupo sin decir nada."],
            index=None,
            key="caso6",
            label_visibility="collapsed"
        )
        if caso6 == "1. Comentar en el grupo que 'se lo merecía'.":
            st.markdown(":red[***(Poco útil) Justificar la agresión la refuerza.***]")
        if caso6 == "2. Decirle a quien la filtró que eso no está bien y avisar al compañero afectado.":
            st.markdown(":green[***(Más útil) Muestra que la conducta no tiene respaldo y le da información a quien la necesita.***]")
            conteo += 1
        if caso6 == "3. Salirte del grupo sin decir nada.":
            st.markdown(":orange[***(Regular) Puede protegerte, pero no frena la difusión.***]")
    
    resultado.subheader(
        f"Elegiste la acción más útil en {conteo} de 6 casos. "
        "No importa el resultado, lo importante es que ya pensaste qué harías.",
        text_alignment="center",
    )
    menu_barra()
    menu_prin(1.1)


elif st.session_state.pg == "Rutas":
    st.title(":red[RUTAS DE ATENCIÓN]", text_alignment="center")
    st.markdown("Si estás viviendo una agresión, o conoces a alguien que sí, no tienes que resolverlo solo.", text_alignment="center")
    r1, r2 = st.columns(2, gap= 50)
    st.divider()
    with r1:
        st.subheader("Qué hacer paso a paso.")
        st.markdown("1. **Tu seguridad primero.** Si hay peligro inmediato, llama al :red[123].")
        st.markdown("2. **Guarda la evidencia.** Capturas de pantalla con fecha y hora, enlaces y nombres de usuario. Hazlo antes de bloquear o borrar.")
        st.markdown("3. **No respondas con agresión.** Bloquea y reporta la cuenta o el contenido en la plataforma.")
        st.markdown("4. **Cuéntaselo a alguien de confianza:** familia, amigos o docentes.")
        st.markdown("5. **Acude a la universidad.** Bienestar Universitario puede orientarte y acompañarte.")
    with r2:
        st.subheader("Cómo guardar evidencia")
        st.markdown("• Toma capturas donde se vea el mensaje completo, el nombre de usuario y la fecha y hora.")
        st.markdown("• Copia el enlace de la publicación o del perfil.")
        st.markdown("• Guarda las capturas en un lugar seguro (por ejemplo, un correo o carpeta solo tuya).")
        st.markdown("• No edites las capturas.")
        st.subheader("Si quieres apoyar a alguien")
        st.markdown("• Escúchalo sin juzgar y no le preguntes qué hizo para merecerlo.")
        st.markdown("• Ayúdale a guardar evidencia y a reportar.")
        st.markdown("• Ofrécete a acompañarle a pedir ayuda.")
        st.markdown("• No reenvíes ni comentes el contenido agresivo.")

    st.header(":green[Contactos en la UNAL Sede Bogotá]", text_alignment="center")
    st.subheader("División de Acompañamiento integral, Bienestar Universitario")
    st.markdown("• Ciudad Universitaria, Edificio 103 (Polideportivo), piso 2")
    st.markdown("• Correo: aaintegral@unal.edu.co")
    st.markdown("• Teléfono: (601) 316 5000, ext. 17171 y 17172")
    st.subheader("Proyecto de género, Sede Bogotá")
    st.markdown("• Correo: proygenero_bog@unal.edu.co")
    st.divider()
    st.header(":red[Líneas de ayuda]", text_alignment="center")
    st.markdown("• 123: emergencias, si hay peligro inmediato.")
    st.markdown("• 155: línea de orientación a mujeres víctimas de violencia.")
    st.markdown("• 106: línea de apoyo emocional en Bogotá.")
    st.divider()
    st.header("Marco legal (Para tener en cuenta)", text_alignment="center")
    st.markdown(marcotxt)
    menu_barra()
    menu_prin(1.1)