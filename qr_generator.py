from PIL import Image, ImageDraw, ImageFont
import qrcode
import io
import os

def hex_to_rgb(hex_color: str) -> tuple:
    """Convierte un color hexadecimal a RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def añadir_padding_logo(logo: Image.Image, padding: int, color_fondo: tuple) -> Image.Image:
    """Añade un padding alrededor del logo con el color de fondo especificado."""
    # Crear una nueva imagen con el padding
    new_size = (logo.size[0] + 2 * padding, logo.size[1] + 2 * padding)
    padded_logo = Image.new('RGBA', new_size, (*color_fondo, 255))
    
    # Pegar el logo original en el centro
    position = (padding, padding)
    padded_logo.paste(logo, position, mask=logo.split()[3])
    
    return padded_logo

def añadir_titulo(imagen: Image.Image, titulo: str, color_rgb: tuple) -> Image.Image:
    """Añade un título a la imagen."""
    if not titulo:
        return imagen

    # Crear una nueva imagen con espacio para el título
    padding_titulo = 60  # Aumentado para dar más espacio al título
    nueva_altura = imagen.height + padding_titulo
    nueva_imagen = Image.new('RGB', (imagen.width, nueva_altura), 'white')
    
    # Pegar la imagen original
    nueva_imagen.paste(imagen, (0, padding_titulo))
    
    # Añadir el título
    draw = ImageDraw.Draw(nueva_imagen)
    
    # Usar Roboto Bold incluida en el proyecto
    try:
        font_path = "fonts/Roboto-Bold.ttf"
        font = ImageFont.truetype(font_path, 32)
    except Exception as e:
        print(f"Error al cargar la fuente: {e}")
        font = ImageFont.load_default()

    # Centrar el texto
    bbox = draw.textbbox((0, 0), titulo, font=font)
    text_width = bbox[2] - bbox[0]
    x = (imagen.width - text_width) // 2
    y = 15  # Padding superior para el título
    
    # Dibujar el texto
    draw.text((x, y), titulo, fill=color_rgb, font=font)
    
    return nueva_imagen

def generar_qr_con_logo(
    texto: str,
    estilo: str = "blanco_negro",  # "blanco_negro" o "corporativo"
    logo_color: bool = True,  # True para logo a color, False para blanco y negro
    titulo: str = ""
) -> bytes:
    # Definir colores según el estilo
    if estilo == "blanco_negro":
        color_qr_rgb = (0, 0, 0)  # Negro
        color_fondo_rgb = (255, 255, 255)  # Blanco
    else:  # corporativo
        color_qr_rgb = (214, 14, 140)  # Rosa corporativo UDC
        color_fondo_rgb = (255, 255, 255)  # Blanco

    # Crear el objeto QR con mayor tamaño y corrección de errores alta
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)

    # Crear una imagen QR básica
    img_qr = qr.make_image(fill_color=color_qr_rgb, back_color=color_fondo_rgb)
    img_qr = img_qr.convert("RGB")

    # Preparar el logo según la preferencia
    logo_path = "static/logo_udc_color.png" if logo_color else "static/logo_udc.png"
    logo = Image.open(logo_path).convert("RGBA")
    
    # Calcular el tamaño máximo recomendado para el logo (25% del QR)
    qr_width = img_qr.size[0]
    logo_max_size = int(qr_width * 0.25)
    
    # Redimensionar el logo manteniendo la proporción
    logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    
    # Añadir padding blanco alrededor del logo (10% del tamaño del logo)
    padding = int(logo.size[0] * 0.1)
    logo_con_padding = añadir_padding_logo(logo, padding, color_fondo_rgb)

    # Calcular la posición central para el logo con padding
    pos = (
        (img_qr.size[0] - logo_con_padding.size[0]) // 2,
        (img_qr.size[1] - logo_con_padding.size[1]) // 2
    )

    # Pegar el logo con padding
    img_qr.paste(logo_con_padding, pos, mask=logo_con_padding.split()[3])

    # Añadir título si existe
    if titulo:
        img_qr = añadir_titulo(img_qr, titulo, color_qr_rgb)

    # Guardar en buffer
    buffer = io.BytesIO()
    img_qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
