from os import listdir
from os import remove
from os.path import isfile
from os.path import join
import datetime
import time
from plyer import notification
while True:
    fecha_hoy = datetime.datetime.now()
    with open("logs de camaras") as archivo:
        ultimo_log = archivo.readlines()
    ultimo = []
    for i in ultimo_log:
        z = i.strip()
        ultimo.append(z)
    ultimo_final = []
    for i in ultimo:
        if "Fecha de ejecucion:" in i:
            ultimo_final.append(i)
    if ultimo_final == []:
        ejecutar = True
    else:
        log_final = ultimo_final[-1]
        log_ultimo = log_final.split(" ")
        log_final = log_ultimo[3]
        log_ultimo = datetime.datetime.strptime(log_final, "%Y-%m-%d")
        log_ultimo = log_ultimo.date()
        
        if fecha_hoy.date() != log_ultimo:
            ejecutar = True
        else:
            ejecutar = False
    if ejecutar:
            hora = fecha_hoy.time()
            horario1 = datetime.time(13, 45)
            horario2 = datetime.time(14,15)
            if horario1 <= hora <= horario2:
                ruta = r"G:\camaras\video\FSDMP\video\FSDMP"
                carpeta = listdir(ruta)
                ruta_videos = []
                nombres_completos = []
                nombres = []
                dias = []
                days = []
                fechas_archivos = []
                notificacion = []
                por_notificar = []
                dia_grabaciones = {}
                for i in carpeta:
                    z = join(ruta, i)
                    if isfile(z):
                        ruta_videos.append(z)
                for i in ruta_videos:
                    z = i.split("_")
                    nombres_completos.append(z)
                for i in nombres_completos:
                    z = i[1]
                    nombres.append(z)
                for i in nombres:
                    z = datetime.datetime.strptime(i, "%Y-%m-%d")
                    fechas_archivos.append(z)
                for i in fechas_archivos:
                    z = fecha_hoy - i
                    dias.append(z)
                for i in dias:
                    z = i.days
                    days.append(z)
                for archivo, fecha, dia in zip(ruta_videos, fechas_archivos, days):
                    notificacion.append(fecha)
                fechas_ordenadas = list(set(notificacion))
                fechas_ordenadas.sort()
                for i in ruta_videos:
                    z = i.split("_")[1]
                    if z not in dia_grabaciones:
                        dia_grabaciones[z] = []
                    dia_grabaciones[z].append(i)
                for i in dia_grabaciones:
                    z = datetime.datetime.strptime(i, "%Y-%m-%d")
                    y = fecha_hoy - z
                    x = y.days
                    if x > 21:
                        por_notificar.append(i)
                if len(por_notificar) >= 7:
                    por_notificar.sort()
                    primera_fecha = ""
                    ultima_fecha = ""
                    primera_fecha = por_notificar[0]
                    ultima_fecha = por_notificar[-1]
                    ya_notificadas = []
                    ya_notificados = []
                    with open("logs de camaras") as archivo:
                        ya_notificadas = archivo.readlines()
                    for i in ya_notificadas:
                        z = i.strip()
                        ya_notificados.append(z)
                    notificadas = []
                    notificar = []
                    for i in ya_notificados:
                        if len(i) == 10:
                            if "-" in i:
                                notificadas.append(i)
                    for i in por_notificar:
                        if i not in notificadas:
                            notificar.append(i)
                    notification.notify(
                        title = "Atencion! Grabaciones de camara que seran borrados",
                        message = f"Los archivos entre las fechas {primera_fecha} y {ultima_fecha} seran eliminados el dia de mañana",
                        timeout = 30
                    )
                    print(fecha_hoy)
                    print(primera_fecha)
                    print(ultima_fecha)
                    print(notificar)
                    fechas_texto = "\n".join(notificar)
                    notificacion_final = (
                        f"[Fecha de ejecucion: {fecha_hoy}]\n"
                        "[EVENTO: Aviso de eliminación programada de grabaciones]\n"
                        "[RANGO AFECTADO:]\n"
                        f"[{primera_fecha}  →  {ultima_fecha}]\n"
                        "[FECHAS A ELIMINAR:]\n"
                        f"{fechas_texto}\n"
                    )
                    with open("logs de camaras","a") as archivo:
                        archivo.write(notificacion_final)
                    
                    borrar = []
                    for i in notificadas:
                        if i not in notificar:
                            borrar.append(i)
                    for D in borrar:
                        if D in dia_grabaciones:
                            for archivo in dia_grabaciones[D]: 
                                remove(archivo)
                    borrar.sort()
                    if borrar != []:
                        primera_borrado = borrar[0]
                        ultima_borrado = borrar[-1]
                        notification.notify(
                            title = "Atencion! Grabaciones de camara han sido borradas",
                            message = f"Los archivos entre las fechas {primera_borrado} y {ultima_borrado} han sido borrados hoy",
                            timeout = 30
                        )
                        print(fecha_hoy)
                        print(primera_borrado)
                        print(ultima_borrado)
                        print(borrar)
                        fechas_texto = "\n".join(borrar)
                        notificacion_borrado = (
                            f"[Fecha de ejecucion: {fecha_hoy}]\n"
                            "[EVENTO: Eliminación completada.]\n"
                            "[RANGO AFECTADO:]\n"
                            f"[{primera_borrado}  →  {ultima_borrado}]\n"
                            "[FECHAS ELIMINADAS:]\n"
                            f"{fechas_texto}\n"
                        )
                        with open("logs de camaras","a") as archivo:
                            archivo.write(notificacion_borrado)
                else:
                    notificacion_nada = (
                        f"[Fecha de ejecucion: {fecha_hoy}]\n"
                        "[EVENTO: SIN ACCION]\n"
                        "[DETALLE:]\n"
                        'No hay suficientes dias para notificar.\n'
                    )
                    with open("logs de camaras","a") as archivo:
                        archivo.write(notificacion_nada)
    time.sleep(6*3600)