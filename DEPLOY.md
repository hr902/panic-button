# Despliegue del bot de Slack en Python

Este proyecto ya esta preparado para funcionar con un slash command de Slack por `HTTP`.

## Como funciona ahora

- Slack envia el comando `/panic` a una URL publica
- Tu app Python recibe la solicitud en `/slack/events`
- La app valida la firma con `SLACK_SIGNING_SECRET`
- La app publica la alerta en el canal configurado en `ALERT_CHANNEL`

## Variables necesarias

- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `ALERT_CHANNEL`

## Archivos importantes

- `app.py`
- `requirements.txt`
- `render.yaml`
- `.env.example`

## Paso 1. Configurar Slack

En tu app de Slack:

1. Ve a `Slash Commands`
2. Abre `/panic`
3. En `Request URL` pon:

```text
https://TU-SERVICIO/slack/events
```

4. Guarda los cambios

Luego:

1. Ve a `Basic Information`
2. Copia el valor de `Signing Secret`
3. Guardalo como `SLACK_SIGNING_SECRET`

Tambien necesitas:

1. Ve a `OAuth & Permissions`
2. Confirmar que tienes:
   - `commands`
   - `chat:write`
3. Si agregaste permisos, pulsa `Reinstall to Workspace`

## Paso 2. Configurar el canal de alertas

`ALERT_CHANNEL` debe ser el ID real del canal, por ejemplo:

```text
C0123456789
```

No pongas el nombre visible del canal.

Si el canal es privado, invita al bot a ese canal.

## Paso 3. Desplegar

### Opcion recomendada: Render

1. Sube este proyecto a GitHub
2. Entra a Render
3. Crea un `Web Service`
4. Conecta el repositorio
5. Render usara:
   - `buildCommand`: `pip install -r requirements.txt`
   - `startCommand`: `gunicorn --bind 0.0.0.0:$PORT app:web_app`
6. Agrega las variables:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `ALERT_CHANNEL`
7. Despliega

Cuando Render te entregue la URL publica, usala en Slack como:

```text
https://TU-SERVICIO.onrender.com/slack/events
```

## Paso 4. Probar

1. Ejecuta `/panic`
2. Verifica que Slack responda `Alerta recibida. Estamos contigo.`
3. Verifica que llegue el mensaje al canal de alertas

## Prueba local opcional

Si solo quieres probar localmente:

```powershell
python app.py
```

Luego expones tu puerto con una herramienta tipo `ngrok` y usas esa URL temporal en Slack.

## Nota importante

Ya no necesitas `SLACK_APP_TOKEN` ni `Socket Mode`.

Esta version es la adecuada para produccion porque no depende de tener Python abierto en tu computador personal.
