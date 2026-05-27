import requests
import random
import xml.etree.ElementTree as ET

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/1509203531184214067/nks3JtSmZgkb7qgH08_nxXYFBOrCiFs_9NxcAAcRTNbCxCvASPgdtEuR-DxtXG5-bc-U"

def cazar_fangames_fnaf():
    # Usamos el feed RSS oficial de itch.io para la etiqueta FNAF
    url = "https://itch.io/games/tag-fnaf.xml"
    
    print("🔦 Sincronizando radares con el feed Fazbear de Itch.io...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        respuesta = requests.get(url, headers=headers)
        
        if respuesta.status_code == 200:
            # Parseamos el XML estructurado del feed
            raiz = ET.fromstring(respuesta.content)
            
            # Buscamos todos los elementos <item>
            items = raiz.findall('.//item')
            
            if not items:
                print("⚠️ El servidor respondió, pero el feed venía vacío.")
                return
                
            # 🔀 Mezclamos los juegos para asegurar variedad total
            random.shuffle(items)
            
            embeds = []
            contador = 0
            
            # Espacios de nombres para extraer imágenes del feed de itch.io
            ns = {'im': 'http://itch.io/rss'}
            
            for item in items:
                titulo = item.find('title').text if item.find('title') is not None else "Fangame de FNAF"
                url_juego = item.find('link').text if item.find('link') is not None else "https://itch.io"
                descripcion_raw = item.find('description').text if item.find('description') is not None else ""
                
                # Buscamos la imagen de portada usando el formato nativo del feed de itch
                imagen_tag = item.find('im:image', ns)
                imagen_url = imagen_tag.text if imagen_tag is not None else None
                
                # Limpieza estética del texto original
                if descripcion_raw:
                    import re
                    descripcion = re.sub(r'<[^>]*>', '', descripcion_raw).strip() # Quita código HTML residual
                else:
                    descripcion = ""
                
                if not descripcion or len(descripcion) == 0:
                    descripcion = "Un espeluznante fangame inspirado en las noches de terror de Freddy Fazbear."
                    
                if len(descripcion) > 160:
                    descripcion = descripcion[:157] + "..."
                
                # 🎨 DISEÑO TERROR PREMIUM (Rojo Fazbear)
                embed = {
                    "author": {
                        "name": "🐻 FANGAME DE FNAF DETECTADO",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png"
                    },
                    "title": titulo,
                    "url": url_juego,
                    "description": f"*{descripcion}*\n\n🔋 **Estado:** `Transmisión Activa`\n🕹️ **Plataforma:** `Itch.io` (Feed)",
                    "color": 10038562, # Rojo oscuro
                    "image": {"url": imagen_url} if imagen_url else None,
                    "footer": {
                        "text": "👁️ GORDOBOT FAZBEAR • ARCHIVOS DE SEGURIDAD",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png"
                    }
                }
                
                embeds.append(embed)
                contador += 1
                
                # Mandamos una dosis doble de juegos sorpresa
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "⚠️ ❗ **【 ALERTA DE NUEVO ARCHIVO: REPORTE FAZBEAR 】** ❗ ⚠️\n*Nuestros sensores detectaron transmisiones de fangames activos en la red. Proceda con precaución:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear enviado con éxito a Discord desde el Feed! 🐻🎉")
            else:
                print("⚠️ Error al estructurar las tarjetas.")
                
        else:
            print(f"❌ Error de conexión con el feed de Itch.io. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error crítico en el parseador XML: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()