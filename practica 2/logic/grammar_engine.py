# logic/grammar_engine.py
import nltk
from nltk import CFG

class GrammarEngine:
    def __init__(self):
        self.grammar = None
        self.parser = None

    def load_grammar(self, grammar_str):
        """
        Carga la gramática en formato de texto y crea el objeto CFG de NLTK.
        Las reglas deben estar en un formato que NLTK entienda (ej. S -> E).
        """
        try:
            # Dividir el string por saltos de línea para procesar regla por regla
            rules = grammar_str.strip().split('\n')
            formatted_rules = "\n".join([rule.strip() for rule in rules if rule.strip()])
            
            self.grammar = CFG.fromstring(formatted_rules)
            self.parser = nltk.ChartParser(self.grammar)
            return True, "Gramática cargada exitosamente."
        except Exception as e:
            return False, f"Error al procesar la gramática: {str(e)}"

    def parse_expression(self, expression_tokens):
        """
        Analiza la expresión objetivo usando el ChartParser.
        expression_tokens debe ser una lista de strings (ej. ['4', '-', '(', '5', ')']).
        """
        if not self.parser:
            return None, "Primero debes cargar una gramática válida."
        try:
            # El parser genera múltiples árboles si hay ambigüedad; tomamos el primero
            trees = list(self.parser.parse(expression_tokens))
            if not trees:
                return None, "La expresión no es válida o no pertenece a esta gramática."
            return trees[0], "Árbol de derivación generado."
        except Exception as e:
            return None, f"Error de análisis: {str(e)}"