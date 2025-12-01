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
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento = Evento.objects.all().order_by("id")
        lista = EventoSerializer(evento, many=True).data
        for eventos in lista:
            if isinstance(eventos,dict) and "publico_objetivo" in eventos:
                try:
                    eventos["publico_objetivo"] = json.loads(eventos["publico_objetivo"])
                except Exception:
                    eventos["publico_objetivo"] = []       
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
       
    
    # Actualizar datos del evento
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el maestro a actualizar
        evento = get_object_or_404(Evento, id=request.data["id"])
        evento.descripcion=request.data["descripcion"]
        evento.fecha=request.data["fecha"]
        evento.hora_inicio=request.data["hora_inicio"]
        evento.hora_fin=request.data["hora_fin"]
        evento.lugar=request.data["lugar"]
        evento.publico_objetivo=json.dumps(request.data["publico_objetivo"])
        evento.nombre=request.data["nombre"]
        evento.tipo=request.data["tipo"]
        evento.numero_participantes=request.data["numero_participantes"]
        evento.programa_educativo= request.data["programa_educativo"]
        evento.nombre_responsable=request.data["nombre_responsable"]
        evento.save()
        
        return Response({"message": "Maestro actualizado correctamente", "maestro": EventoSerializer(evento).data}, 200)
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        evento = get_object_or_404(Evento, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details":"Evento eliminado"},200)
        except Exception as e:
            
            return Response({"details":"Algo pasó al eliminar"},400)