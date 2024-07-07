import matplotlib.pyplot as plt
import numpy as np
import requests

token = ""
usuarioNome = ""

def titulo(texto, sublinhado="-"):
  print()
  print(texto)
  print(sublinhado*40)

def login():
  titulo("Login do Usuário")

  email = input("E-mail: ")
  senha = input("Senha.: ")

  response = requests.post("http://localhost:3000/login", 
    json={"email": email, "senha": senha}
  )
  

  if response.status_code != 200:
    print("Erro... Login ou Senha inválidos")
    return
  
  dados = response.json()

  global token 
  global userNome
  token = dados['token']
  usuarioNome = dados['nome']
  print(f"Bem-vindo ao sistema: {usuarioNome}")

def inclusao():
  titulo("Fazer Agendamento")

  if token == "":
    print("Erro... Você deve logar-se primeiro")
    return
  
  print()

  data_marcada = input("Data..: ")
  horario = input("Horário: ")
  id_quadra = int(input("Código da Quadra: "))

  response = requests.post("http://localhost:3000/agendamentos", 
    json={"data": data_marcada, "hora": horario, "quadra_id": id_quadra},
    headers={"Authorization": f"Bearer {token}"}
  )
  
  print(response.status_code)

  if response.status_code == 201:
    dados = response.json()
    print(f"Ok... Agendamento cadastrado com o código {dados['id']}")
  else:
    print("erro" + data_marcada, horario, id_quadra)
    
def listagem():
  titulo("Listagem de Agendamentos")

  response = requests.get("http://localhost:3000/agendamentos")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()

  for linha in dados:
    print(f"Código: {linha['id']} - Data de Reserva: {linha['data']} - Horário: {linha['hora']}")
    
def alteracao():
  titulo("Alteração de Agendamento")

  if token == "":
    print("Erro... Você deve logar-se primeiro")
    return

  id = int(input("Código do Agendamento: "))
  data_marcada = input("Data..: ")
  horario = input("Horário: ")
  id_quadra = 1

  response = requests.put(f"http://localhost:3000/agendamentos/{id}", 
    json={"data": data_marcada, "hora": horario, "quadra_id": id_quadra},
    headers={"Authorization": f"Bearer {token}"}
  )

  if response.status_code == 200:
    print("Ok... Agendamento alterado")
  else:
    print("Erro... Agendamento não encontrado")
    
def exclusao():
  titulo("Exclusão de Esporte")

  if token == "":
    print("Erro... Você deve logar-se primeiro")
    return

  id = int(input("Código do Agendamento: "))

  response = requests.delete(f"http://localhost:3000/agendamentos/{id}", 
    headers={"Authorization": f"Bearer {token}"}
  )

  if response.status_code == 200:
    print("Agendamento excluído")
  else:
    print("Agendamento Excluido |  obs: Soft Delete")

def agrupar():
  titulo("Agrupar por Quadra")

  response = requests.get("http://localhost:3000/agendamentos")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()

  contador_quadra1 = 0
  contador_quadra2 = 0
  contador_quadra3 = 0
  contador_quadra4 = 0
  
  for linha in dados:
    if linha['quadra_id'] == 1:
        contador_quadra1 += 1         
    elif linha['quadra_id'] == 2:
        contador_quadra2 += 1   
    elif linha['quadra_id'] == 3:
        contador_quadra3 += 1
    elif linha['quadra_id'] == 4:
        contador_quadra4 += 1

  print(f"Quadra 1: {contador_quadra1} agendamentos")
  print(f"Quadra 2: {contador_quadra2} agendamentos")
  print(f"Quadra 3: {contador_quadra3} agendamentos")
  print(f"Quadra 4: {contador_quadra4} agendamentos")

def grafico():
  titulo("Gráfico de Quadras")
    
  response = requests.get("http://localhost:3000/quadras")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()
  
  contador_volei = 0
  contador_futebol = 0
  contador_basquete = 0
  contador_handebol = 0
  
  for linha in dados:
    if linha['esporte_id'] == 1:
        contador_volei += 1         
    elif linha['esporte_id'] == 2:
        contador_futebol += 1   
    elif linha['esporte_id'] == 3:
        contador_basquete += 1
    elif linha['esporte_id'] == 4:
        contador_handebol += 1

  fig, ax = plt.subplots()

  Jogos = ["Volei", "Futebol", "Basquete", "Handebol"]
  counts = [contador_volei, contador_futebol, contador_basquete, contador_handebol]
  bar_labels = ['red', 'blue', 'green', 'orange']
  bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']

  ax.bar(Jogos, counts, label=bar_labels, color=bar_colors)

  ax.set_ylabel('Numero de Jogos')
  ax.set_title('Esporte Por Quadra')
  ax.legend(title='Quadra')

  plt.show()

# ----------------------------------- Programa Principal
while True:
  if token: 
    titulo(f"Agendamento de quadras - Usuário {usuarioNome}", "=")
  else:
    titulo("Agendamento de quadras", "=")
  print("1. Fazer Login")
  print("2. Incluir agendamento")
  print("3. Listar agendamentos")
  print("4. Alterar Dados")
  print("5. Excluir agendamento")
  print("6. agrupar por quadra")
  print("7. Gráfico")
  print("8. Finalizar")
  opcao = int(input("Opção: "))
  if opcao == 1:
    login()
  elif opcao == 2:
    inclusao()
  elif opcao == 3:
    listagem()
  elif opcao == 4:
    alteracao()
  elif opcao == 5:
    exclusao()
  elif opcao == 6:
    agrupar()
  elif opcao == 7:
    grafico()
  else:
    break
