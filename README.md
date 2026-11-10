# SketchCraft

**SketchCraft** é uma aplicação de modelagem 3D e CAD inspirada no fluxo de trabalho e funcionalidades clássicas do SketchUp, reconstruída com interface moderna (estilo Fluent Design), renderização acelerada e arquitetura em Python com PyQt6.

---

## 🚀 Funcionalidades

- **Espaço 3D e Navegação**:
  - Eixos ortogonais padrão (Vermelho: X, Verde: Y, Azul: Z).
  - Horizonte dinâmico com iluminação natural, plano de solo e céu personalizáveis.
  - Navegação fluida com Orbitar, Panorâmica (Pan) e Zoom.
  - Figura humana clássica de referência de escala na origem.

- **Ferramentas de Desenho e Modelagem**:
  - Linhas, retângulos, círculos e polígonos.
  - Extrusão (Push/Pull) e manipulação de faces e arestas 3D.
  - Fita métrica, transferidor e medição dimensional em tempo real.
  - Seleção por clique e janela (bounding box).

- **Painel Lateral Integrado (Tray)**:
  - **Materiais & Texturas**: Paleta de cores e acabamentos arquitetônicos.
  - **Etiquetas / Camadas (Tags/Layers)**: Organização e visibilidade de elementos.
  - **Informações da Entidade**: Propriedades e dimensões do objeto selecionado.
  - **Sombras & Iluminação**: Simulação solar e projeção de sombras.

- **Interface Moderna**:
  - Estilo visual contemporâneo (Fluent Design) com bordas arredondadas e ícones vetoriais.
  - Barra de ferramentas configurável e barra de status com coordenadas e dicas em tempo real.

---

## 🛠️ Requisitos e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Pip

### Instalação de Dependências
```bash
pip install PyQt6 PyOpenGL
```

### Executar o Aplicativo
```bash
python app/main.py
```

### Gerar Executável Standalone (Windows)
```bash
pip install pyinstaller
pyinstaller --name "SketchCraft" --windowed --onefile app/main.py
```

---

## 📂 Estrutura do Projeto

```text
Sketch Craft/
├── app/
│   ├── main.py            # Código-fonte principal da aplicação
│   ├── mechanics.json     # Constantes e mecânicas de modelagem
│   ├── MECHANICS.md       # Documentação de mecânicas e medidas
│   └── shots/             # Capturas de tela e testes visuais
├── capture/               # Especificações e referências técnicas
├── reference/             # Imagens e referências visuais
└── README.md
```
