import os
import smtplib
from email.mime.multipart import MIMEMultipart # Multipurpose Internet Mail Extensions
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 

#Cargar variables de entorno
load_dotenv()

app = Flask(__name__) #Incializar aplicación de Flask

#Función para enviar los correos electrónicos
def send_email(subject, recipient, body_html):
    email_sender = os.getenv('GoogleMail__EmailSender')
    email_password = os.getenv('GoogleMail__ApiKey')
    smtp_server = os.getenv('GoogleMail__Host')
    smtp_port = os.getenv('GoogleMail__Port')

    print(f"Email sender: {email_sender}")
    print(f"Email password: {email_password}")
    print(f"SMTP server: {smtp_server}")
    print(f"SMTP port: {smtp_port}")

    #Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje en formato HTML
    msg.attach(MIMEText(body_html, 'html'))

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server: #Concetarse al servidor
            server.starttls() # Asegura la conexión
            server.login(email_sender, email_password)
            server. sendmail(email_sender, recipient, msg.as_string())


        return True
    except Exception as e:
        return False, str(e)
    
# Endpoint para enviar el correo

@app.route('/send-email', methods=["POST"])
def send_email_endpoint():
    data = request.json
    subject = data.get('subject')
    recipient = data.get('recipient')
    content= data.get('content')

    body_html= generate_template(subject, content)

    success = send_email(subject, recipient, body_html)
    print(f"Success: {success}")
    if success:
        print('Email sent succesfully!')
        return jsonify({'message': 'Email sent succesfully'})
    else:
        print('Failed to send email')
        return jsonify({'message': 'Failed to sent email'})
    
    #EndPoint para listar users

@app.route('/get-users', methods=['GET'])
def get_users():
        return jsonify([
        {'name': 'John Doe', 'email': 'name@example.com'},
        {'name': 'John Doe', 'email': 'name@example.com'}
    ])
    
def generate_template(subject, content):
    # Define la estructura básica del HTML con estilos

    if(subject == "Nueva contraseña"):
        return (f"""
            <html>
            <head>
                <title>Contenido en Negrita</title>
            </head>
            <body>
                <div style='font-family: Arial, sans-serif; background-color: #f6f6f6; margin: 0; padding: 20px;'> 
                <div style='max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);'> 
                <h1 style='color: #333;'>¡Nueva Contraseña!</h1> 
                <p>Tu Contraseña es la siguiente:</p> 
                <div style='background-color: #e7f3fe; border: 1px solid #a6c8ff; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 16px; color: #1a73e8;'>
                    {content}
                </div> 
                <p>Por favor, guarda este contraseña en un lugar seguro y no lo compartas con nadie 🤫</p> 
                <div style='margin-top: 20px; font-size: 12px; color: #999;'> 
                <p>Gracias por utilizar nuestros servicios.</p> </div> </div> </div>
            </body>
            </html>
            """ )
    
    elif(subject == "Codigo autenticacion"):
        return (f"""
            <html>
            <head>
                <title>Codigo de autenticacion</title>
            </head>
            <body>
                <div style='font-family: Arial, sans-serif; background-color: #f6f6f6; margin: 0; padding: 20px;'> 
                    <div style='max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);'> 
                        <h1 style='color: #333;'>¡Codigo de autenticacion!</h1> 
                        <p>Tu Codigo de autenticacion es el siguiente:</p> 
                        <div style='background-color: #e7f3fe; border: 1px solid #a6c8ff; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 16px; color: #1a73e8;'>
                            {content}
                        </div> 
                        <p>Este código es de uso único, así que asegúrate de utilizarlo antes de que expire. No lo dejes pasar. ⚠️</p> 
                        <div style='margin-top: 20px; font-size: 12px; color: #999;'> 
                            <p>Gracias por utilizar nuestros servicios.</p> 
                        </div> 
                    </div> 
                </div>
            </body>
            </html>
            """ )
    elif(subject == "Factura"):
        
        fecha = datetime.datetime.strptime(content["fecha"], '%Y-%m-%d %H:%M:%S')
        dia_y_fecha = fecha.strftime('%A %d de %B del %Y')
        hora = fecha.hour
        minutos = fecha.minute
        if hora >= 12:
            am_pm = 'p.m.'
        else:
            am_pm = 'a.m.'
        hora_12 = hora % 12
        if hora_12 == 0:  # Para que 0 sea 12
            hora_12 = 12

        # Formatear la hora
        hora_formateada = f"{hora_12}:{minutos:02d} {am_pm}"

        return (f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Factura</title>
            </head>
            <body style="font-family: 'Arial', sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; color: #333;">

                <div style="width: 600px; margin: 30px auto; background-color: #fff; padding: 30px; border: 2px solid #007ACC; border-radius: 10px;">
                    <!-- Encabezado -->
                    <div style="text-align: center; padding-bottom: 20px; border-bottom: 2px solid #007ACC;">
                        <h1 style="font-size: 28px; margin: 0; color: #007ACC;">Factura de Compra</h1>
                        <p style="font-size: 14px; color: #666;">Número de Factura: {content["factura"]}</p>
                        <p style="font-size: 14px; color: #666;">Fecha de Emisión: {dia_y_fecha} {hora_formateada}</p>
                    </div>

                    <!-- Información del vendedor y comprador -->
                    <div style="padding: 20px 0; display: flex; justify-content: space-between;">
                        <div style="width: 45%;">
                            <h2 style="font-size: 18px; margin-bottom: 10px; color: #333;">Vendedor:</h2>
                            <p style="font-size: 14px; margin: 0; color: #555;">Acarreos Manizales</p>
                            <p style="font-size: 14px; margin: 0; color: #555;">Av. Comercial 789</p>
                            <p style="font-size: 14px; margin: 0; color: #555;">Manizales, Colombia</p>
                            <p style="font-size: 14px; margin: 0; color: #555;">Email: AcarreosManizales@gmail.com</p>
                        </div>
                        <div style="width: 45%;">
                            <h2 style="font-size: 18px; margin-bottom: 10px; color: #333;">Comprador:</h2>
                            <p style="font-size: 14px; margin: 0; color: #555;">{content["nombres"]} {content["apellidos"]}</p>
                            <p style="font-size: 14px; margin: 0; color: #555;">Direccion: {content["direccion"]}</p>
                            <p style="font-size: 14px; margin: 0; color: #555;">CC: {content["documento"]}</p>
                            <p style="font-size: 14px; margin: 0; color: #555;">Email: {content["email"]}</p>
                        </div>
                    </div>

                    <!-- Detalles del artículo -->
                    <div style="padding: 20px 0; border-bottom: 2px solid #007ACC;">
                        <h2 style="font-size: 20px; color: #007ACC;">Detalles del Producto</h2>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <div style="width: 60%;">
                                <p style="font-size: 16px; color: #333; margin: 0;"><strong>Producto:</strong> Servicio acarreo</p>
                                <p style="font-size: 14px; color: #555; margin: 5px 0;">Descripción: {content["descripcion"]}</p>
                            </div>
                            <div style="width: 30%; text-align: right;">
                                <p style="font-size: 16px; color: #333; margin: 0;"><strong>Precio:</strong></p>
                                <p style="font-size: 24px; color: #007ACC; margin: 5px 0;"><strong>${content["baseiva"]}</strong></p>
                            </div>
                        </div>
                    </div>

                    <!-- Resumen del precio -->
                    <div style="padding: 20px 0; text-align: right;">
                        <p style="font-size: 16px; color: #555; margin: 5px 0;">Subtotal: ${content["baseiva"]}</p>
                        <p style="font-size: 16px; color: #555; margin: 5px 0;">Impuestos (IVA): ${content["iva"]}</p>
                        <p style="font-size: 20px; color: #007ACC; margin: 10px 0;"><strong>Total a Pagar: ${content["valorneto"]}</strong></p>
                    </div>

                    <!-- Información adicional -->
                    <div style="padding-top: 20px; text-align: center; font-size: 14px; color: #777;">
                        <p>Gracias por su compra. Si tiene alguna pregunta, contáctenos en <a href="mailto:ventas@xyz.com" style="color: #007ACC; text-decoration: none;">AcarreosManizales@xyz.com</a></p>
                    </div>
                </div>

            </body>
            </html>

            """ )

    return f"""
        <html>
        <head>
            <title>Contenido en Negrita</title>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

# Supongamos que obtienes el contenido de alguna fuente

if __name__ == "__main__":
    app.run(debug=True)

#Prueba de colaborador