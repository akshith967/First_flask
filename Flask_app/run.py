from f.mq import *
from f import create_app
from f.models import db, Audits

app = create_app()
client = receive_client()
def on_message(client, userdata, message):
    try:
        with app.app_context():
            new_audit = Audits(msg=message.payload.decode())
            db.session.add(new_audit)
            db.session.commit()
        print(f"Received message: {message.payload.decode()}")
    except Exception as e: 
        print(e)

client.on_message = on_message

if __name__ == '__main__':
    app.run(port=8000)
    
  
