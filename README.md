# Xerador de Códigos QR - UDC

Aplicación web para xerar códigos QR personalizados para URLs dos dominios da Universidade da Coruña (UDC).

![Logo UDC](https://udc.es/export/sites/udc/identidadecorporativa/_galeria_down/png/Simbolo_logo_cor.png_2063069239.png)

## Características

- Xeración de códigos QR para URLs dos dominios udc.es e udc.gal
- Personalización do estilo do código QR (negro ou cor corporativa)
- Opción de logo UDC en negro ou cor
- Interface web intuitiva e responsive
- Validación automática de dominios permitidos
- Descarga directa dos códigos QR xerados en formato PNG

## Requisitos

- Python 3.8 ou superior
- FastAPI
- uvicorn
- Outras dependencias (especificadas en requirements.txt)

## Instalación

1. Clona o repositorio:
```bash
git clone https://github.com/teu-usuario/qr_udc.git
cd qr_udc
```

2. Crea e activa un entorno virtual con uv:
```bash
uv venv
source .venv/bin/activate  # En Linux/macOS
# ou
.venv\Scripts\activate  # En Windows
```

3. Instala as dependencias:
```bash
uv pip install -r requirements.txt
```

## Uso

1. Inicia o servidor:
```bash
python main.py
```

2. Abre o navegador e accede a:
```
http://localhost:8000
```

3. Na interface web:
   - Introduce unha URL válida dos dominios udc.es ou udc.gal
   - (Opcional) Engade un título para o código QR
   - Selecciona o estilo do código QR (negro ou cor)
   - Selecciona o estilo do logo (negro ou cor)
   - Fai clic en "Xerar código QR"

## Contribucións

As contribucións son benvidas! Por favor, sinte libre de:

1. Facer un fork do proxecto
2. Crear unha rama para a túa funcionalidade (`git checkout -b feature/NovaFuncionalidade`)
3. Facer commit dos teus cambios (`git commit -am 'Engadida nova funcionalidade'`)
4. Facer push á rama (`git push origin feature/NovaFuncionalidade`)
5. Crear un Pull Request

## Licenza

Este proxecto está baixo a licenza MIT - consulta o arquivo [LICENSE](LICENSE) para máis detalles.

## Contacto

Para calquera consulta ou suxestión, por favor, abre un issue no repositorio. 