# Aletheia: taller de videos con ManimGX

Videos matemáticos (sobre todo de geometría en 3D) hechos con ManimGX: escenas en Python que se
renderizan en la GPU a MP4, con música, efectos y narración. Un video por carpeta en `videos/`.

**Fuente de verdad**: https://manimgx.academa.ai/llms.txt. Antes de usar una clase o un argumento
que no aparece en este repo, búscalo en https://manimgx.academa.ai/llms-full.txt; un nombre
adivinado es un bug. La skill `manimgx` (`.claude/skills/`) resume el mismo flujo.

## Reglas duras

- ManimGX es otro motor, no el paquete `manim`. Cada escena empieza con `import manimgx as m`.
- Python 3.13 o 3.14 (`.python-version` fija 3.14). El entorno es `.venv`, creado con `uv sync`.
- La API es la de Manim CE y todo cuelga de `m.`: `m.Create`, `m.MathTex`, `m.UP`, `m.BLUE`.
  `ShowCreation` y los demás nombres de manimgl o de módulos internos no existen.
- Se instalan solo las dependencias de `pyproject.toml`. ManimGX trae el texto y la matemática (Typst)
  y la codificación del video, así que `manim`, ffmpeg y LaTeX sobran.
- LaTeX siempre en strings crudos: `m.MathTex(r"\frac{a}{b}")`.

## Comandos

Desde la raíz, con el script (Windows, PowerShell):

```powershell
./scripts/mgx.ps1 inspect <video> [-Time "1.5,end"]   # storyboard + timeline, sin video
./scripts/mgx.ps1 draft   <video>                     # 1280x720 a 30 fps -> draft.mp4
./scripts/mgx.ps1 final   <video>                     # 1920x1080 a 60 fps
./scripts/mgx.ps1 present <video>                     # secciones como diapositivas en el navegador
```

Si un archivo tiene varias escenas, añade `-Scene NombreEscena`. Debajo están los comandos de
[Command line](https://manimgx.academa.ai/reference/rendering/command-line/index.md):

- `uv run manimgx inspect videos/<video>/scene.py` (`-t 1.5,end` para instantes concretos, `-o detalle.png`).
- `uv run manimgx render videos/<video>/scene.py [NombreEscena]` (1080p60; `-r 1280x720 --fps 30` para borrador).
- `uv run manimgx present ...` muestra como diapositivas las secciones que abre `self.next_section("nombre")`.

El MP4 se escribe junto a `scene.py`. Al terminar un render, ábreselo al usuario
(`Invoke-Item <ruta>`; en macOS `open`, en Linux `xdg-open`) y dile la ruta. El script ya lo hace.

## Flujo por video

1. Escribir o editar `videos/<video>/scene.py`.
2. `uv run ty check`, hasta que salga limpio (ty conoce cada keyword de ManimGX).
3. `inspect` y **mirar los .png del storyboard**. En 3D no hay chequeos de layout (`layout: not
   checked`), así que el visto bueno es tuyo: encuadre, solapes, texto legible.
4. `draft` y revisar el movimiento, no solo los fotogramas.
5. `final` solo cuando el borrador esté bien.

## Reglas de escena

- El tiempo solo avanza en `self.play(...)` (1 s salvo `run_time=`) y `self.wait(s)`. `self.add`
  muestra sin animar.
- El marco mide 14.2 x 8 unidades y está centrado en el origen. Todo dentro de x ∈ [-7, 7] e
  y ∈ [-4, 4].
- Los updaters y `always_redraw` derivan su estado de un `ValueTracker`, del tiempo o de otros
  objetos. Así el movimiento es el mismo a cualquier fps.
- En 3D: `m.ThreeDScene`, `set_camera_orientation`/`move_camera` y títulos con
  `add_fixed_in_frame_mobjects`. Ver [Camera and 3D](https://manimgx.academa.ai/user-guide/camera-and-3d/index.md).

## Sonido y voz

Referencia: [Sound and voice](https://manimgx.academa.ai/user-guide/sound-and-voice/index.md).

- Música de fondo en bucle, quieta bajo la voz:
  `music = self.add_sound(audio.pad().gain(-22).fade_in(2).loop().duck())`; al final
  `music.stop(fade=2)`. Un bucle va siempre con `add_sound` (`play` lo rechaza), y se apaga con
  `stop(fade=...)`, porque `fade_out` necesita un final.
- Efectos de 1 s como máximo, dentro del play: `self.play(m.Create(x), audio.whoosh())`.
  `common/audio.py` los sintetiza con `m.Sound.of`. Los archivos propios van en `videos/<video>/assets/`.
- Narración en español con `self.say("Texto con [palabras] y [más palabras].", anim1, anim2)`: una
  animación por corchete, en el mismo orden. Los corchetes son solo para animaciones; las etiquetas
  de Eleven v3 (`[whispers]`) chocarían con ellos.
- Voz por defecto, como atributo de la clase:
  `voice = m.voices.Fal("fal-ai/elevenlabs/tts/eleven-v3", voice="...", stability=0.5, language_code="es")`.
- `FAL_KEY` existe solo como variable de entorno. Su valor nunca se imprime, se muestra ni se escribe
  en un archivo (`.env.example` lista solo el nombre).
- **Coste**: unos $0.10 por 1.000 caracteres (fal, Eleven v3). Lo dicho se guarda en
  `videos/<video>/voice/` (audio + JSON por frase), que se versiona y se conserva siempre: con ella
  se re-renderiza sin pagar y sin conexión. Cambiar una frase vuelve a cobrar solo esa frase.
- Cualquier comando (`inspect` incluido) sobre una escena con `self.say` sintetiza las frases que
  falten en `voice/`. Pide confirmación al usuario antes de ejecutarlo si hay frases nuevas o
  cambiadas. `mgx.ps1` se niega con la caché vacía salvo `-AllowVoiceSpend`.

## Estilo visual

- Llama a `style.apply()` (de `common/style.py`) justo tras los imports: pone el fondo `#0B0B14`.
- Paleta: `style.CYAN`, `style.MAGENTA` y `style.AMBER` para los objetos; `style.INK` para el texto;
  `style.DIM` para lo secundario. Un color nuevo del taller se añade en `style.py`.
- Movimientos suaves (rate func por defecto, `run_time` de 1.5 a 3 s en lo importante). En 3D,
  cámara con `begin_ambient_camera_rotation(rate≈0.15)`.
- Texto pequeño y limpio: `style.TITLE_SIZE` y `style.TEXT_SIZE`, títulos en una esquina y una idea
  por rótulo.

## Carpetas y nombres

```
common/style.py, common/audio.py   compartidos; se importan con `from common import audio, style`
videos/<tema-en-kebab-case>/
  scene.py      una escena principal (clase en inglés, CamelCase)
  assets/       música y efectos propios de ese video
  voice/        caché de voz que crea ManimGX: se versiona y se conserva
docs/ideas.md   backlog de temas; al empezar uno, márcalo como en curso
```

Todo lo generado (`*.mp4`, `*.srt`, `*.storyboard*.png`, `.html` y `.pdf` de `present`) está en
`.gitignore`.

## Cuando algo falla

- Lee el error entero: ManimGX indica la línea de `scene.py` y, si el nombre está mal, cuál es el
  correcto (`ShowCreation is Create in ManimGX`). Arregla la causa y conserva el contenido de la
  escena; recortarla para que pase no cuenta como arreglo.
- `no GPU adapter`: el comando corrió en un sandbox que oculta la GPU. Ejecútalo fuera del sandbox o
  pide aprobación al usuario.

## Enlaces

- [llms.txt](https://manimgx.academa.ai/llms.txt) · [llms-full.txt](https://manimgx.academa.ai/llms-full.txt)
- [Camera and 3D](https://manimgx.academa.ai/user-guide/camera-and-3d/index.md) · [Surfaces and solids](https://manimgx.academa.ai/reference/camera-and-3d/surfaces-and-solids/index.md)
- [Sound and voice](https://manimgx.academa.ai/user-guide/sound-and-voice/index.md) · [Voice](https://manimgx.academa.ai/reference/sound/voice/index.md)
- [Command line](https://manimgx.academa.ai/reference/rendering/command-line/index.md) · [Galería](https://manimgx.academa.ai/gallery/index.md)
