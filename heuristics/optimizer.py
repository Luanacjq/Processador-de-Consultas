def apply_heuristics(parsed):
    steps = []

    steps.append("Árvore Inicial: execução direta com JOIN")

    selection_steps = []
    for cond in parsed["where"]:
        table = cond.split(".")[0]
        selection_steps.append(f"σ {cond}({table})")

    steps.append("Heurística 1 (Redução de Tuplas):\n" + "\n".join(selection_steps))

    projection_steps = []
    for field in parsed["select"]:
        table = field.split(".")[0]
        projection_steps.append(f"π {field}({table})")

    steps.append("Heurística 2 (Redução de Atributos):\n" + "\n".join(projection_steps))

    return steps