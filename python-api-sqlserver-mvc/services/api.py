import requests
from flask import current_app
ALIASES={"municipio":["municipio"],"tipo":["tipo_de_atractivo","tipo de atractivo","tipo"],"subregion":["subregion"],"nombre":["atractivo_turistico_o_producto","atractivo turístico o producto","nombre"],"ubicacion":["lugar_de_ubicacion","lugar de ubicacion","ubicacion"],"descripcion":["descripcion","descripción"],"id":[":id","id","id_api"]}
def normalize(row,i):
    d={str(k).lower().strip():v for k,v in row.items()}
    x={k:next((str(d[a]).strip() for a in aliases if d.get(a) not in (None,"")), "") for k,aliases in ALIASES.items()}
    if not x["nombre"]: return None
    x["id"]=x["id"] or f"generated-{i}-{x['nombre'][:40]}"
    return x
def fetch_rows():
    r=requests.get(current_app.config["API_URL"],headers={"Accept":"application/json"},timeout=45); r.raise_for_status()
    p=r.json()
    rows=p if isinstance(p,list) else next((p[k] for k in ("data","results","records","result") if isinstance(p.get(k),list)),None) if isinstance(p,dict) else None
    if rows is None: raise ValueError("La API respondió, pero no se reconoció una lista de registros. Revise services/api.py y el formato JSON.")
    result=[normalize(x,i) for i,x in enumerate(rows,1) if isinstance(x,dict)]
    result=[x for x in result if x]
    if not result: raise ValueError("No se encontraron registros con el campo del nombre del atractivo.")
    return result
def import_rows(rows):
    from models.db import db
    new=updated=0
    with db() as c:
        cur=c.cursor()
        for x in rows:
            mid=tid=None
            if x["municipio"]:
                cur.execute("IF NOT EXISTS(SELECT 1 FROM dbo.Municipios WHERE nombre=?) INSERT dbo.Municipios(nombre,subregion) VALUES(?,?); SELECT id FROM dbo.Municipios WHERE nombre=?",x["municipio"],x["municipio"],x["subregion"],x["municipio"]); mid=cur.fetchone()[0]
            if x["tipo"]:
                cur.execute("IF NOT EXISTS(SELECT 1 FROM dbo.Tipos WHERE nombre=?) INSERT dbo.Tipos(nombre) VALUES(?); SELECT id FROM dbo.Tipos WHERE nombre=?",x["tipo"],x["tipo"],x["tipo"]); tid=cur.fetchone()[0]
            cur.execute("SELECT id FROM dbo.Atractivos WHERE id_api=?",x["id"]); found=cur.fetchone()
            vals=(mid,tid,x["nombre"],x["ubicacion"] or None,x["descripcion"] or None)
            if found:
                cur.execute("UPDATE dbo.Atractivos SET municipio_id=?,tipo_id=?,nombre=?,ubicacion=?,descripcion=?,origen='API',fecha_importacion=SYSDATETIME() WHERE id_api=?",*vals,x["id"]); updated+=1
            else:
                cur.execute("INSERT dbo.Atractivos(id_api,municipio_id,tipo_id,nombre,ubicacion,descripcion,origen,fecha_importacion) VALUES(?,?,?,?,?,?,'API',SYSDATETIME())",x["id"],*vals); new+=1
        c.commit()
    return {"total":len(rows),"nuevos":new,"actualizados":updated}
