def getProvinciMunicipioDeQ(q:str):
    l = q.split(",")
    provincia = ""
    municipio = ""
    if len(l) > 1:
        provincia = l[0]
        municipio = l[1]
    return (provincia,municipio)