from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from qr_generator import generar_qr_con_logo
import io
from urllib.parse import urlparse
import base64
import re

app = FastAPI(title="Xerador de Códigos QR - UDC")

def validar_dominio_udc(texto: str) -> bool:
    """Valida si la URL pertenece a los dominios permitidos de la UDC."""
    try:
        if not texto.startswith(('http://', 'https://')):
            return False
        parsed = urlparse(texto)
        dominio = parsed.netloc.lower()
        return dominio.endswith('udc.es') or dominio.endswith('udc.gal')
    except:
        return False

def sanitizar_nombre_archivo(titulo: str) -> str:
    """Convierte el título en un nombre de archivo válido y seguro.
    - Elimina caracteres especiales y acentos
    - Reemplaza espacios con guiones bajos
    - Asegura que el nombre sea ASCII válido
    """
    if not titulo:
        return "qr_udc"
    
    # Mapeo de caracteres especiales a sus equivalentes ASCII
    caracteres_especiales = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u'
    }
    
    # Reemplazar caracteres especiales
    for especial, normal in caracteres_especiales.items():
        titulo = titulo.replace(especial, normal)
    
    # Convertir espacios y otros caracteres no válidos a guiones bajos
    # Solo permitir letras, números y guiones bajos
    titulo_limpio = ""
    for char in titulo:
        if char.isalnum():
            titulo_limpio += char
        else:
            titulo_limpio += "_"
    
    # Eliminar guiones bajos múltiples consecutivos
    while "__" in titulo_limpio:
        titulo_limpio = titulo_limpio.replace("__", "_")
    
    # Eliminar guiones bajos al inicio y final
    titulo_limpio = titulo_limpio.strip("_")
    
    # Si después de la limpieza no queda nada, usar nombre por defecto
    return titulo_limpio if titulo_limpio else "qr_udc"

@app.get("/", response_class=HTMLResponse)
def formulario():
    return """
    <!DOCTYPE html>
    <html lang="gl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Xerador de QR da UDC</title>
            <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
            <style>
                :root {
                    --udc-primary: #D60E8C;
                    --udc-primary-dark: #A80B70;
                    --udc-primary-light: rgba(214, 14, 140, 0.1);
                    --udc-gray: #666666;
                    --udc-light: #f5f5f5;
                    --udc-white: #ffffff;
                    --udc-blue: #002B7F;
                }
                
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Open Sans', sans-serif;
                    line-height: 1.6;
                    background-color: var(--udc-light);
                    color: #333;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                }
                
                .header {
                    background: linear-gradient(135deg, var(--udc-primary-dark), var(--udc-primary));
                    color: var(--udc-white);
                    padding: 2rem 0;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 2rem;
                }
                
                .header h1 {
                    font-size: 2rem;
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                }
                
                .header div {
                    font-size: 1.1rem;
                    opacity: 0.9;
                }
                
                .container {
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 2rem;
                    background: var(--udc-white);
                    border-radius: 12px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    text-align: center;
                }
                
                .form-group {
                    margin-bottom: 1.5rem;
                    background: var(--udc-white);
                    padding: 1.5rem;
                    border-radius: 8px;
                    border: 1px solid rgba(0,0,0,0.1);
                }
                
                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    color: var(--udc-gray);
                    font-weight: 600;
                    font-size: 0.95rem;
                }
                
                input[type="url"],
                input[type="text"] {
                    width: 100%;
                    padding: 0.75rem;
                    border: 2px solid #ddd;
                    border-radius: 6px;
                    font-size: 1rem;
                    transition: all 0.3s ease;
                    background-color: var(--udc-white);
                }
                
                input[type="url"]:focus,
                input[type="text"]:focus {
                    outline: none;
                    border-color: var(--udc-primary);
                    box-shadow: 0 0 0 3px var(--udc-primary-light);
                }
                
                .nota {
                    color: var(--udc-gray);
                    font-size: 0.85rem;
                    margin-top: 0.5rem;
                    padding-left: 0.25rem;
                }
                
                .error-message {
                    color: #dc3545;
                    font-size: 0.85rem;
                    margin-top: 0.5rem;
                    padding: 0.5rem;
                    background-color: rgba(220, 53, 69, 0.1);
                    border-radius: 4px;
                    display: none;
                }
                
                input.error {
                    border-color: #dc3545;
                }
                
                input.error:focus {
                    box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
                }
                
                .style-selectors {
                    display: flex;
                    justify-content: center;
                    gap: 3rem;
                    margin-top: 1rem;
                }
                
                .selector {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .selector > label {
                    font-weight: 600;
                    color: var(--udc-gray);
                    margin-bottom: 0.25rem;
                }
                
                .button-group {
                    display: flex;
                    gap: 0.5rem;
                }
                
                .style-radio {
                    display: none;
                }
                
                .style-button {
                    padding: 0.5rem 1.5rem;
                    border: 2px solid var(--udc-primary);
                    border-radius: 6px;
                    font-size: 0.9rem;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    background-color: var(--udc-white);
                    color: var(--udc-primary);
                }
                
                .style-radio:checked + .style-button {
                    background-color: var(--udc-primary);
                    color: var(--udc-white);
                }
                
                .style-button:hover {
                    background-color: var(--udc-primary-light);
                }
                
                .style-radio:checked + .style-button:hover {
                    background-color: var(--udc-primary-dark);
                }
                
                button:disabled {
                    background-color: var(--udc-gray);
                    cursor: not-allowed;
                    transform: none;
                    box-shadow: none;
                }
                
                button:disabled:hover {
                    background-color: var(--udc-gray);
                    transform: none;
                    box-shadow: none;
                }
                
                button[type="submit"] {
                    background-color: var(--udc-primary);
                    color: var(--udc-white);
                    border: none;
                    padding: 0.75rem 2rem;
                    font-size: 1rem;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: block;
                    width: 100%;
                    max-width: 300px;
                    margin: 2rem auto 0;
                    font-weight: 600;
                }
                
                button[type="submit"]:hover {
                    background-color: var(--udc-primary-dark);
                    transform: translateY(-1px);
                    box-shadow: 0 2px 4px rgba(214, 14, 140, 0.2);
                }
                
                button[type="submit"]:active {
                    transform: translateY(0);
                    box-shadow: none;
                }
                
                .footer {
                    margin-top: auto;
                    padding: 1rem;
                    background-color: var(--udc-white);
                    border-top: 1px solid rgba(0,0,0,0.1);
                    text-align: center;
                    font-size: 0.9rem;
                    color: var(--udc-gray);
                }
                
                .footer a {
                    color: var(--udc-primary);
                    text-decoration: none;
                    transition: color 0.3s ease;
                }
                
                .footer a:hover {
                    color: var(--udc-primary-dark);
                    text-decoration: underline;
                }
                
                @media (max-width: 768px) {
                    .container {
                        margin: 1rem;
                        padding: 1rem;
                    }
                    
                    .style-selectors {
                        flex-direction: column;
                        align-items: center;
                        gap: 1.5rem;
                    }
                }
            </style>
        </head>
        <body>
            <header class="header">
                <h1>Xerador de Códigos QR</h1>
                <div>Universidade da Coruña</div>
            </header>
            
            <div class="container">
                <form action="/xerar_qr" method="post" id="qrForm">
                    <div class="form-group">
                        <label>Título (opcional)</label>
                        <input type="text" name="titulo" placeholder="Título para o código QR"/>
                        <div class="nota">O título aparecerá xunto co código QR xerado</div>
                    </div>

                    <div class="form-group">
                        <label>URL</label>
                        <input type="url" name="texto" id="urlInput" required placeholder="https://www.udc.es/..." />
                        <div class="nota">Só se permiten URLs dos dominios udc.es e udc.gal</div>
                        <div class="error-message" id="urlError">A URL debe pertencer aos dominios udc.es ou udc.gal</div>
                    </div>
                    
                    <div class="form-group">
                        <label>Estilo</label>
                        <div class="style-selectors">
                            <div class="selector">
                                <label>QR:</label>
                                <div class="button-group">
                                    <input type="radio" id="qr_negro" name="estilo" value="blanco_negro" checked class="style-radio">
                                    <label for="qr_negro" class="style-button">Negro</label>
                                    <input type="radio" id="qr_color" name="estilo" value="corporativo" class="style-radio">
                                    <label for="qr_color" class="style-button">Cor</label>
                                </div>
                            </div>
                            <div class="selector">
                                <label>Logo:</label>
                                <div class="button-group">
                                    <input type="radio" id="logo_negro" name="logo_color" value="false" class="style-radio">
                                    <label for="logo_negro" class="style-button">Negro</label>
                                    <input type="radio" id="logo_color" name="logo_color" value="true" checked class="style-radio">
                                    <label for="logo_color" class="style-button">Cor</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <button type="submit">Xerar código QR</button>
                </form>
            </div>

            <footer class="footer">
                <p>© 2025 Universidade da Coruña - <a href="https://github.com/cjescudero/qr_udc" target="_blank">Repositorio en GitHub</a> - Licenza <a href="https://github.com/cjescudero/qr_udc/blob/main/LICENSE" target="_blank">MIT</a></p>
            </footer>

            <script>
                function validarDominioUDC(url) {
                    try {
                        const urlObj = new URL(url);
                        const dominio = urlObj.hostname.toLowerCase();
                        return dominio.endsWith('udc.es') || dominio.endsWith('udc.gal');
                    } catch {
                        return false;
                    }
                }

                const urlInput = document.getElementById('urlInput');
                const urlError = document.getElementById('urlError');
                const form = document.getElementById('qrForm');

                form.addEventListener('submit', function(e) {
                    if (!validarDominioUDC(urlInput.value)) {
                        e.preventDefault();
                        urlError.style.display = 'block';
                        urlInput.classList.add('error');
                    } else {
                        urlError.style.display = 'none';
                        urlInput.classList.remove('error');
                    }
                });
            </script>
        </body>
    </html>
    """

@app.post("/xerar_qr", response_class=HTMLResponse)
def xerar_qr(
    texto: str = Form(...),
    estilo: str = Form("blanco_negro"),
    logo_color: bool = Form(True),
    titulo: str = Form("")
):
    if not validar_dominio_udc(texto):
        raise HTTPException(
            status_code=400,
            detail="Só se permiten URLs dos dominios udc.es e udc.gal"
        )
    
    qr_bytes = generar_qr_con_logo(texto, estilo=estilo, logo_color=logo_color, titulo=titulo)
    qr_base64 = base64.b64encode(qr_bytes).decode()
    nombre_archivo = sanitizar_nombre_archivo(titulo)
    
    return f"""
    <!DOCTYPE html>
    <html lang="gl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Código QR Xerado - UDC</title>
            <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --udc-primary: #D60E8C;
                    --udc-primary-dark: #A80B70;
                    --udc-primary-light: rgba(214, 14, 140, 0.1);
                    --udc-gray: #666666;
                    --udc-light: #f5f5f5;
                    --udc-white: #ffffff;
                }}
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Open Sans', sans-serif;
                    line-height: 1.6;
                    background-color: var(--udc-light);
                    color: #333;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                }}
                
                .header {{
                    background: linear-gradient(135deg, var(--udc-primary-dark), var(--udc-primary));
                    color: var(--udc-white);
                    padding: 2rem 0;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 2rem;
                }}
                
                .header h1 {{
                    font-size: 2rem;
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                }}
                
                .header div {{
                    font-size: 1.1rem;
                    opacity: 0.9;
                }}
                
                .container {{
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 2rem;
                    background: var(--udc-white);
                    border-radius: 12px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    text-align: center;
                }}
                
                .qr-container {{
                    margin: 1.5rem 0;
                    padding: 1rem;
                    background: var(--udc-white);
                    border-radius: 8px;
                    display: inline-block;
                }}
                
                .qr-image {{
                    max-width: 400px;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }}
                
                .url-info {{
                    margin: 1.5rem 0;
                    color: var(--udc-gray);
                    word-break: break-all;
                    font-size: 0.9rem;
                    padding: 0 1rem;
                }}
                
                .button-container {{
                    margin-top: 2rem;
                    display: flex;
                    gap: 1.5rem;
                    justify-content: center;
                    flex-wrap: wrap;
                    padding: 0 1rem;
                }}
                
                .button {{
                    padding: 1rem 2.5rem;
                    border-radius: 6px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                }}
                
                .button-primary {{
                    background-color: var(--udc-primary);
                    color: var(--udc-white);
                    border: none;
                }}
                
                .button-primary:hover {{
                    background-color: var(--udc-primary-dark);
                    transform: translateY(-1px);
                    box-shadow: 0 2px 4px rgba(230, 0, 126, 0.2);
                }}
                
                .button-secondary {{
                    background-color: var(--udc-white);
                    color: var(--udc-primary);
                    border: 2px solid var(--udc-primary);
                }}
                
                .button-secondary:hover {{
                    background-color: var(--udc-primary-light);
                    transform: translateY(-1px);
                }}
                
                .footer {{
                    margin-top: auto;
                    padding: 1rem;
                    background-color: var(--udc-white);
                    border-top: 1px solid rgba(0,0,0,0.1);
                    text-align: center;
                    font-size: 0.9rem;
                    color: var(--udc-gray);
                }}
                
                .footer a {{
                    color: var(--udc-primary);
                    text-decoration: none;
                    transition: color 0.3s ease;
                }}
                
                .footer a:hover {{
                    color: var(--udc-primary-dark);
                    text-decoration: underline;
                }}
                
                @media (max-width: 768px) {{
                    .container {{
                        margin: 1rem;
                        padding: 1rem;
                    }}
                    
                    .qr-image {{
                        max-width: 100%;
                    }}
                    
                    .button-container {{
                        flex-direction: column;
                        align-items: stretch;
                    }}
                    
                    .button {{
                        text-align: center;
                        padding: 0.875rem 2rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <header class="header">
                <h1>Código QR Xerado</h1>
                <div>Universidade da Coruña</div>
            </header>
            
            <div class="container">
                <div class="qr-container">
                    <img src="data:image/png;base64,{qr_base64}" alt="Código QR" class="qr-image">
                </div>
                
                <div class="url-info">
                    URL: {texto}
                </div>
                
                <div class="button-container">
                    <a href="data:image/png;base64,{qr_base64}" download="{nombre_archivo}.png" class="button button-primary">
                        Descargar QR
                    </a>
                    <a href="/" class="button button-secondary">
                        Xerar outro QR
                    </a>
                </div>
            </div>

            <footer class="footer">
                <p>© 2025 Universidade da Coruña - <a href="https://github.com/cjescudero/qr_udc" target="_blank">Repositorio en GitHub</a> - Licenza <a href="https://github.com/cjescudero/qr_udc/blob/main/LICENSE" target="_blank">MIT</a></p>
            </footer>
        </body>
    </html>
    """

@app.get("/descargar_qr")
def descargar_qr(qr_base64: str):
    qr_bytes = base64.b64decode(qr_base64)
    return StreamingResponse(
        io.BytesIO(qr_bytes),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=qr_udc.png"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
