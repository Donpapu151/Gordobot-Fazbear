import requests
import random
import re

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/1509203531184214067/nks3JtSmZgkb7qgH08_nxXYFBOrCiFs_9NxcAAcRTNbCxCvASPgdtEuR-DxtXG5-bc-U"

def cazar_fangames_fnaf():
    # Entramos a la página web normal de itch.io que vería cualquier usuario
    url = "https://itch.io/games/tag-fnaf"
    
    print("🔦 Escaneando el código de Itch.io en busca de anomalías Fazbear...")
    try:
        # Simulamos un navegador real (User-Agent) para que no nos bloquee nadie
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        respuesta = requests.get(url, headers=headers)
        
        if respuesta.status_code == 200:
            html = respuesta.text
            
            # Capturamos los bloques de juegos usando expresiones regulares en el HTML
            # Buscaremos los enlaces, títulos y las imágenes de portada
            juegos_encontrados = re.findall(r'class="game_link" href="(https://[^"]+)"[^>]*>(.*?)</a>', html)
            imagenes_encontradas = re.findall(r'data-background_image="([^"]+)"', html)
            descripciones_encontradas = re.findall(r'class="game_text"[^>]* title="([^"]+)"', html)

            if not juegos_encontrados:
                print("⚠️ No se pudieron extraer estructuras de juegos del HTML.")
                return
            
            # Emparejamos los datos recolectados en una lista limpia
            lista_juegos = []
            for i in range(min(len(juegos_encontrados), 15)):
                url_juego = juegos_encontrados[i][0]
                titulo = juegos_encontrados[i][1].strip()
                
                # Intentamos asociar su imagen y descripción correspondiente si existen
                img_url = imagenes_encontradas[i] if i < len(imagenes_encontradas) else None
                desc = descripciones_encontradas[i] if i < len(descripciones_encontradas) else "¡Un espeluznante fangame inspirado en el universo de Five Nights at Freddy's creado por la comunidad!"
                
                lista_juegos.append({
                    "titulo": titulo,
                    "url": url_juego,
                    "imagen": img_url,
                    "descripcion": desc
                })

            # 🔀 Mezclamos los juegos para que varíen cada 3 días
            random.shuffle(lista_juegos)
            
            embeds = []
            contador = 0
            
            for juego in lista_juegos:
                # 🎨 DISEÑO TERROR PREMIUM (Rojo Carmesí)
                embed = {
                    "author": {
                        "name": "🐻 FANGAME DE FNAF DETECTADO",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png"
                    },
                    "title": juego["titulo"],
                    "url": juego["url"],
                    "description": f"*{juego['descripcion']}*\n\n🔋 **Estado:** `Transmisión Activa`\n🕹️ **Plataforma:** `Itch.io` (Web)",
                    "color": 10038562, # Rojo Fazbear oscuro
                    "image": {"url": juego["imagen"]} if juego["imagen"] else None,
                    "footer": {
                        "text": "👁️ GORDOBOT FAZBEAR • ARCHIVOS DE SEGURIDAD",
                        "icon_url": "https://i.imgur.com/OcMRbT8.png"
                    }
                }
                
                embeds.append(embed)
                contador += 1
                
                # Mandamos un dúo de fangames sorpresa
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "⚠️ ❗ **【 ALERTA DE NUEVO ARCHIVO: REPORTE FAZBEAR 】** ❗ ⚠️\n*Nuestros sensores detectaron transmisiones de fangames activos en la red. Proceda con precaución:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear enviado con éxito a Discord desde el HTML de Itch.io! 🐻🎉")
            else:
                print("⚠️ Error al estructurar las tarjetas.")
        else:
            print(f"❌ Error al cargar la página. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Error crítico en el raspado: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()