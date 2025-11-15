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

class AlumnosAll(generics.CreateAPIView):
    #Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener todos los alumnos
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active = 1).order_by("id")
        lista = AlumnosSerializer(alumnos, many=True).data
        return Response(lista, 200)
    
class AlumnosView(generics.CreateAPIView):
    #Obtener usuario por ID
    # Verifica que el usuario esté autenticado
    def get(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        alumno = get_object_or_404(Alumnos, id = request.GET.get("id"))
        alumno = AlumnosSerializer(alumno, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(alumno, 200)
    
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

            alumnos = Alumnos.objects.create(user=user,
                                            clave_alumno=request.data["clave_alumno"],
                                            telefono=request.data["telefono"],
                                            fecha_nacimiento=request.data["fecha_nacimiento"],
                                            rfc=request.data["rfc"].upper(),
                                            curp=request.data["curp"].upper(),
                                            edad=request.data["edad"],
                                            ocupacion=request.data["ocupacion"]                                                   
                                            )

            alumnos.save()

            return Response({"alumno_created_id": alumnos.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el alumno a actualizar
        alumno = get_object_or_404(Alumnos, id=request.data["id"])
        alumno.clave_alumno = request.data["clave_alumno"]
        alumno.telefono = request.data["telefono"]
        alumno.fecha_nacimiento = request.data["fecha_nacimiento"]
        alumno.rfc = request.data["rfc"]
        alumno.curp = request.data["curp"]
        alumno.edad = request.data["edad"]
        alumno.ocupacion = request.data["ocupacion"]
        alumno.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = alumno.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Alumno actualizado correctamente", "alumno": AlumnosSerializer(alumno).data}, 200)
        # return Response(user,200)
    # Eliminar admin con delete (Borrar realmente)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
        try:
            alumno.user.delete()
            return Response({"details":"Alumno eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
