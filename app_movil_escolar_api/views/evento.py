from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import EventoSerializer
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json 
from django.shortcuts import get_object_or_404


class EventoAll(generics.CreateAPIView):
    #Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener todos los administradores
    def get(self, request, *args, **kwargs):
        evento = Evento.objects.filter(user__is_active = 1).order_by("id")
        lista = EventoSerializer(evento, many=True).data
        return Response(lista, 200)
    
class EventosView(generics.CreateAPIView):
    #Obtener usuario por ID
    # Verifica que el usuario esté autenticado
    def get(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        evento = get_object_or_404(Evento, id = request.GET.get("id"))
        evento = EventoSerializer(evento, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(evento, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)

        evento = Evento.objects.create(
                descripcion=request.data["descripcion"],
                fecha=request.data["fecha"],
                hora_inicio=request.data["hora_inicio"],
                hora_fin=request.data["hora_fin"],
                lugar=request.data["lugar"],
                publico_objetivo=json.dumps(request.data["publico_objetivo"]),
                nombre=request.data["nombre"],
                tipo=request.data["tipo"],
                numero_participantes=request.data["numero_participantes"],
                programa_educativo= request.data["programa_educativo"],
                nombre_responsable=request.data["nombre_responsable"],
            )                               

        evento.save()
        return Response({"evento_created_id": evento.id}, 201)
       
    
    # Actualizar datos del maestro
    # @transaction.atomic
    # def put(self, request, *args, **kwargs):
    #     permission_classes = (permissions.IsAuthenticated,)
    #     # Primero obtenemos el maestro a actualizar
    #     maestro = get_object_or_404(Maestros, id=request.data["id"])
    #     maestro.clave_maestro = request.data["clave_maestro"]
    #     maestro.telefono = request.data["telefono"]
    #     maestro.rfc = request.data["rfc"]
    #     maestro.fecha_nacimiento = request.data["fecha_nacimiento"]
    #     maestro.materias_json = json.dumps(request.data["materias_json"])
    #     maestro.cubiculo = request.data["cubiculo"]
    #     maestro.area_investigacion = request.data["area_investigacion"]
    #     maestro.save()
    #     # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
    #     user = maestro.user
    #     user.first_name = request.data["first_name"]
    #     user.last_name = request.data["last_name"]
    #     user.save()
        
    #     return Response({"message": "Maestro actualizado correctamente", "maestro": MaestrosSerializer(maestro).data}, 200)
    # # Eliminar maestro con delete (Borrar realmente)
    # @transaction.atomic
    # def delete(self, request, *args, **kwargs):
    #     permission_classes = (permissions.IsAuthenticated,)
    #     maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
    #     try:
    #         maestro.user.delete()
    #         return Response({"details":"Maestro eliminado"},200)
    #     except Exception as e:
    #         return Response({"details":"Algo pasó al eliminar"},400)