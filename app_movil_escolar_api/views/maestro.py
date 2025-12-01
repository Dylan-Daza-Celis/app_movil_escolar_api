from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json 
from django.shortcuts import get_object_or_404


class MaestrosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active=1).order_by("id")
        lista = MaestrosSerializer(maestros, many=True).data
        for maestro in lista:
            if isinstance(maestro,dict) and "materias_json" in maestro:
                try:
                    maestro["materias_json"] = json.loads(maestro["materias_json"])
                except Exception:
                    maestro["materias_json"] = []       
        return Response(lista, 200)
    
class MaestrosView(generics.CreateAPIView):
    #Obtener usuario por ID
    # Verifica que el usuario esté autenticado
    def get(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        maestro = get_object_or_404(Maestros, id = request.GET.get("id"))
        maestro = MaestrosSerializer(maestro, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(maestro, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user = UserSerializer(data=request.data)

        if user.is_valid():
            #Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']

            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)


            user.save()

            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()


            maestros = Maestros.objects.create(user=user,
                                                clave_maestro=request.data["clave_maestro"],
                                                fecha_nacimiento=request.data["fecha_nacimiento"],
                                                telefono=request.data["telefono"],
                                                rfc=request.data["rfc"].upper(),
                                                materias_json=json.dumps(request.data["materias_json"]),  # Guardar como JSON string
                                                cubiculo=request.data["cubiculo"],
                                                area_investigacion=request.data["area_investigacion"]  # Cambiar 'area' por 'area_investigacion'
            )                               

            maestros.save()

            return Response({"maestro_created_id": maestros.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar datos del maestro
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el maestro a actualizar
        maestro = get_object_or_404(Maestros, id=request.data["id"])
        maestro.clave_maestro = request.data["clave_maestro"]
        maestro.telefono = request.data["telefono"]
        maestro.rfc = request.data["rfc"]
        maestro.fecha_nacimiento = request.data["fecha_nacimiento"]
        maestro.materias_json = json.dumps(request.data["materias_json"])
        maestro.cubiculo = request.data["cubiculo"]
        maestro.area_investigacion = request.data["area_investigacion"]
        maestro.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = maestro.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Maestro actualizado correctamente", "maestro": MaestrosSerializer(maestro).data}, 200)
    # Eliminar maestro con delete (Borrar realmente)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            maestro.user.delete()
            return Response({"details":"Maestro eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
        
        #Eliminar maestro (Desactivar usuario)
    # @transaction.atomic
    # def delete(self, request, *args, **kwargs):
    #     id_maestro = kwargs.get('id_maestro', None)
    #     if id_maestro:
    #         try:
    #             maestro = Maestros.objects.get(id=id_maestro)
    #             user = maestro.user
    #             user.is_active = 0
    #             user.save()
    #             return Response({"message":"Maestro con ID "+str(id_maestro)+" eliminado correctamente."},200)
    #         except Maestros.DoesNotExist:
    #             return Response({"message":"Maestro con ID "+str(id_maestro)+" no encontrado."},404)
    #     return Response({"message":"Se necesita el ID del maestro."},400)   