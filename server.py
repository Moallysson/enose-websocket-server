from websocket_server import WebsocketServer
import MySQLdb

valor = 0

con = MySQLdb.connect("localhost", "root", "", "websocket")

# Função chamada quando um novo cliente se conecta
def new_client(client, server):
    print(f"Cliente {client['id']} conectado")

# Função chamada quando uma mensagem é recebida
def message_received(client, server, message):
    valor = int(message)
    print("Valor sensor: "+str(valor))

    try:
        cursor = con.cursor()  # Inicia um cursor do banco de dados
        cursor.execute("INSERT INTO sensor VALUES(%s)", (valor,))  # Comando para inserir valores no banco
        con.commit()  # Executa o comando do banco de dados
    except MySQLdb.IntegrityError:
        print("Falha ao inserir valores no banco de dados.")
    finally:
        cursor.close()
    
    server.send_message(client, "Mensagem recebida com sucesso")

# Criação do servidor WebSocket
server = WebsocketServer(host='192.168.1.109', port=8765)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)

print("Servidor WebSocket iniciado...")



server.run_forever()
