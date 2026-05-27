import requests
import random
import re

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/1509203531184214067/nks3JtSmZgkb7qgH08_nxXYFBOrCiFs_9NxcAAcRTNbCxCvASPgdtEuR-DxtXG5-bc-U" # <-- Tu webhook ya está puesto aquí

def cazar_fangames_fnaf():
    # Usamos el Feed RSS público de la comunidad de FNAF en Game Jolt (Es antibloqueos)
    url = "https://gamejolt.com/feed/tag/fnaf"
    
    print("🔦 Rastreando transmisiones en el feed de Freddy Fazbear...")
    try:
        respuesta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if respuesta.status_code == 200:
            texto_xml = respuesta.text
            
            # Buscamos los bloques de cada juego/publicación (<item>)
            items = re.findall(r'<item>(.*?)</item>', texto_xml, re.DOTALL)
            
            if not items:
                print("⚠️ El feed no devolvió publicaciones en este instante.")
                return
                
            # 🔀 Mezclamos las publicaciones para que varíen cada 3 días
            random.shuffle(items)
            
            embeds = []
            contador = 0
            
            for item in items:
                # Extraemos el título, el enlace y la descripción usando expresiones regulares simples
                titulo_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item) or re.search(r'<title>(.*?)</title>', item)
                enlace_match = re.search(r'<link>(.*?)</link>', item)
                desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item) or re.search(r'<description>(.*?)</description>', item)
                
                titulo = titulo_match.group(1) if titulo_match else "Fangame Misterioso"
                url_juego = enlace_match.group(1).strip() if enlace_match else "https://gamejolt.com"
                descripcion_raw = desc_match.group(1) if desc_match else ""
                
                # Limpiamos etiquetas HTML raras que puedan venir en la descripción
                descripcion = re.sub(r'<[^>]*>', '', descripcion_raw).strip()
                if len(descripcion) > 150:
                    descripcion = descripcion[:147] + "..."
                if not descripcion:
                    descripcion = "¡Un proyecto interactivo de FNAF directo desde las cocinas de la comunidad!"
                
                # Intentamos pescar alguna imagen dentro de la publicación
                img_match = re.search(r'<media:content[^>]*url="(.*?)"', item) or re.search(r'src="(.*?)"', item)
                imagen_url = img_match.group(1) if img_match else None
                
                # 🎨 DISEÑO TERROR PREMIUM (Rojo Carmesí)
                embed = {
                    "author": {
                        "name": "🐻 FANGAME DE FNAF DETECTADO",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png"
                    },
                    "title": titulo,
                    "url": url_juego,
                    "description": f"*{descripcion}*\n\n🔋 **Estado:** `Transmisión Activa`\n🕹️ **Plataforma:** `Game Jolt`",
                    "color": 10038562, # Rojo Fazbear oscuro
                    "image": {"url": imagen_url} if imagen_url else None,
                    "footer": {
                        "text": "👁️ GORDOBOT FAZBEAR • ARCHIVOS SECRETOS DE LA PIZZERÍA",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png"
                    }
                }
                
                embeds.append(embed)
                contador += 1
                
                # Mandamos 2 fangames al azar en cada boletín
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "⚠️ ❗ **【 ALERTA DE NUEVO ARCHIVO: REPORTE FAZBEAR 】** ❗ ⚠️\n*Nuestros sensores detectaron actividad popular en los servidores de Game Jolt. Proceda bajo su propio riesgo:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear enviado con éxito a Discord! 🐻🎉")
            else:
                print("⚠️ No se pudieron estructurar tarjetas válidas.")
        else:
            print(f"❌ Error de servidor en Game Jolt. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error al procesar el feed: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()