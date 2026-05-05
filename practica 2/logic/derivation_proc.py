# logic/derivation_proc.py
import nltk

class DerivationProcessor:
    def __init__(self, parse_tree):
        self.tree = parse_tree

    def get_left_derivation(self):
        """
        Genera la derivación por la izquierda paso a paso.
        Reemplaza el símbolo no terminal más a la izquierda en cada iteración.
        """
        if not self.tree:
            return []
        
        steps = []
        # El símbolo inicial es la raíz del árbol
        current_string = [self.tree.label()]
        steps.append(" ".join(current_string))
        
        # tree.productions() devuelve las reglas aplicadas en orden Pre-Order (Derivación izquierda)
        for prod in self.tree.productions():
            lhs = prod.lhs().symbol()
            # Convertir los elementos del lado derecho a strings
            rhs = [sym.symbol() if isinstance(sym, nltk.grammar.Nonterminal) else str(sym) for sym in prod.rhs()]
            
            # Buscar el primer no terminal coincidente de izquierda a derecha
            for i, sym in enumerate(current_string):
                if sym == lhs:
                    # Reemplazar el no terminal por su expansión
                    current_string = current_string[:i] + rhs + current_string[i+1:]
                    steps.append(" ".join(current_string))
                    break
        return steps

    def get_right_derivation(self):
        """
        Genera la derivación por la derecha paso a paso.
        Reemplaza el símbolo no terminal más a la derecha en cada iteración.
        """
        if not self.tree:
            return []
            
        steps = []
        current_string = [self.tree.label()]
        steps.append(" ".join(current_string))
        
        # Para la derivación por la derecha, necesitamos las producciones en orden inverso al de su expansión en el lado derecho.
        # Un enfoque práctico es mapear el árbol y procesar los hijos de derecha a izquierda.
        
        def traverse_rightmost(node, strings_list):
            if isinstance(node, nltk.Tree):
                # El lado izquierdo de la producción
                lhs = node.label()
                rhs = [child.label() if isinstance(child, nltk.Tree) else child for child in node]
                
                # Encontrar y reemplazar el último (más a la derecha) símbolo igual a lhs
                for i in range(len(strings_list[-1]) - 1, -1, -1):
                    if strings_list[-1][i] == lhs:
                        new_string = strings_list[-1][:i] + rhs + strings_list[-1][i+1:]
                        strings_list.append(new_string)
                        break
                        
                # Recursión de derecha a izquierda
                for child in reversed(node):
                    traverse_rightmost(child, strings_list)

        strings_sequence = [current_string]
        traverse_rightmost(self.tree, strings_sequence)
        
        # Formatear la salida
        for seq in strings_sequence[1:]:
            steps.append(" ".join(seq))
            
        return steps