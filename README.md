# Readme: API de Atribuição de Funções no Discord com Ngrok

## Visão Geral
Este aplicativo baseado em FastAPI fornece uma API simples para atribuir funções a usuários do Discord com base em um identificador único (starter_id) e um código de autorização. Ele foi projetado para integrar-se ao Discord OAuth2 para autenticação de usuários e atribuição de funções em um servidor Discord (guild) específico.

## Pré-requisitos
Antes de executar este código com Ngrok, certifique-se de ter os seguintes pré-requisitos:

1. **Conta de Desenvolvedor Discord**: Você precisa ter uma conta de desenvolvedor do Discord e ter criado um aplicativo Discord para obter os valores `CLIENT_ID`, `SECRET`, `REDIRECT_URI`, `BOT_TOKEN` e `GUILD_ID` necessários para este aplicativo. Você pode configurar uma conta de desenvolvedor Discord e criar um aplicativo em [Discord Developer Portal](https://discord.com/developers/applications).

2. **Variáveis de Ambiente**: Você deve configurar variáveis de ambiente para os seguintes valores, que serão usados no aplicativo:
   - `CLIENT_ID`: O ID do cliente Discord do seu aplicativo.
   - `SECRET`: O segredo do cliente do seu aplicativo.
   - `REDIRECT_URI`: O URI de redirecionamento configurado para o seu aplicativo no Discord Developer Portal.
   - `BOT_TOKEN`: O token do bot Discord (necessário para autorização).
   - `GUILD_ID`: O ID do servidor Discord (guild) onde você deseja atribuir funções.

3. **Ambiente Python**: Verifique se você tem o Python instalado em seu sistema.

4. **Ngrok**: Certifique-se de ter o Ngrok instalado e configurado em seu sistema. Você pode obtê-lo em [Ngrok](https://ngrok.com/).

## Instalação
1. Clone este repositório em sua máquina local ou servidor.

2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS e Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instale os pacotes Python necessários usando `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração
1. Defina as variáveis de ambiente necessárias para `CLIENT_ID`, `SECRET`, `REDIRECT_URI`, `BOT_TOKEN` e `GUILD_ID` em um arquivo `.env` ou diretamente em seu ambiente.

2. Modifique o dicionário `hash_to_role_map` para mapear os valores `starter_id` para os IDs de função correspondentes em seu servidor Discord. Este dicionário é usado para determinar qual função atribuir aos usuários com base em seu `starter_id`.

3. Inicie o Ngrok para expor sua API local para a internet usando o seguinte comando:
   ```bash
   ngrok http 8000
   ```

   O Ngrok fornecerá um URL público que você usará como seu `REDIRECT_URI` no Discord Developer Portal.

## Executando o Aplicativo
Para executar o aplicativo, execute o seguinte comando a partir do diretório do projeto:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará acessível localmente em `http://localhost:8000` e será exposta para a internet por meio do URL fornecido pelo Ngrok.

## Pontos de Extremidade da API

### `GET /join/{starter_id}`
- Este ponto de extremidade é usado para ingressar no servidor Discord (guild) e atribuir uma função a um usuário.
- **Parâmetros**:
  - `starter_id` (int): O identificador único do usuário.
  - `code` (str): O código de autorização obtido por meio do fluxo de autenticação do Discord OAuth2.
- **Resposta**:
  - Se o usuário for autenticado com sucesso e receber uma função, ele será redirecionado para o servidor Discord especificado por `GUILD_ID`.
  - Se ocorrer algum erro durante o processo, uma resposta JSON de erro será retornada.

## Tratamento de Erros
- Se qualquer etapa do processo de autenticação ou atribuição de função falhar, uma resposta JSON de erro será retornada. A mensagem de erro será