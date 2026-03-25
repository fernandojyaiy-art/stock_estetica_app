def evaluar_stock(cremas):
    if len(cremas) == 0:
        return "No hay productos cargados. Agregá stock."
    elif len(cremas) == 1:
        return "Solo queda 1 producto. Revisar stock."
    return None


def productos_bajo_stock(cremas):
  
    return [c for c in cremas if c.cantidad <= 1]