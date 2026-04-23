# Boton de panico nativo en Slack

Esta opcion elimina la dependencia de `Python`, `VS Code` y una terminal abierta.

La idea es mover la alerta a un flujo nativo de Slack usando `Workflow Builder`.

## Que necesitas

- Un plan de Slack que incluya `Workflow Builder`
- Permiso para crear workflows en tu workspace
- Un canal de alertas, por ejemplo `#alertas`
- Idealmente un grupo de usuarios para emergencias, por ejemplo `@panic-responders`

## Resultado esperado

Cualquier persona de la empresa puede lanzar la alerta desde Slack, sin que tu computador tenga nada abierto.

## Opcion recomendada

Usa un workflow con:

- Trigger de tipo `Shortcut` si aparece en tu Slack
- Si no aparece, usa `Link trigger`
- Paso opcional de formulario para pedir detalle corto
- Paso para publicar la alerta en `#alertas`

## Configuracion recomendada

### 1. Crea un grupo de personas que deban reaccionar

En Slack, crea un `user group` como:

- `@panic-responders`

Agrega ahi a las personas o equipos que deben reaccionar cuando alguien active la alerta.

Esto evita tener que mantener una lista de personas dentro de Python.

### 2. Crea el workflow

En Slack:

1. Ve a `Tools` o `Automations`
2. Abre `Workflow Builder`
3. Crea un workflow nuevo desde cero
4. Ponle un nombre como `Boton de panico`

### 3. Elige el disparador

Usa uno de estos:

- `Shortcut`
  Es la mejor opcion si quieres que el usuario pueda buscarlo desde el menu de slash/shortcuts.

- `Link trigger`
  Es la mejor alternativa si tu Slack no muestra shortcut trigger. Puedes fijar el workflow en el tab `Workflows` o compartir el enlace en canales y canvases.

## Flujo sugerido

### Paso 1. Formulario

Agrega un formulario corto con campos como:

- `Tipo de alerta`
- `Sede o pais`
- `Descripcion breve`

Si quieres algo mas rapido, puedes omitir el formulario y mandar una alerta inmediata.

### Paso 2. Enviar mensaje al canal `#alertas`

Configura un paso de envio de mensaje al canal de alertas.

Texto sugerido:

```text
🚨 ALERTA DE PANICO
Persona: {{persona_que_inicio_el_workflow}}
Sede: {{sede_o_pais}}
Tipo: {{tipo_de_alerta}}
Detalle: {{descripcion_breve}}
Atencion: @panic-responders
```

Si no usas formulario:

```text
🚨 ALERTA DE PANICO
La persona {{persona_que_inicio_el_workflow}} activo una alerta.
Atencion: @panic-responders
```

### Paso 3. Confirmacion para quien lo activa

Agrega un paso de confirmacion o mensaje final:

```text
Tu alerta fue enviada correctamente al canal de emergencias.
```

## Donde dejarlo visible

Para que cualquiera lo use facilmente:

- Agregalo al tab `Workflows` del canal `#alertas`
- Comparte el enlace del workflow en un canvas o mensaje fijado
- Si usas `Shortcut`, pide a las personas escribir `/` y buscar `Boton de panico`

## Recomendacion importante

La version nativa funciona mejor si la alerta se publica en un canal central y se menciona un grupo como `@panic-responders`.

Eso es mas estable que intentar mandar mensajes directos individuales a muchas personas.

## Cuando no sirve esta opcion

No uses esta opcion si necesitas:

- Logica compleja por horarios o paises
- Consultar bases de datos
- Reglas avanzadas por usuario
- Integraciones personalizadas fuera de Slack

En esos casos conviene un servicio HTTP o una app alojada.

## Lo que cambia frente a Python

### Antes

- Dependias de `app.py`
- Dependias de `Socket Mode`
- Dependias de una terminal abierta

### Ahora

- Slack ejecuta el workflow dentro de Slack
- No necesitas tener Python corriendo
- El uso queda disponible para mas personas del workspace

## Validacion final

Antes de publicarlo, prueba esto:

1. Ejecuta el workflow con un usuario normal
2. Verifica que llegue mensaje a `#alertas`
3. Verifica que se mencione el grupo `@panic-responders`
4. Verifica que el usuario vea el mensaje de confirmacion

## Fuentes oficiales

- https://slack.com/help/articles/360035692513-Guide-to-Slack-Workflow-Builder
- https://slack.com/help/articles/201259356-Slash-commands-in-Slack
- https://docs.slack.dev/workflows/workflow-builder/
