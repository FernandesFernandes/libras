# 🤟 Tradutor Inteligente de Português para Libras



**Sistema de tradução em tempo real de fala para Libras utilizando Inteligência Artificial, geração automática de glosas e integração com o avatar VLibras.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-OpenAI%20Compatible-412991?style=for-the-badge)
![Speech To Text](https://img.shields.io/badge/Speech--to--Text-RealTime-success?style=for-the-badge)
![VLibras](https://img.shields.io/badge/VLibras-Avatar-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

</p>

---

# 📖 Sobre o Projeto

O **Tradutor Português → Libras** foi desenvolvido para tornar conteúdos falados mais acessíveis à comunidade surda.

A aplicação captura o áudio em tempo real, realiza a transcrição utilizando reconhecimento de fala, converte automaticamente o texto para uma **glosa compatível com Libras** e envia o resultado para um avatar baseado no **VLibras**, permitindo a interpretação visual em tempo real.

O projeto possui arquitetura modular, permitindo que cada etapa da tradução funcione de maneira independente.

---

# ✨ Funcionalidades

- 🎤 Captura de áudio em tempo real
- 📝 Transcrição automática da fala
- 🤖 Tradução inteligente para Libras
- 📚 Aplicação de regras linguísticas específicas
- 🔤 Geração automática de glosas
- 👤 Integração com avatar VLibras
- ⚡ Processamento contínuo
- 🖥️ Interface Desktop (Tkinter)
- 📄 Persistência em arquivos JSONL
- 🔄 Arquitetura baseada em serviços independentes

---

# 🏗 Arquitetura

```text
             🎤 Microfone
                   │
                   ▼
        Captura de Áudio
                   │
                   ▼
      Speech-to-Text (STT)
                   │
                   ▼
      Transcrição em Português
                   │
                   ▼
      Tradutor Português → Libras
                   │
                   ▼
         Gerador de Glosas
                   │
                   ▼
            glosas.jsonl
                   │
                   ▼
        Adaptador VLibras
                   │
                   ▼
          Avatar em Libras
```

---

# 📂 Estrutura do Projeto

```text
Libras/
│
├── audio/
│   └── capture.py
│
├── avatar/
│   ├── avatar_adapter.py
│   ├── avatar_queue.py
│   ├── glosa_reader.py
│   ├── signal_map.py
│   ├── token_cleaner.py
│   ├── vlibras_adapter.py
│   └── vlibras_server.py
│
├── libras/
│   ├── translator.py
│   ├── glosa_generator.py
│   ├── lexicon.py
│   └── rules.py
│
├── services/
│   └── service_manager.py
│
├── storage/
│   └── transcript_writer.py
│
├── stt/
│   └── transcriber.py
│
├── ui/
│   └── main_window.py
│
├── tests/
│
├── main.py
├── translator_main.py
└── avatar_main.py
```

---

# ⚙ Fluxo de Funcionamento

## 1️⃣ Captura

O sistema inicia capturando o áudio do usuário.

↓

## 2️⃣ Transcrição

O áudio é convertido em texto utilizando reconhecimento automático de fala.

↓

## 3️⃣ Tradução

O texto é enviado ao módulo responsável pela tradução para Libras.

↓

## 4️⃣ Geração de Glosas

São aplicadas regras linguísticas específicas para produzir glosas compatíveis com a estrutura da Libras.

↓

## 5️⃣ Avatar

As glosas são encaminhadas ao adaptador do VLibras e apresentadas pelo avatar.

---

# 🚀 Como Executar

## Clone o projeto

```bash
git clone https://github.com/SEU-USUARIO/libras-translator.git

cd libras-translator
```

---

## Crie um ambiente virtual

Windows

```bash
python -m venv .venv
```

Linux

```bash
python3 -m venv .venv
```

---

## Ative

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## Instale as dependências

```bash
pip install -r requirements.txt
```

---

# ▶ Executando

## Interface Principal

```bash
python main.py
```

---

## Apenas Tradutor

```bash
python translator_main.py
```

---

## Apenas Avatar

```bash
python avatar_main.py
```

---

# 📁 Arquivos Gerados

| Arquivo | Descrição |
|----------|-----------|
| transcriptions.jsonl | Transcrições em tempo real |
| glosas.jsonl | Glosas produzidas pelo tradutor |
| coverage_report.json | Relatório de cobertura do dicionário |
| missing_signals.json | Sinais ainda não encontrados |

---

# 🧠 Principais Componentes

## 🎤 STT

Responsável por transformar áudio em texto.

---

## 📚 Translator

Aplica regras de tradução específicas para Libras.

---

## 🔤 Glosa Generator

Converte frases em glosas.

---

## 📖 Lexicon

Dicionário de sinais conhecidos.

---

## 📏 Rules

Motor responsável pelas regras gramaticais.

---

## 👤 VLibras Adapter

Realiza a comunicação entre o sistema e o avatar.

---

## 🖥 Interface

Construída em **Tkinter**, responsável por:

- iniciar serviços
- acompanhar a transcrição
- monitorar status
- controlar execução

---

# 🧪 Testes

Os testes podem ser executados com:

```bash
pytest
```

ou

```bash
python -m pytest
```

---

# 🔮 Próximas Evoluções

- [ ] Tradução com contexto
- [ ] Tradução bidirecional
- [ ] Interface Web
- [ ] API REST
- [ ] Streaming via WebSocket
- [ ] Suporte a múltiplos avatares
- [ ] Integração com modelos de IA mais avançados
- [ ] Aprendizado contínuo do dicionário
- [ ] Painel administrativo
- [ ] Estatísticas de tradução

---

# 💡 Tecnologias

- Python
- Tkinter
- Speech-to-Text
- JSONL
- Threads
- Queue
- VLibras
- Inteligência Artificial
- Processamento de Linguagem Natural (NLP)

---

# 🎯 Objetivo

Este projeto busca reduzir barreiras de comunicação entre ouvintes e pessoas surdas, oferecendo uma solução prática para tradução automática de fala em português para Libras utilizando Inteligência Artificial e avatares de interpretação.

---

# 🤝 Contribuições

Contribuições são muito bem-vindas!

Caso encontre algum problema ou tenha sugestões de melhoria:

1. Faça um Fork
2. Crie uma Branch
3. Commit suas alterações
4. Abra um Pull Request

---

# 📄 Licença

Este projeto está distribuído sob a licença **MIT**.

---

# 👨‍💻 Autor

**Fernando Fernandes**

Desenvolvido com ❤️ para promover acessibilidade através da tecnologia.

---

<p align="center">

**"Tecnologia só faz sentido quando aproxima pessoas."**

</p>
