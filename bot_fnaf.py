import requests
import random

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/150920353118421406/..." # <-- Tu webhook ya guardado

def cazar_fangames_fnaf():
    # Conectamos al buscador oficial de itch.io filtrando por la etiqueta 'fnaf'
    url = "https://itch.io/games/tag-fnaf.json"
    
    print("🔦 Escaneando los servidores de Itch.io en busca de anomalías Fazbear...")
    try:
        respuesta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if respuesta.status_code == 200:
            datos = respuesta.json()
            juegos = datos.get("games", [])
            
            if not juegos:
                print("⚠️ No se encontraron juegos con esa etiqueta en este momento.")
                return
                
            # 🔀 Mezclamos el mazo de juegos para asegurar variedad total
            random.shuffle(juegos)
            
            embeds = []
            contador = 0
            
            for juego in juegos:
                titulo = juego.get("title")
                url_juego = juego.get("url")
                imagen_url = juego.get("cover_url")
                descripcion = juego.get("short_text")
                precio = juego.get("price", "Gratis")
                
                # Si no trae descripción, le inventamos una bien estática
                if not descripcion or len(descripcion.strip()) == 0:
                    descripcion = "Un espeluznante fangame inspirado en el universo de Five Nights at Freddy's creado por la comunidad."
                
                if not titulo or not url_juego:
                    continue
                
                # Recortamos textos largos para mantener el orden
                if len(descripcion) > 160:
                    descripcion = descripcion[:157] + "..."
                
                # 🎨 DISEÑO TERROR PREMIUM (Rojo Carmesí)
                embed = {
                    "author": {
                        "name": f"🐻 FANGAME DETECTADO EN ITCH.IO",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png"
                    },
                    "title": titulo,
                    "url": url_juego,
                    "description": f"*{descripcion}*\n\n💰 **Costo:** `{precio}`\n🕹️ **Plataforma:** `Itch.io`",
                    "color": 10038562, # Rojo Fazbear oscuro
                    "image": {"url": imagen_url} if imagen_url else None,
                    "footer": {
                        "text": "👁️ GORDOBOT FAZBEAR • ARCHIVOS DE SEGURIDAD",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png"
                    }
                }
                
                embeds.append(embed)
                contador += 1
                
                # Juntamos 2 fangames aleatorios
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "⚠️ ❗ **【 ALERTA DE NUEVO ARCHIVO: REPORTE FAZBEAR 】** ❗ ⚠️\n*Nuestros sensores detectaron transmisiones de fangames activos en la red. Proceda con precaución:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear enviado con éxito a Discord desde Itch.io! 🐻🎉")
            else:
                print("⚠️ Las notas no pudieron transformarse en Embeds.")
                
        else:
            print(f"❌ Error de conexión con Itch.io. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error crítico en el bot: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()