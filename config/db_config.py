import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from Firebase.firebase_init import init_firebase

class ServerConfig:
    def __init__(self):
        self.db = init_firebase()

    async def initialize_config(self, server_name: str):
        """
        executed by /config
        Create the folder from the server name if it doesn't exist
        Initialize config.json if it doesn't exist
        """
        try:
            # Create the folder from the server name if it doesn't exist
            if not os.path.exists(f'config/Servers_configs/{server_name}'):
                os.makedirs(f'config/Servers_configs/{server_name}')

                # Initialize config.json if it doesn't exist
                await self.default_config(server_name=server_name)

            # Initialize config.json if it doesn't exist
            elif not os.path.exists(f'config/Servers_configs/{server_name}/config.json'):
                await self.default_config(server_name=server_name)

            # If config.json exists in local but not at DB
            elif os.path.exists(f'config/Servers_configs/{server_name}/config.json'):
                if not self.db.collection(server_name).document(document_id='config').get().exists:
                    local_config = await read_json(f'config/Servers_configs/{server_name}/config.json')
                    self.db.collection(server_name).document(document_id='config').set(local_config)
                
        except Exception as e:
            print("Error while initializing config:", e)
    async def default_config(self, server_name: str):
        try:
            # Initialize config.json if it doesn't exist
            if not os.path.exists(f'config/Servers_configs/{server_name}/config.json'):
                os.makedirs(f'config/Servers_configs/{server_name}', exist_ok=True)
                with open(f'config/Servers_configs/{server_name}/config.json', 'w') as f:
                    pass
            
            # Initialize the DATA in config.json if equal to None
            if await read_json(f'config/Servers_configs/{server_name}/config.json') is None:

                # Check if the document exists in DB
                # if it does, read the document from DB and write it to config.json
                # if not, create it with default values
                if self.db.collection(server_name).document(document_id='config').get().exists:
                    print("Document exists")
                    config = self.db.collection(server_name).document(document_id='config').get().to_dict()

                    await write_json(f'config/Servers_configs/{server_name}/config.json', config)
                else:
                    print("Document does not exist")
                    config = {
                        "channels": {
                            "alert": None,
                            "ponto": None
                        },
                        "permissions": {}
                    }

                    doc_ref = self.db.collection(server_name).document(document_id='config')
                    doc_ref.set(config)

                    await write_json(f'config/Servers_configs/{server_name}/config.json', config)
    
        except Exception as e:
            print("Error while getting config:", e)

    async def update_config(self,server_name: str, field: str, config: dict):
        try:
            doc_ref = self.db.collection(server_name).document(document_id='config')
            doc_ref.update(config)

            configjson = await read_json(f'config/Servers_configs/{server_name}/config.json')

            if field == 'channels.alert':
                value = config['channels.alert']
                configjson['channels']['alert'] = value

            elif field == 'channels.ponto':
                value = config['channels.ponto']
                configjson['channels']['ponto'] = value

            elif field == 'permissions':
                value = config['permissions']
                configjson['permissions'] = value

            # atualize o campo no documento
            await write_json(f'config/Servers_configs/{server_name}/config.json', configjson)

            print("Document written with ID: ", doc_ref.id)

        except Exception as e:
            print("Error while setting config:", e)


async def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

async def read_json(path):
    with open(path, 'r') as json_file:
        file_content = json_file.read()
        
        # Verifica se o arquivo está vazio
        if not file_content.strip():
            return None
        else:
            # Tenta decodificar o conteúdo JSON
            data = json.loads(file_content)
            return data


