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
    print(f"{linha['id']} - {linha['data']} - {linha['hora']}")
    
def alteracao():
  titulo("Alteração de Agendamento")

  if token == "":
    print("Erro... Você deve logar-se primeiro")
    return

  id = int(input("Código do Agendamento: "))
  data_marcada = input("Data..: ")
  horario = input("Horário: ")
  id_usuario = 1
  id_quadra = 1

  response = requests.put(f"http://localhost:3000/agendamentos/{id}", 
    json={"data_marcada": data_marcada, "horario": horario, "id_usuario": id_usuario, "id_quadra": id_quadra},
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
  titulo("Gráfico comparando Raças e Faixas Etárias")

  raca1 = input("1ª Raça: ")
  raca2 = input("2ª Raça: ")
  raca3 = input("3ª Raça: ")

  # (): significa que é uma tupla (característica: é imutável)
  faixas = ("Até 5 anos", "Entre 6 e 10 anos", "Acima de 10 anos")
  # {}: significa que é um dicionário (chave: valor)
  animais = {
      raca1: [0, 0, 0],
      raca2: [0, 0, 0],
      raca3: [0, 0, 0],
  }

  response = requests.get("http://localhost:3000/animais")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()

#  print(dados)

  for linha in dados:
    if linha['raca'] == raca1:
      if linha['idade'] <= 5:
        animais[raca1][0] += 1
      elif linha['idade'] <= 10:
        animais[raca1][1] += 1          
      else:
        animais[raca1][2] += 1   
    elif linha['raca'] == raca2:
      if linha['idade'] <= 5:
        animais[raca2][0] += 1
      elif linha['idade'] <= 10:
        animais[raca2][1] += 1          
      else:
        animais[raca2][2] += 1   
    elif linha['raca'] == raca3:
      if linha['idade'] <= 5:
        animais[raca3][0] += 1
      elif linha['idade'] <= 10:
        animais[raca3][1] += 1          
      else:
        animais[raca3][2] += 1   

  x = np.arange(len(faixas))  # the label locations
  width = 0.25  # the width of the bars
  multiplier = 0

  fig, ax = plt.subplots(layout='constrained')

  for attribute, measurement in animais.items():
      offset = width * multiplier
      rects = ax.bar(x + offset, measurement, width, label=attribute)
      ax.bar_label(rects, padding=3)
      multiplier += 1

  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Quantidades')
  ax.set_title('Gráfico Comparativo de Faixas Etárias')
  ax.set_xticks(x + width, faixas)
  ax.legend(loc='upper left', ncols=3)
  ax.set_ylim(0, 10)

  plt.show()

# ----------------------------------- Programa Principal
while True:
  if token: 
    titulo(f"Cadastro de Animais do Zoo - Usuário {usuarioNome}", "=")
  else:
    titulo("Cadastro de Animais do Zoo", "=")
  print("1. Fazer Login")
  print("2. Incluir Animais")
  print("3. Listar Animais")
  print("4. Alterar Dados")
  print("5. Excluir Animal")
  print("6. Agrupar por Habitat")
  print("7. Gráfico Relacionando Faixas Etárias")
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
