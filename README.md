# 🚀 NASA DONKI GST Dashboard

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-brightgreen)](https://github.com/features/actions)
[![Supabase](https://img.shields.io/badge/Supabase-Database-green)](https://supabase.com)
[![NASA DONKI](https://img.shields.io/badge/NASA-DONKI-orange)](https://api.nasa.gov/)

Dashboard interativo para visualização de tempestades geomagnéticas (GST) usando a API pública DONKI da NASA. Desenvolvido como atividade escolar para as trilhas B (GitHub Copilot Estudante) e D (Continue.dev + DeepSeek).

---

## 🎯 Objetivo

Substituir o exemplo de voos/SIROS por um dashboard moderno que:
- Consome dados da API **DONKI (GST)** da NASA.
- Funciona offline com um JSON de exemplo.
- Utiliza boas práticas de segurança, organização e automação.
- É totalmente responsivo e visualmente atrativo.

---

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nasa-donki-dashboard.git
   cd nasa-donki-dashboard
   ```

2. Crie um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo de exemplo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   Edite o `.env` com sua chave da NASA (opcional) e credenciais do Supabase.

---

## ▶️ Execução

### Servir a página localmente
Abra o arquivo `index.html` em um navegador ou use um servidor local:
```bash
python -m http.server 8000
```
Acesse `http://localhost:8000`.

### Atualizar dados via script Python
```bash
python scripts/fetch_donki.py
```

---

## 🌐 GitHub Pages

Ative o GitHub Pages no repositório (branch `main`, pasta `/root`).

---

## 🗄️ Supabase

Execute `sql/setup.sql` no SQL Editor do Supabase e configure `.env`.

---

## 📡 API DONKI

`https://api.nasa.gov/DONKI/GST` com parâmetros `startDate`, `endDate` e `api_key`.

---

## 📁 Estrutura do Projeto

```
nasa-donki-dashboard/
├── .github/
├── .continue/
├── assets/
├── data/
├── scripts/
├── sql/
├── .env.example
├── config.example.yaml
├── requirements.txt
├── README.md
└── index.html
```

---

## 🛡️ Segurança

- Escapamento de HTML com `escapeHtml()`.
- Variáveis sensíveis em `.env`.
- RLS no Supabase.

---

## 📝 Licença

MIT
