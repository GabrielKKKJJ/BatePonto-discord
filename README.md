## Como usar o Ponto bot

**Clone o repositório:**

1. Clique no botão verde "Clone or download".
2. Escolha "Copy HTTPS" para copiar o link do repositório.
3. Abra um terminal ou prompt de comando no seu computador.
4. Navegue até a pasta onde você deseja clonar o repositório.
5. Execute o seguinte comando:

```
https://github.com/GabrielKKKJJ/Ponto-discord-Bot.git
```

**Adapte o código para o seu uso:**

1. Abra o arquivo `Main.py` no seu editor de texto favorito.
2. Onde tem:
```
await bot.start("TOKEN")  # Replace with your bot token
```
5. Altere para o token do seu bot.
   
**Metodo com relatorios**
1. Caso queira usar o /relatorio crie uma banco de dados no firebase
```
TUTORIAL
https://www.youtube.com/watch?v=TW02hwhBvo4
```
2. Na hora de criar o documento coloque o nome como Pontos
3. Apos a criação do banco de dados va na seguinte opção

![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/850266cc-22d1-42c2-aabf-8196978061da)

5. Clique em:

![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/524bf876-461c-4c8b-9aa8-9d47edaa2cb3)

7. E depois em:
   
![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/dc27898d-fe45-4fad-a28a-024c27d752f2)

9. Apos o download do JSON, coloque ele na pasta firebase do repositorio e já podera usa-lo

**Metodo sem relatorios**
1. Comente as seguintes linhas:
2. Aquivo -> Ponto.py
3. Linhas 6, 45, 47, 109-118, 120-127
4. Apague a pasta -> Firebase

**Cargos com permissão para o comando**
1. Para alterar os cargos com permissão para executar os comandos va em
2. Arquivo -> Ponto.py
3. Na linha 9 em allowed_rules
4. Remova todos os ids dentro dele e adicione o id dos cargos do seu servidor que terão permissão

**Comandos disponíveis:**

* `/ponto`: Inicia o ponto de um usuario.
* `/relatorio`: Faz um relatorio do tempo dos usuarios.
* `/cleardb`: Limpa o banco de dados.

**Preview**

![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/7e99876d-ea4e-4f16-8c3e-fb75f1353f0f)
![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/1b2f74d2-6e2c-4f76-b260-7f060db468a9)
![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/97bfeeee-865b-4edd-a252-6b04155db73b)
![image](https://github.com/GabrielKKKJJ/Ponto-discord-Bot/assets/123528138/f0cf6278-b26b-4eb8-a43b-a1ce7f0da788)


**Exemplo de uso:**
Digite:
```
python3 Main.py
```

**Observações:**

* Este repositório é um exemplo de como usar a API do Discord.
* Você pode adaptar o código para criar o seu próprio bot com as funcionalidades que desejar.
* Se você tiver alguma dúvida, sinta-se à vontade para abrir uma issue no repositório.

**Links úteis:**

* Documentação da API do Discord: [https://discord.com/developers/docs/intro](https://discord.com/developers/docs/intro)
* Tutoriais sobre como criar bots do Discord: [Tutorial](https://www.youtube.com/watch?v=4-aVu1_w18Y&list=PL9-YiBpH1Ne7NJlG9wGsEee24koLc8JTT)

**Contribuições:**

* Se você quiser contribuir para este repositório, sinta-se à vontade para enviar um pull request.
* Todas as contribuições são bem-vindas!

