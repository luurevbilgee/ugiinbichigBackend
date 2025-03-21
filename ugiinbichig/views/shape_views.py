
from django.shortcuts import render
from ugiinbichig.models import Shape 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.serializers import ShapeSerializer
from django.contrib.auth.hashers import check_password
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)
class ShapeList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        shape_id = request.query_params.get("shapeID")
        try:
            if not shape_id:  # shape_id байхгүй эсвэл хоосон бол
                shapes = Shape.objects.all()
                
                if not shapes.exists():
                    return Response({
                        'status': 'error',
                        'message': 'Дүрс олдсонгүй',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)

                # ✅ ShapeSerializer-д `many=True` тохиргоотой serialize хийх
                shape_data = ShapeSerializer(shapes, many=True).data

                return Response({
                    'status': 'success',
                    'data': shape_data
                }, status=status.HTTP_200_OK)

            else:
                shape = Shape.objects.filter(shape_id=shape_id).first()

                if not shape:
                    return Response({
                        'status': 'error',
                        'message': 'Дүрс олдсонгүй',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)

                shape_data = ShapeSerializer(shape).data

                return Response({
                    'status': 'success',
                    'data': shape_data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching shape {shape_id}: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        shape_data = request.data
        try:
            human_ID = shape_data.get("human_ID")
            existing_shape = Shape.objects.filter(human_ID=human_ID).first()
            if existing_shape and existing_shape.human:
                return Response({
                    "status": "error",
                    "message": f"Shape {human_ID} already has a human assigned."
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShapeSerializer(data=shape_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "status": "success",
                "message": "Shapes created successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating shapes: {str(e)}")
            return Response({
                "status": "error",
                "message": "Internal server error",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, shape_id):
        try:
            shape = Shape.objects.filter(shape_id=shape_id).first()
            if not shape:
                return Response({
                    "status": "error",
                    "message": "Shape not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Хэрэв shape-д холбогдсон human байгаа эсэхийг шалгах
            if shape.human:
                return Response({
                    "status": "error",
                    "message": f"Shape {shape_id} already has a human assigned."
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShapeSerializer(shape, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Хүчингүй өгөгдөл",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error updating shape {shape_id}: {str(e)}")
            return Response({
                "status": "error",
                "message": "Дотоод серверийн алдаа",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)