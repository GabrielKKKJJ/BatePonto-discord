import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from utils.DateOperations import DateTimeConverter
from config.db_config import ServerConfig
class DatabaseOperations:
    """
    Classe para realizar operações no banco de dados Firebase Firestore.
    """
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados Firestore.
        """
        self.db = ServerConfig().db

    async def register(self,server_name, register):
        """
        Registra um novo ponto no banco de dados.

        Args:
            register (dict): Dicionário contendo os dados do registro.
        """
        try:
            doc_ref = self.db.collection(server_name).document('Pontos').collection('registros').document()
            doc_ref.set(register)

            print("Document written with ID: ", doc_ref.id)

        except Exception as e:
            print("Error while registering:", e)

    async def relatorio(self, server_name: str):
        """
        Gera um relatório com os totais de tempo para cada usuário.

        Returns:
            list: Lista de dicionários contendo os totais de tempo para cada usuário.
        """
        try:
            user_totals = {}
            list_users = []
            date_converter = DateTimeConverter()
            
            docs = self.db.collection(server_name).document('Pontos').collection('registros').get() 
            for doc in docs:
                user_data = doc.to_dict()
                if 'User' in user_data and 'Hours' in user_data and 'Minutes' in user_data and 'Seconds' in user_data:
                    user = user_data['User']
                    hours = user_data['Hours']
                    minutes = user_data['Minutes']
                    seconds = user_data['Seconds']
                    
                    # Calcula o total de segundos
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    
                    # Se o usuário já existir nos totais, adicione os segundos, caso contrário, crie uma entrada
                    if user in user_totals:
                        user_totals[user] += total_seconds
                    else:
                        user_totals[user] = total_seconds

            # Imprime os totais para cada usuário 
            for user, total_seconds in user_totals.items():
                # Converte o total de segundos em horas, minutos e segundos
                total_hours, total_minutes, total_seconds = date_converter.convert_to_time(total_seconds)
                
                users_totals = {
                    "User": user,
                    "Hours": total_hours,
                    "Minutes": total_minutes,
                    "Seconds": total_seconds
                }

                list_users.append(users_totals)

            return list_users

        except Exception as e:
            print("Error while generating report:", e)

    async def cleardb(self, server_name: str):
        """
        Limpa todos os documentos da coleção 'Pontos'.
        """
        try:
            docs = self.db.collection(server_name).document('Pontos').collection('registros').get()
            for doc in docs:
                doc.reference.delete()
            
            print("Documents deleted successfully!")

        except Exception as e:
            print("Error while clearing the database:", e)
