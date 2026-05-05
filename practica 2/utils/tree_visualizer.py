# utils/tree_visualizer.py
import networkx as nx
from nltk.tree import Tree

class TreeVisualizer:
    """
    Clase utilitaria para transformar un árbol de NLTK en un grafo visible.
    Aplica un algoritmo de espaciado basado en las hojas para evitar superposiciones[cite: 1].
    """
    
    @staticmethod
    def draw_nltk_tree(nltk_tree, ax):
        if not nltk_tree:
            return

        graph = nx.DiGraph()
        pos = {}
        labels = {}
        
        # Variables de estado para calcular las posiciones
        leaf_x = [0]          # Rastrea la posición horizontal disponible para la próxima hoja
        node_counter = [0]    # Garantiza un ID único para cada nodo, incluso si tienen el mismo texto

        def traverse(tree, parent_id=None, depth=0):
            # Asignar un ID único matemático a cada nodo
            node_id = node_counter[0]
            node_counter[0] += 1
            
            # Extraer el texto a mostrar
            label = tree.label() if isinstance(tree, Tree) else str(tree)
            
            graph.add_node(node_id)
            labels[node_id] = label
            
            if parent_id is not None:
                graph.add_edge(parent_id, node_id)
                
            if isinstance(tree, Tree) and len(tree) > 0:
                # Es un nodo intermedio: primero calculamos la posición de sus hijos
                children_x = []
                for child in tree:
                    child_id = traverse(child, node_id, depth + 1)
                    children_x.append(pos[child_id][0])
                
                # La posición X del padre es el centro exacto entre las coordenadas de sus hijos
                x = sum(children_x) / len(children_x)
                y = -depth
                pos[node_id] = (x, y)
            else:
                # Es una hoja: le asignamos el espacio horizontal actual y avanzamos el contador
                x = leaf_x[0]
                y = -depth
                pos[node_id] = (x, y)
                leaf_x[0] += 1.5 # El 1.5 es la separación horizontal entre hojas
                
            return node_id

        # Iniciar el recorrido recursivo
        traverse(nltk_tree)

        # Dibujar el grafo sobre el eje (canvas) proporcionado
        nx.draw(graph, pos, ax=ax, labels=labels, with_labels=True, 
                node_size=900, node_color='lightblue', font_size=10, 
                font_weight='bold', arrows=False)