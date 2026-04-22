import pyautogui
from time import sleep

#Acessar o sistema 
#acrescentar o login
#definição da extração 
#extrair os dados
#Fechar sistema
#abrir local do arquivo
# editar nome do arquivo

#Abrir o sistema
pyautogui.click(1309,125,2,duration=1)

#Abrir Diário de Bordo
pyautogui.click(1048,767,duration=7)
pyautogui.click(1048,767,duration=1)

#Configuração
pyautogui.click(973,647,duration=1)
pyautogui.click(1035,505,duration=1)
pyautogui.click(746,700,duration=1)

#Login
pyautogui.click(645,358,duration=1)
pyautogui.write('0')
pyautogui.click(606,412,duration=1)
pyautogui.write('2104')
pyautogui.click(636,449,duration=1)

#Seleção de período
pyautogui.click(670,395,duration=1)
pyautogui.click(692,657,duration=1)
pyautogui.click(840,393,duration=1)
pyautogui.click(871,659,duration=1)

#Extração dos dados
pyautogui.click(613,465,duration=1)
pyautogui.click(597,469,duration=1)
pyautogui.click(774,463,duration=1)
pyautogui.click(738,490,duration=3)
pyautogui.click(826,459,duration=20)

#Fechar sistema
pyautogui.click(772,471,duration=1)
pyautogui.click(895,751,duration=1)

#Abrir local do arquivo
#C:\Arquivos Transferência
pyautogui.click(895,751,duration=1)

#Ativa atalho do Windows
pyautogui.press('win')

#Ativa atalho do Windows
pyautogui.click(663,88,duration=1)
pyautogui.write('Explorador de Arquivos')
pyautogui.press('enter')
sleep(2)
pyautogui.click(845,63,duration=1)
pyautogui.write('C:\Arquivos Transferência')
pyautogui.press('enter')
sleep(2)

#exluir primeiro arquivo
pyautogui.click(792,173,duration=1)
pyautogui.press('delete')

#Editar nome do arquivo
pyautogui.click(792,173,duration=1)
pyautogui.click(792,173,duration=1)
pyautogui.write('Diário de Bordo')
pyautogui.press('enter')
sleep(2)

#Finalizar
pyautogui.click(1345,9,duration=1)
pyautogui.press('win')
pyautogui.click(678,86,duration=1)
pyautogui.write('Paradas de Manutenção')
pyautogui.press('enter')
pyautogui.click(475,89,duration=1)
pyautogui.click(198,98,duration=1)

pyautogui.alert('Processo finalizado!')