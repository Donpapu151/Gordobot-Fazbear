import requests
import random
import re

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/1509203531184214067/nks3JtSmZgkb7qgH08_nxXYFBOrCiFs_9NxcAAcRTNbCxCvASPgdtEuR-DxtXG5-bc-U"

def cazar_fangames_fnaf():
    # Usamos la URL de búsqueda directa de itch.io que devuelve los resultados crudos en texto plano
    url = "https://itch.io/search?q=fnaf&format=json"
    
    print("🔦 Sincronizando radares con la base de datos de Itch.io...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        respuesta = requests.get(url, headers=headers)
        
        if respuesta.status_code == 200:
            # Conseguimos el texto completo de la página
            html = respuesta.text
            
            # Recolectamos de forma masiva links de juegos, imágenes y descripciones mediante patrones estables
            enlaces = re.findall(r'class="game_link" href="([^"]+)"\s*>([^<]+)</a>', html)
            imagenes = re.findall(r'data-background_image="([^"]+)"', html)
            descripciones = re.findall(r'class="game_text"[^>]*>([^<]+)</div>', html)
            
            if not enlaces:
                # Intento de respaldo si las clases cambian sutilmente
                enlaces = re.findall(r'href="(https://[^"]+/games/[^"]+)"', html)
                if not enlaces:
                    print("⚠️ Alerta: Los servidores de Itch.io no respondieron con datos legibles.")
                    return
            
            # Armamos la lista unificando las piezas encontradas
            lista_juegos = []
            for i in range(min(len(enlaces), 10)):
                # Manejamos si el patrón capturó tupla o texto individual
                if isinstance(enlaces[i], tuple):
                    url_juego = enlaces[i][0]
                    titulo = enlaces[i][1].strip()
                else:
                    url_juego = enlaces[i]
                    titulo = "Fangame de FNAF"
                
                # Asignamos portada y resumen si están disponibles en la tanda
                img_url = imagenes[i] if i < len(imagenes) else "https://i.imgur.com/u7f3bYV.png"
                desc = descripciones[i].strip() if i < len(descripciones) else "Un proyecto interactivo inspirado en el universo de Five Nights at Freddy's."
                
                # Ignoramos links de perfiles de usuario que se cuelen
                if "/games/" not in url_juego and not url_juego.split("//")[1].startswith("itch.io"):
                    lista_juegos.append({
                        "titulo": titulo if titulo != "Fangame de FNAF" else url_juego.split("/")[-1].replace("-", " ").title(),
                        "url": url_juego,
                        "imagen": img_url,
                        "descripcion": desc
                    })

            if not lista_juegos:
                print("⚠️ No se encontraron estructuras limpias de juegos.")
                return

            # 🔀 Mezclamos los resultados para asegurar sorpresas cada 3 días
            random.shuffle(lista_juegos)
            
            embeds = []
            contador = 0
            
            for juego in lista_juegos:
                # 🎨 DISEÑO TERROR PREMIUM (Rojo Fazbear)
                embed = {
                    "author": {
                        "name": "🐻 FANGAME DE FNAF DETECTADO",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png"
                    },
                    "title": juego["titulo"],
                    "url": juego["url"],
                    "description": f"*{juego['descripcion']}*\n\n🔋 **Estado:** `Transmisión Activa`\n🕹️ **Plataforma:** `Itch.io`",
                    "color": 10038562,
                    "image": {"url": juego["imagen"]} if juego["imagen"] else None,
                    "footer": {
                        "text": "👁️ GORDOBOT FAZBEAR • ARCHIVOS DE SEGURIDAD",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png"
                    }
                }
                embeds.append(embed)
                contador += 1
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "⚠️ ❗ **【 ALERTA DE NUEVO ARCHIVO: REPORTE FAZBEAR 】** ❗ ⚠️\n*Nuestros sensores detectaron transmisiones de fangames activos en la red. Proceda con precaución:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear enviado con éxito a Discord! 🐻🎉")
            else:
                print("⚠️ Error al construir las tarjetas de los juegos.")
        else:
            print(f"❌ Error de respuesta. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error crítico en el módulo de búsqueda: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()