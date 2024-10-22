import os
import smtplib
from email.mime.multipart import MIMEMultipart # Multipurpose Internet Mail Extensions
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv

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