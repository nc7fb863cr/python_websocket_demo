import asyncio
import ssl
import pathlib
import websockets


connected = set()


async def server(websocket, path):
    # Register
    connected.add(websocket)
    
    try:
        async for message in websocket:
            print(message)
            for conn in connected:
                await conn.send(message)
    finally:
        # Unregister
        connected.remove(websocket)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(pathlib.Path(
    __file__).with_name('cert.pem'), keyfile=pathlib.Path(
    __file__).with_name("key.pem"))
start_server = websockets.serve(server, "192.168.0.3", 6000, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
print('Server is running ...')
asyncio.get_event_loop().run_forever()
