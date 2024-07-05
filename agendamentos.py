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
  id_quadra = 1

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
  titulo("Exclusão de Agendamento")

  if token == "":
    print("Erro... Você deve logar-se primeiro")
    return

  id = int(input("Código do Agendamento: "))

  response = requests.delete(f"http://localhost:3000/agendamentos/{id}", 
    headers={"Authorization": f"Bearer {token}"}
  )

  if response.status_code == 200:
    print("Ok... Agendamento excluído")
  else:
    print("Erro... Agendamento não encontrado")

def grafico():
  titulo("Gráfico de Quadras")

  esporte1 = input("1ª Esporte: ")
  esporte2 = input("2ª Esporte: ")
  
  if esporte1 == "volei":
    esporte1 = 1
  if esporte2 == "futebol":
    esporte2 = 2

  # (): significa que é uma tupla (característica: é imutável)
  faixas = ("Volei", "Futebol", "Teste")
  # {}: significa que é um dicionário (chave: valor)
  esportes = {
      esporte1: [0],
      esporte2: [0]
  }

  response = requests.get("http://localhost:3000/quadras")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()

#  print(dados)

  for linha in dados:
    if linha['esporte_id'] == esporte1:
        esportes[esporte1][0] += 1         
    elif linha['esporte_id'] == esporte2:
        esportes[esporte2][0] += 1     

  x = np.arange(len(faixas))  # the label locations
  width = 0.25  # the width of the bars
  multiplier = 0

  fig, ax = plt.subplots(layout='constrained')

  for attribute, measurement in esportes.items():
      offset = width * multiplier
      rects = ax.bar(x + offset, measurement, width, label=attribute)
      ax.bar_label(rects, padding=3)
      multiplier += 1

  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Quantidades')
  ax.set_title('Gráfico Comparativo de Esportes por Quadras')
  ax.set_xticks(x + width, faixas)
  ax.legend(loc='upper left', ncols=3)
  ax.set_ylim(0, 10)

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
  elif opcao == 7:
    grafico()
  else:
    break
