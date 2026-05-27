import requests
import random

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/1509203531184214067/nks3JtSmZgkb7qgH08_nxXYFBOrCiFs_9NxcAAcRTNbCxCvASPgdtEuR-DxtXG5-bc-U"

def cazar_fangames_fnaf():
    # Buscamos en el catálogo de Game Jolt juegos con la etiqueta fnaf, ordenados por los mejores/populares
    url = "https://gamejolt.com/site-api/discover/games/fnaf?page=1"
    
    print("🔦 Encendiendo la linterna en los servidores de Game Jolt...")
    try:
        respuesta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if respuesta.status_code == 200:
            datos = respuesta.json()
            # Extraemos la lista de juegos del catálogo de Game Jolt
            juegos = datos.get("payload", {}).get("games", {}).get("iterable", [])
            
            # 🔀 Barajamos el mazo para que cada 3 días sea un juego completamente sorpresa
            random.shuffle(juegos)
            
            embeds = []
            contador = 0
            
            for juego in juegos:
                titulo = juego.get("title")
                resumen = juego.get("header_media_item", {}).get("content_url") or juego.get("img_thumbnail")
                enlace_slug = juego.get("slug")
                id_juego = juego.get("id")
                desarrollador = juego.get("developer", {}).get("name", "Creador Anónimo")
                
                # Intentamos armar una pequeña descripción o usamos una por defecto si viene vacía
                descripcion = f"Un increíble fangame de FNAF alojado en Game Jolt. Creado por un miembro de la comunidad."
                
                if not titulo or not enlace_slug:
                    continue
                    
                # Construimos el enlace real de Game Jolt
                url_juego = f"https://gamejolt.com/games/{enlace_slug}/{id_juego}"
                
                # 🎨 DISEÑO OSCURO / TERROR PARA DISCORD
                embed = {
                    "author": {
                        "name": f"🐻 FANGAME DESTACADO POR: {desarrollador.upper()}",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png" # Icono de garra/terror
                    },
                    "title": titulo,
                    "url": url_juego,
                    "description": f"*{descripcion}*\n\n¡Ideal para jugar este fin de semana con las luces apagadas! 🔦",
                    "color": 10038562,  # Rojo carmesí oscuro tipo Fazbear
                    "image": {"url": resumen} if resumen else None, # Captura del juego en grande
                    "footer": {
                        "text": "👁️ GORDOBOT FAZBEAR • ARCHIVOS DE LA COMUNIDAD",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png"
                    }
                }
                
                embeds.append(embed)
                contador += 1
                
                # Con 1 o 2 fangames de calidad cada 3 días es más que suficiente para mantener el hype
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "⚠️ ❗ **【 ALERTA DE NUEVO ARCHIVO: REPORTE FAZBEAR 】** ❗ ⚠️\n*Se han detectado transmisiones de fangames altamente populares en Game Jolt. Proceda con precaución:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear enviado con éxito a Discord! 🐻🎉")
            else:
                print("⚠️ No se encontraron fangames disponibles en este momento.")
        else:
            print(f"❌ No se pudo conectar a Game Jolt. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()