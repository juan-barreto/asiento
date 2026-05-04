def validar_movimientos(movimientos):
    """
    Valida y limpia movimientos devueltos por la IA.
    - Evita datos corruptos
    - Convierte a float
    - Filtra inconsistencias
    """
    resultado = []
    for m in movimientos:
        # Validar fecha
        if not m.get("fecha"):
            continue
        # Validar números
        try:
            debito = float(m.get("debito", 0))
            credito = float(m.get("credito", 0))
            saldo = float(m.get("saldo", 0))
        except:
            continue
        # No puede haber debito y credito juntos
        if debito > 0 and credito > 0:
            continue
        # Normalizar texto
        m["descripcion"] = m.get("descripcion", "").strip()
        m["detalle"] = m.get("detalle", "").strip()
        resultado.append(m)
    return resultado