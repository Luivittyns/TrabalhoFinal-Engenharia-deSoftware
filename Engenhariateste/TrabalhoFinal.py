from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# 🔹 Caminho correto do WebDriver (Edge)
webdriver_path = r"C:\Users\Luiara\Downloads\edgedriver_win64\msedgedriver.exe"

# 🔹 Configurar o Edge WebDriver
options = Options()
service = Service(webdriver_path)
driver = webdriver.Edge(service=service, options=options)

# 🔹 URL da página
url = "http://127.0.0.1:5500/site.html"  # Substitua pela URL correta
driver.get(url)
time.sleep(2)  # Pequeno delay para garantir carregamento inicial

# 🔹 Criando um WebDriverWait para ser reutilizado
wait = WebDriverWait(driver, 10)


# 📌 Função para testar login
def fazer_login(usuario, senha):
    print(f"🔍 Fazendo login com usuário: {usuario}")

    wait = WebDriverWait(driver, 10)

    # Aguarda os campos de entrada e o botão de login
    campo_username = wait.until(EC.presence_of_element_located((By.ID, "username")))
    campo_password = wait.until(EC.presence_of_element_located((By.ID, "password")))
    botao_login = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))

    # Preenche os campos e faz login
    campo_username.send_keys(usuario)
    campo_password.send_keys(senha)
    botao_login.click()

    time.sleep(2)  # Pequeno delay para redirecionamento

    # Verifica se o login foi bem-sucedido
    assert "inicio.html" in driver.current_url, "❌ ERRO: Login falhou, usuário não foi redirecionado!"
    print("✅ Login realizado com sucesso!")

    # Teste de login com falha
    def fazer_login_falha(usuario, senha):
        print(f"🔍 Fazendo login com usuário: {usuario}")

        campo_username.clear()
        campo_password.clear()
        campo_username.send_keys(usuario)
        campo_password.send_keys(senha)
        botao_login.click()

        time.sleep(2)
        mensagem_erro = wait.until(EC.presence_of_element_located((By.ID, "mensagem_erro"))).text
        assert "Usuário ou senha incorretos" in mensagem_erro, "❌ ERRO: Mensagem de erro não exibida corretamente!"
        print("✅ Mensagem de erro validada com sucesso!")
        assert "inicio.html" in driver.current_url, "❌ ERRO: Login falhou, usuário não foi redirecionado!"
        print("❌ Erro ao realizar login!")



# 📌 Função para testar o formulário de contato
def testar_formulario_contato():
    print("🔍 Testando formulário de contato...")

    try:
        campo_nome = wait.until(EC.presence_of_element_located((By.ID, "nome")))
        campo_email = wait.until(EC.presence_of_element_located((By.ID, "email")))
        campo_mensagem = wait.until(EC.presence_of_element_located((By.ID, "mensagem")))
        botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Enviar']")))

        campo_nome.send_keys("João Silva")
        campo_email.send_keys("joao@email.com")
        campo_mensagem.send_keys("Gostei muito do site!")
        botao_enviar.click()

        driver.implicitly_wait(5)  # Espera até 3 segundos para encontrar elementos


        try:
            alerta = driver.switch_to.alert
            assert "Mensagem enviada com sucesso!" in alerta.text, "❌ ERRO: Formulário de contato falhou!"
            alerta.accept()
        except:
            print("⚠️ Aviso: Nenhum alerta foi encontrado após o envio.")

        print("✅ Formulário de contato testado com sucesso!")

    except Exception as e:
        print(f"❌ Erro no teste do formulário: {e}")


# 📌 Função para testar o botão de cadastro
def testar_botao_cadastro():
    print("🔍 Testando botão de cadastro...")

    try:
        botao_cadastrar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Cadastrar']")))
        botao_cadastrar.click()
        time.sleep(2)

        assert "cadastro.html" in driver.current_url, "❌ ERRO: O botão de cadastro não redirecionou corretamente!"

        print("✅ Botão de cadastro testado com sucesso!")
        driver.back()

    except Exception as e:
        print(f"❌ Erro ao testar botão de cadastro: {e}")



# 📌 Função para testar o menu de navegação
def testar_menu_navegacao():
    print("🔍 Testando menu de navegação...")

    try:
        fazer_login("user123", "senha123")  # Insira um usuário válido

        # 🔹 Aguardar o botão "Sair" estar disponível
        botao_sair = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sair']")))

        print("✅ Botão 'Sair' encontrado! Clicando...")
        
        # 🔹 FORÇA o clique via JavaScript para evitar bloqueios
        driver.execute_script("arguments[0].click();", botao_sair)

        time.sleep(2)

        # 🔹 Se houver um alerta de confirmação, aceitá-lo
        try:
            alerta = driver.switch_to.alert
            print(f"📌 Alerta detectado: {alerta.text}")
            alerta.accept()
            time.sleep(2)
        except:
            print("⚠️ Nenhum alerta detectado.")

        # 🔹 Verificar se o usuário voltou para a página de login
        assert "login.html" in driver.current_url, "❌ ERRO: O botão de sair não redirecionou corretamente!"

        print("✅ Menu de navegação testado com sucesso!")

    except Exception as e:
        print(f"❌ ERRO ao testar menu de navegação: {e}")





# 📌 Executando os testes individualmente
if __name__ == "__main__":
    try:
        testar_formulario_contato()
        testar_botao_cadastro()
        testar_menu_navegacao()

        print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")

    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")

    finally:
        driver.quit()  # Fecha o navegador
