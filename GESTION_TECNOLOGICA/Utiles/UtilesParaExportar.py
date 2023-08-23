def retornarBienDatoExportar(metodo):
    def accion(a,*b,**c):
        try:
            return metodo(a,*b,**c)
        except Exception as e:
            pass
        else:
            pass
        finally:
            pass
        return ""
    return accion

