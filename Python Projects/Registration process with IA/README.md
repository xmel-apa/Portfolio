ESCOPO DO PROJETO

     Desenvolvimento de aplicação para cadastros autômatos utilizando IA para a verificação da integridade dos dados e orquestrador dos processos de inserção no Business Partner do ERP SAP S/4HANA.
  Declaração do Projeto: O projeto foi criado para atender uma demanda específica na rotina de compradores, o cadastro de fornecedores. Fora implementado uma automação nos registros antes feitos manualmente, seguindo o fluxo de recebimento de novo item acrescentado na pasta de formulários do sharepoint da empresa e envio dos dados do formulário para a rota HTTP cinectada à API em Python utilizando o Power Automate, em seguida, na API Python são executadas às chamadas a API do Assistente de IA que verifica a integridade e valida os dados, por fim, o script Python insere através da conexão à uma API Odata criada no SAP a inserção dos dados. Após a finalização do input dos dados, a API Python retorna uma mensagem de sucesso ou falha do processo, com tudo, a trigger finalizará notificando através de um email para as pastas "Processados" em caso de sucesso na execução ou na pasta de "Falhas" a caso de insucesso. 
  Em adendo, fora realizada a conexão com o ngrok, o qual viabilizou o serviço de um servidor local. 
  IMPORTANTE: Essa aplicação está sem atribuíção das políticas de segurança necessárias. Aconselho a incrementar de acordo com as necessidades.

  FERRAMENTAS e BIBLIOTECAS: flask, requests, anthropic, python-dotenv, BrasilAPI, API ViaCEP, ngrok, Power Automate, Claude IA.
  
  OBS: O projeto pode ser utilizado e modificado por qualquer pessoa interessada. 
  Ultima versão: 15 de Maio, 2026

by EU

PROJECT SCOPE

   Development of an application for automated registrations using AI to verify data integrity and orchestrate insertion processes in the SAP S/4HANA ERP Business Partner.
Project Statement: The project was created to meet a specific demand in the buyers' routine: supplier registration. Automation was implemented in the records previously done manually, following the flow of receiving a new item added to the company's SharePoint form folder and sending the form data to the HTTP route connected to the API in Python using Power Automate. Then, in the Python API, calls are executed to the AI ​​Assistant API that verifies the integrity and validates the data. Finally, the Python script inserts the data through a connection to an Odata API created in SAP. After the data input is complete, the Python API returns a success or failure message. The trigger will then notify via email to the "Processed" folder in case of successful execution or to the "Failures" folder in case of failure.
Additionally, a connection was made to ngrok, which enabled the service of a local server.
IMPORTANT: This application lacks the necessary security policies. I advise adding them according to your needs.

TOOLS and LIBRARIES: flask, requests, anthropic, python-dotenv, BrasilAPI, API ViaCEP, ngrok, Power Automate, Claude IA.

NOTE: The project can be used and modified by anyone interested.
Last version: May 15, 2026

By ME

# ------------------------------------------------------#
# Data de criação: 2026-05-11
# Autor: Pamela Almeida
# email: pamela.almeidasp@gmail.com
# GitHub: xmel-apa
# linkedin: pamela-almeida-7b6695320
# -------------------------------------------------------#
