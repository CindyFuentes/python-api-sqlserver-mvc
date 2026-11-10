from models.db import db
def rows(cur):
    names=[x[0] for x in cur.description]; return [dict(zip(names,r)) for r in cur.fetchall()]
def attractions(q="",municipio="",tipo="",limit=None):
    top=f"TOP ({int(limit)}) " if limit else ""
    sql=f"""SELECT {top}a.id,a.nombre,a.ubicacion,a.descripcion,a.origen,m.nombre municipio,t.nombre tipo
    FROM dbo.Atractivos a LEFT JOIN dbo.Municipios m ON m.id=a.municipio_id LEFT JOIN dbo.Tipos t ON t.id=a.tipo_id
    WHERE (?='' OR a.nombre LIKE '%'+?+'%' OR a.descripcion LIKE '%'+?+'%')
    AND (?='' OR m.nombre=?) AND (?='' OR t.nombre=?) ORDER BY a.nombre"""
    with db() as c:
        cur=c.cursor(); cur.execute(sql,q,q,q,municipio,municipio,tipo,tipo); return rows(cur)
def attraction(rid):
    with db() as c:
        cur=c.cursor(); cur.execute("SELECT a.id,a.nombre,a.ubicacion,a.descripcion,m.nombre municipio,t.nombre tipo FROM dbo.Atractivos a LEFT JOIN dbo.Municipios m ON m.id=a.municipio_id LEFT JOIN dbo.Tipos t ON t.id=a.tipo_id WHERE a.id=?",rid)
        x=rows(cur); return x[0] if x else None
def lookup(cur,table,col,value):
    value=(value or "").strip()
    if not value:return None
    cur.execute(f"IF NOT EXISTS(SELECT 1 FROM dbo.{table} WHERE nombre=?) INSERT dbo.{table}(nombre) VALUES(?); SELECT id FROM dbo.{table} WHERE nombre=?",value,value,value); return cur.fetchone()[0]
def save_attraction(f,rid=None):
    if not f.get("nombre","").strip(): raise ValueError("El nombre es obligatorio.")
    with db() as c:
        cur=c.cursor(); mid=lookup(cur,"Municipios","nombre",f.get("municipio")); tid=lookup(cur,"Tipos","nombre",f.get("tipo"))
        vals=(mid,tid,f["nombre"].strip(),f.get("ubicacion"),f.get("descripcion"))
        if rid: cur.execute("UPDATE dbo.Atractivos SET municipio_id=?,tipo_id=?,nombre=?,ubicacion=?,descripcion=? WHERE id=?",*vals,rid)
        else: cur.execute("INSERT dbo.Atractivos(municipio_id,tipo_id,nombre,ubicacion,descripcion,origen) VALUES(?,?,?,?,?,'LOCAL')",*vals)
        c.commit()
def remove_attraction(rid):
    with db() as c: c.cursor().execute("DELETE dbo.Atractivos WHERE id=?",rid); c.commit()
def reviews():
    with db() as c:
        cur=c.cursor(); cur.execute("SELECT r.id,r.atractivo_id,a.nombre atractivo,r.calificacion,r.comentario,r.fecha FROM dbo.Resenas r JOIN dbo.Atractivos a ON a.id=r.atractivo_id ORDER BY r.fecha DESC"); return rows(cur)
def review(rid):
    with db() as c:
        cur=c.cursor(); cur.execute("SELECT id,atractivo_id,calificacion,comentario FROM dbo.Resenas WHERE id=?",rid); x=rows(cur); return x[0] if x else None
def save_review(f,rid=None):
    rating=int(f["calificacion"])
    if rating not in range(1,6): raise ValueError("La calificación debe estar entre 1 y 5.")
    with db() as c:
        cur=c.cursor()
        if rid: cur.execute("UPDATE dbo.Resenas SET atractivo_id=?,calificacion=?,comentario=? WHERE id=?",int(f["atractivo_id"]),rating,f["comentario"].strip(),rid)
        else: cur.execute("INSERT dbo.Resenas(atractivo_id,calificacion,comentario) VALUES(?,?,?)",int(f["atractivo_id"]),rating,f["comentario"].strip())
        c.commit()
def remove_review(rid):
    with db() as c: c.cursor().execute("DELETE dbo.Resenas WHERE id=?",rid); c.commit()
def stats():
    with db() as c:
        cur=c.cursor(); result=[]
        for table in ("Atractivos","Municipios","Tipos","Resenas"):
            cur.execute(f"SELECT COUNT(*) FROM dbo.{table}"); result.append(cur.fetchone()[0])
        return dict(zip(("atractivos","municipios","tipos","resenas"),result))
