from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from firebase_admin import db
from datetime import datetime


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing"  # nombre de la colección en Firebase

    def get(self, request):
        """
        GET: devuelve todos los registros de la colección
        """
        ref = db.reference(self.collection_name)
        data = ref.get()

        return Response({
            "api": self.name,
            "timestamp": datetime.now(),
            "data": data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST: crea un nuevo registro
        """
        ref = db.reference(self.collection_name)

        new_data = {
            "content": request.data,
            "created_at": datetime.now().isoformat()
        }

        ref.push(new_data)

        return Response(
            {"message": "Registro creado correctamente"},
            status=status.HTTP_201_CREATED
        )


class LandingAPIItem(APIView):
    collection_name = "landing"

    def put(self, request, item_id):
        """
        PUT: reemplazo completo del recurso
        """
        ref = db.reference(f"{self.collection_name}/{item_id}")

        if ref.get() is None:
            return Response(
                {"message": f"No existe un elemento con id '{item_id}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.data:
            return Response(
                {"message": "PUT requiere un cuerpo completo de datos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_data = {
            "content": request.data,
            "updated_at": datetime.now().isoformat()
        }

        ref.set(new_data)

        return Response(
            {"message": "Actualización completa exitosa (PUT).", "data": new_data},
            status=status.HTTP_200_OK
        )

    def patch(self, request, item_id):
        """
        PATCH: actualización parcial
        """
        ref = db.reference(f"{self.collection_name}/{item_id}")

        if ref.get() is None:
            return Response(
                {"message": f"No existe un elemento con id '{item_id}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.data:
            return Response(
                {"message": "PATCH requiere al menos un campo a actualizar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        update_data = {
            "content": request.data,
            "updated_at": datetime.now().isoformat()
        }

        ref.update(update_data)

        return Response(
            {"message": "Actualización parcial exitosa (PATCH).", "data": update_data},
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        """
        DELETE: eliminación lógica
        """
        ref = db.reference(f"{self.collection_name}/{item_id}")

        if ref.get() is None:
            return Response(
                {"message": f"No existe un elemento con id '{item_id}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        ref.update({
            "is_active": False,
            "deleted_at": datetime.now().isoformat()
        })

        return Response(
            {"message": "Eliminación lógica exitosa (DELETE)."},
            status=status.HTTP_200_OK
        )
