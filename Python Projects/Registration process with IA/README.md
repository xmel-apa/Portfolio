ESCOPO DO PROJETO

     Desenvolvimento de aplicação para cadastros automatos utilizando IA para a verificação da integridade dos dados e orquestrador dos processos de inserção no ERP SAP HANNA.
  Declaração do Projeto: O projeto foi criado para atender uma demanda específica na rotina de compradores, o cadastro de fornecedores. Fora implementado uma automação nos registros antes feitos manualmente, seguindo o fluxo de recebimento do sharepoint por email e envio dos dados do formulário para a rota HTTP da API em Python utilizando o Power Automate, em seguida, na API Python são executadas às chamadas a API do Assistente de IA que verifica a integridade e valida os dados, e por fim, o script Python insere através de um SAPScript a inserção dos dados. Após a finalização do input dos dados, o Assistente de IA retorna uma mensagem de sucesso ou falha do processo, com tudo, a trigger finalizará movendo aquele email para as pastas "Processados" em caso de sucesso na execução ou na pasta de "Falhas" a caso de unsucesso. 
  Ferramentas: NewsAPI, requests, tkinter, webbrowser, threading, copilot, Hugging Face Transformers, phpaiola/ptt5-base-summ-xlsum, torch, sentencepiece/protobuf.
  
  OBS: O projeto pode ser utilizado e modificado por qualquer pessoa interessada. 
  Ultima versão: 27 de Abril, 2026


PROJECT SCOPE

     A News summarizer application developed with filters for especific segmentations through the implementation of Machine Learning.
  Project Statement: This project was created to address a specific need in the routine of buyers: supplier registration. Automation was implemented for the registrations previously done by them, following a flow of receiving data from SharePoint via email and sending the form data to http route of Python API using Power Automate. Then, the Python API executes calls to the AI Assistent API, wich verifies the integraty and validates the data. Finally, the Python script inserts the data via SAPScript. After the data input is complete, the AI Assistent returns a success or failure messege. The trigger then moves the email to the "Processed" folder if successful, or ti the "Failed" folder if unsuccessful.
  Tools: NewsAPI, requests, tkinter, webbrowser, threading, copilot, Hugging Face Transformers, phpaiola/ptt5-base-summ-xlsum, torch, sentencepiece/protobuf.

  Note: The project can be used and modified by anyone interested.

  Last version: April 27, 2026
