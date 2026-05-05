# gui/main_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QLineEdit, QPushButton, QRadioButton,
                             QButtonGroup, QLabel, QMessageBox, QGroupBox, QTabWidget)
from PyQt6.QtCore import Qt
from .widgets import TreeCanvasWidget
from logic.grammar_engine import GrammarEngine
from logic.derivation_proc import DerivationProcessor
from logic.ast_builder import ASTBuilder
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Árboles y Gramáticas CFG")
        self.setGeometry(100, 100, 1200, 700)

        # Instancias de nuestras clases lógicas (Backend)
        self.engine = GrammarEngine()

        # Configurar la Interfaz
        self._setup_ui()

    def _setup_ui(self):
        # Widget y Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- PANEL IZQUIERDO: Entradas ---
        left_panel = QVBoxLayout()
        
        # 1. Definición de la Gramática
        lbl_grammar = QLabel("Definición de Gramática (Formato NLTK/BNF):")
        self.txt_grammar = QTextEdit()
        
        # Gramática todoterreno que cubre todo el alfabeto y los números base
        gramatica_todoterreno = (
            "S -> E\n"
            "E -> E '+' T | E '-' T | T\n"
            "T -> T '*' F | T '/' F | F\n"
            "F -> '(' E ')' | Letra | Numero\n"
            "Letra -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'\n"
            "Numero -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'"
        )
        self.txt_grammar.setPlainText(gramatica_todoterreno)
        left_panel.addWidget(lbl_grammar)
        left_panel.addWidget(self.txt_grammar)

        # 2. Expresión Objetivo
        lbl_expr = QLabel("Expresión Objetivo:")
        self.txt_expr = QLineEdit()
        self.txt_expr.setText("4 - ( 5 - 5 ) * x") # Un ejemplo mixto por defecto
        left_panel.addWidget(lbl_expr)
        left_panel.addWidget(self.txt_expr)

        # 3. Opciones de Derivación
        group_derivation = QGroupBox("Opciones de Derivación")
        vbox_deriv = QVBoxLayout()
        self.rb_left = QRadioButton("Derivación por la Izquierda")
        self.rb_right = QRadioButton("Derivación por la Derecha")
        self.rb_left.setChecked(True) # Por defecto
        
        self.deriv_group = QButtonGroup()
        self.deriv_group.addButton(self.rb_left)
        self.deriv_group.addButton(self.rb_right)
        
        vbox_deriv.addWidget(self.rb_left)
        vbox_deriv.addWidget(self.rb_right)
        group_derivation.setLayout(vbox_deriv)
        left_panel.addWidget(group_derivation)

        # 4. Botón Generar
        self.btn_generate = QPushButton("Generar Derivación y Árboles")
        self.btn_generate.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_generate.clicked.connect(self.process_grammar)
        left_panel.addWidget(self.btn_generate)

        # --- PANEL CENTRAL: Derivación Paso a Paso ---
        center_panel = QVBoxLayout()
        lbl_steps = QLabel("Derivación Paso a Paso:")
        self.txt_steps = QTextEdit()
        self.txt_steps.setReadOnly(True)
        center_panel.addWidget(lbl_steps)
        center_panel.addWidget(self.txt_steps)

        # --- PANEL DERECHO: Visualización (Árboles) ---
        right_panel = QVBoxLayout()
        self.tabs = QTabWidget()
        
        # Pestaña para el Árbol de Derivación
        self.tab_derivation_tree = TreeCanvasWidget()
        self.tabs.addTab(self.tab_derivation_tree, "Árbol de Derivación")
        
        # Pestaña para el AST
        self.tab_ast = TreeCanvasWidget()
        self.tabs.addTab(self.tab_ast, "Árbol de Sintaxis Abstracta (AST)")
        
        right_panel.addWidget(self.tabs)

        # Asignar proporciones de la pantalla (Izquierda: 25%, Centro: 25%, Derecha: 50%)
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(center_panel, 1)
        main_layout.addLayout(right_panel, 2)

    def process_grammar(self):
        """
        Método controlador que conecta la UI con la lógica cuando se presiona el botón.
        """
        grammar_str = self.txt_grammar.toPlainText()
        expr_str = self.txt_expr.text().strip()

        if not grammar_str or not expr_str:
            QMessageBox.warning(self, "Error", "Por favor ingrese la gramática y la expresión.")
            return

        # 1. Cargar Gramática
        success, msg = self.engine.load_grammar(grammar_str)
        if not success:
            QMessageBox.critical(self, "Error de Gramática", msg)
            return

        # --- EL AUTO-FORMATEADOR ---
        # Convierte cosas como "4-(5)*x" en "4 - ( 5 ) * x" automáticamente
        expr_limpia = re.sub(r'([+\-*/()])', r' \1 ', expr_str)
        tokens = expr_limpia.split()
        
        # 2. Analizar Expresión
        parse_tree, msg = self.engine.parse_expression(tokens)
        
        if not parse_tree:
            QMessageBox.critical(self, "Error de Análisis", msg)
            return

        # 3. Procesar Derivación (Izquierda o Derecha)
        processor = DerivationProcessor(parse_tree)
        if self.rb_left.isChecked():
            steps = processor.get_left_derivation()
        else:
            steps = processor.get_right_derivation()

        # Mostrar los pasos en el panel central
        self.txt_steps.setPlainText("\n".join(["⇒ " + step for step in steps]))

        # 4. Generar AST
        ast_builder = ASTBuilder(parse_tree)
        ast_tree = ast_builder.build_ast()

        # 5. Dibujar los árboles
        self.tab_derivation_tree.clear()
        self.tab_ast.clear()
        
        from utils.tree_visualizer import TreeVisualizer
        TreeVisualizer.draw_nltk_tree(parse_tree, self.tab_derivation_tree.canvas.axes)
        self.tab_derivation_tree.canvas.draw()
        
        if ast_tree:
            TreeVisualizer.draw_nltk_tree(ast_tree, self.tab_ast.canvas.axes)
            self.tab_ast.canvas.draw()