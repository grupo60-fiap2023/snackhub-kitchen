# snackhub-kitchen

Este repositório contém a parte da aplicação responsável por exibir os pedidos de acordo com seu status, assim como atualizá-los.

Para executar a aplicação, após baixar o código, é necessário seguir alguns passos, incluindo:

- Instalação de dependências
- Configuração do ambiente AWS e SQS
- Configuração de variáveis de ambiente

## Instalando dependências:

1. Certifique-se de que o Python está instalado em sua máquina.
2. Utilize o comando `pip --version` para verificar se o pip está instalado na máquina.
3. Caso o pip não esteja instalado, execute o comando `python -m ensurepip --default-pip`.
4. Execute o comando `pip install -r requirements.txt` para baixar todas as dependências.

## Configuração do ambiente AWS e SQS:

Para que o sistema funcione, é necessário criar 2 filas no SQS, no formato padrão, com os nomes "order-successful-topic" e "order-status-topic" para postagem das mensagens na fila.

## Configuração de variáveis de ambiente:

Para que o sistema funcione corretamente, é necessário ter algumas variáveis configuradas:

- REGION = a região da AWS onde as filas estão localizadas
- AWS_ACCESS_KEY_ID = Chave de acesso da conta AWS
- AWS_SECRET_ACCESS_KEY = Chave secreta da conta AWS
- MYSQL_USER = usuário do MySQL do banco de dados
- MYSQL_PW = senha do MySQL do banco de dados
- IP_APP = IP para acessar o banco de dados
- PORT = porta para acessar o banco de dados

## Executando Testes:

Para executar os testes, a aplicação deve estar rodando localmente. Basta utilizar o executável 'subir app dev.bat' para a execução.
Para rodar os testes, utilize o executável 'executar testes.bat'.
Para verificar a cobertura de código da aplicação, utilize o executável 'executar coverage.bat'.


# Sonar

Segue o link do sonar, comprovando o coverage acima de 80%

![image](https://github.com/grupo60-fiap2023/snackhub-kitchen/assets/2027566/c962c98d-2f26-439f-b23c-9757dde43745)

