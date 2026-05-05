# logic/ast_builder.py
from nltk.tree import Tree

class ASTBuilder:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree

    def build_ast(self):
        """
        Construye el AST omitiendo nodos redundantes y destacando la estructura clave[cite: 1].
        """
        if not self.parse_tree:
            return None
        return self._simplify(self.parse_tree)

    def _simplify(self, tree):
        """
        Método recursivo para colapsar producciones unitarias (ej. E -> T -> F -> 'id').
        """
        if not isinstance(tree, Tree):
            return tree  # Es un nodo terminal u hoja

        # Simplificar primero todos los hijos
        simplified_children = [self._simplify(child) for child in tree]
        
        # Regla de simplificación: Si el nodo actual tiene exactamente 1 hijo
        # y ese hijo también es un subárbol (no es un terminal), omitimos este nodo
        # para reducir el nivel jerárquico innecesario.
        if len(simplified_children) == 1 and isinstance(simplified_children[0], Tree):
            return simplified_children[0]
            
        # Si tiene múltiples hijos o un solo hijo terminal, conservamos el nodo
        return Tree(tree.label(), simplified_children)