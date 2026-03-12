# 📋 Controle de Contratos — SEFA 2026

Sistema web completo para gerenciamento de contratos com banco de dados real (SQLite).
Desenvolvido com Python/Flask. Pronto para publicar no Railway.

---

## 🚀 Como publicar no Railway (passo a passo)

### 1. Crie uma conta gratuita no GitHub
Acesse https://github.com e crie uma conta se ainda não tiver.

### 2. Crie um repositório no GitHub
1. Clique em **"New repository"** (botão verde)
2. Nome: `contratos-sefa` (ou qualquer nome)
3. Marque **"Private"** (recomendado para sistema interno)
4. Clique em **"Create repository"**

### 3. Faça upload dos arquivos
1. Na página do repositório criado, clique em **"uploading an existing file"**
2. Arraste **TODOS** os arquivos desta pasta:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`
   - `seed_data.json`
   - Pasta `templates/` com o arquivo `index.html` dentro
3. Clique em **"Commit changes"**

### 4. Crie uma conta no Railway
1. Acesse https://railway.app
2. Clique em **"Login"** → **"Login with GitHub"**
3. Autorize o Railway a acessar sua conta GitHub

### 5. Crie o projeto no Railway
1. Clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha o repositório `contratos-sefa`
4. O Railway detecta automaticamente que é Python e faz o deploy

### 6. Aguarde o deploy (1-3 minutos)
- Você verá os logs em tempo real
- Quando aparecer **"Deploy successful"**, está no ar!

### 7. Acesse a URL
1. Clique no serviço criado
2. Vá em **"Settings"** → **"Domains"**
3. Clique em **"Generate Domain"**
4. Você receberá uma URL como: `https://contratos-sefa-production.up.railway.app`

---

## 🌐 Acessando de qualquer lugar
Após publicado, qualquer pessoa com a URL pode:
- Acessar pelo computador, celular ou tablet
- Ver todos os contratos em tempo real
- Criar, editar e excluir registros
- As alterações ficam salvas no servidor e aparecem para todos

---

## 💾 Sobre os dados
- O banco de dados SQLite fica no servidor do Railway
- Os 123 contratos da planilha original já estão pré-carregados
- Todos os registros novos são salvos permanentemente no servidor

---

## 💰 Custo
- Plano gratuito do Railway: **$5 de crédito/mês**
- Um sistema deste porte consome cerca de **$0,50–$1,00/mês**
- Na prática: **gratuito** para uso interno

---

## 🔧 Rodando localmente (opcional)
```bash
pip install flask gunicorn
python app.py
# Acesse: http://localhost:5000
```

---

## 📁 Estrutura dos arquivos
```
contratos_app/
├── app.py              ← Backend Python/Flask (API + servidor)
├── requirements.txt    ← Dependências Python
├── Procfile            ← Comando de inicialização para Railway
├── railway.json        ← Configuração do Railway
├── seed_data.json      ← Dados iniciais (123 contratos)
└── templates/
    └── index.html      ← Interface do sistema (frontend)
```
