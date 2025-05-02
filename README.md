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
- Soporte para títulos personalizados nos códigos QR
- Deseño adaptativo para dispositivos móbiles

## Requisitos

- Python 3.8 ou superior
- uv (xestor de paquetes e entornos virtuais)
- FastAPI
- uvicorn
- qrcode
- Pillow
- python-dotenv

## Instalación

1. Instala uv se aínda non o tes:
```bash
python -m pip install uv
```

2. Clona o repositorio:
```bash
git clone https://github.com/cjescudero/qr_udc.git
cd qr_udc
```

3. Crea e activa un entorno virtual con uv:
```bash
uv venv
source .venv/bin/activate  # En Linux/macOS
# ou
.venv\Scripts\activate  # En Windows
```

4. Instala as dependencias co xestor de paquetes uv:
```bash
uv pip install -r requirements.txt
```

## Configuración

1. Crea un arquivo `.env` na raíz do proxecto:
```bash
cp .env.example .env
```

2. Configura as variables de entorno no arquivo `.env`:
```
PORT=3002  # Porto para o servidor
```

## Uso

1. Inicia o servidor:
```bash
python main.py
```

2. Abre o navegador e accede a:
```
http://localhost:3002/qr_udc
```

3. Na interface web:
   - Introduce unha URL válida dos dominios udc.es ou udc.gal
   - (Opcional) Engade un título para o código QR
   - Selecciona o estilo do código QR (negro ou cor)
   - Selecciona o estilo do logo (negro ou cor)
   - Fai clic en "Xerar código QR"
   - Descarga o código QR xerado ou xera un novo

## Desenvolvemento

Para contribuír ao desenvolvemento:

1. Asegúrate de ter instaladas as dependencias de desenvolvemento:
```bash
uv pip install -r requirements-dev.txt  # Se existe
```

2. Executa os tests:
```bash
pytest
```

3. Comproba o estilo do código:
```bash
flake8
```

## Contribucións

As contribucións son benvidas! Por favor, sinte libre de:

1. Facer un fork do proxecto
2. Crear unha rama para a túa funcionalidade (`git checkout -b feature/NovaFuncionalidade`)
3. Facer commit dos teus cambios (`git commit -am 'Engadida nova funcionalidade'`)
4. Facer push á rama (`git push origin feature/NovaFuncionalidade`)
5. Crear un Pull Request

## Resolución de problemas

### Problemas comúns

1. **Erro de permisos ao crear o entorno virtual**:
   - Asegúrate de ter permisos de escritura no directorio
   - Proba executar os comandos con sudo (só en Linux/macOS)

2. **Erro ao acceder á aplicación**:
   - Verifica que o servidor está en execución
   - Comproba que o porto 3002 está dispoñible
   - Asegúrate de incluír `/qr_udc` na URL

## Licenza

Este proxecto está baixo a licenza MIT - consulta o arquivo [LICENSE](LICENSE) para máis detalles.

## Contacto

Para calquera consulta ou suxestión:
- Abre un issue no repositorio
- Envía un pull request con melloras
- Contacta co equipo de desenvolvemento a través dos issues de GitHub 