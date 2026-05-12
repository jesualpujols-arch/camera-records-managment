from os import listdir
from os import remove
from os.path import isfile
from os.path import join
from os.path import exists
import datetime
import time
from plyer import notification
def notificacion_log(fecha1, fecha2 = None , fecha3 = None , accion = None, accion2 = None ):
    if accion == 'borrar':
        #notificacion de borrado
        notification.notify(
            title = "Atencion! Grabaciones de camara han sido borradas",
            message = f"Los archivos entre las fechas {fecha2} y {fecha3} han sido borrados hoy",
            timeout = 30
        )
        #log de borrado
        fechas_texto = "\n".join(accion2)
        notificacion_borrado = (
            f"[Fecha de ejecucion: {fecha1}]\n"
            "[EVENTO: Eliminación completada.]\n"
            "[RANGO AFECTADO:]\n"
            f"[{fecha2}  →  {fecha3}]\n"
            "[FECHAS ELIMINADAS:]\n"
            f"{fechas_texto}\n"
        )
    elif accion == 'notificar':
        
        #notificacion de aviso
        notification.notify(
            title = "Atencion! Grabaciones de camara que seran borrados",
            message = f"Los archivos entre las fechas {fecha2} y {fecha3} seran eliminados el dia de mañana",
            timeout = 30
        )
        
        #log de notifacion
        fechas_texto = "\n".join(accion2)
        notificacion_borrado = (
            f"[Fecha de ejecucion: {fecha1}]\n"
            "[EVENTO: Aviso de eliminación programada de grabaciones]\n"
            "[RANGO AFECTADO:]\n"
            f"[{fecha2}  →  {fecha3}]\n"
            "[FECHAS A ELIMINAR:]\n"
            f"{fechas_texto}\n"
            )
    else:
        
        #log de revision
        notificacion_borrado = (
        f"[Fecha de ejecucion: {fecha1}]\n"
        "[EVENTO: SIN ACCION]\n"
        "[DETALLE:]\n"
        'No hay suficientes dias para notificar.\n'
        )
    with open("logs de camaras","a") as archivo:
        archivo.write(notificacion_borrado)
def borrar_archivo(a, b):
    for i in a:
        if i in b:
            for archivo in b[i]:
                remove(archivo)

#creamos un bucle infinito
while True:
    
    #actualizamos fecha y log
    fecha_hoy = datetime.datetime.now()
    if exists("logs de camaras"):
        with open("logs de camaras") as archivo:
            ultimo_log = archivo.readlines()
    else:
        ultimo_log = []
    
    #evitamos que se rompa la primera vez
    ultimo = [i.strip() for i in ultimo_log]
    ultimo_final = [i for i in ultimo if "Fecha de ejecucion:" in i]
    if ultimo_final == []:
        ejecutar = True
    else:
        
        #evitar que ejecute dos veces en un dia
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
            
            #evitamos que se ejecute fuera de horario
            hora = fecha_hoy.time()
            horario1 = datetime.time(13, 45)
            horario2 = datetime.time(14,15)
            if horario1 <= hora <= horario2:
                
                #creando la ruta de los archivos
                ruta = r"G:\camaras\video\FSDMP\video\FSDMP"
                carpeta = listdir(ruta)
                ruta_videos = [join(ruta, i) for i in carpeta if isfile(join(ruta, i))]
                
                #separando archivos por edad
                dia_grabaciones = {}
                for i in ruta_videos:
                    z = i.split("_")[1]
                    if z not in dia_grabaciones:
                        dia_grabaciones[z] = []
                    dia_grabaciones[z].append(i)
                por_notificar = [i for i in dia_grabaciones if (fecha_hoy - datetime.datetime.strptime(i, "%Y-%m-%d")).days > 21]
                
                #separando dias viejos por grupo de 7 o mas dias 
                if len(por_notificar) >= 7:
                    por_notificar.sort()
                    primera_fecha = por_notificar[0]
                    ultima_fecha = por_notificar[-1]
                    
                    #filtrado de logs
                    with open("logs de camaras") as archivo:
                        ya_notificadas = archivo.readlines()
                    ya_notificados = [i.strip() for i in ya_notificadas]
                    notificadas = {i.strip() for i in ya_notificadas if len(i.strip()) == 10}
                    
                    #verificando que se notifique correctamente 
                    notificar = [i for i in por_notificar if i not in notificadas]
                    
                    #notificacion de aviso
                    notificacion_log(fecha_hoy, primera_fecha, ultima_fecha, 'notificar', notificar)
                    
                    #borrado de archivos
                    borrar = [i for i in notificadas if i not in notificar]
                    borrar_archivo(borrar, dia_grabaciones)
                    
                    #notificando el borrado
                    borrar.sort()
                    if borrar:
                        primera_borrado = borrar[0]
                        ultima_borrado = borrar[-1]
                        
                        #notificacion de borrado
                        notificacion_log(fecha_hoy, primera_borrado, ultima_borrado, 'borrar', borrar)
                else:
                    
                    #log de revision
                    notificacion_log(fecha_hoy)
    
    #tiempo que el script duerme
    time.sleep(6*3600)