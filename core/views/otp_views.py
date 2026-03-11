from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import OTP
from ..serializers import OTPSerializer, OTPVerifySerializer
from core.utils.pagination import CustomLimitOffsetPagination


class OTPListCreateView(APIView):
    pagination_class = CustomLimitOffsetPagination()

    def get(self, request):
        otps = OTP.objects.get_all_otps()
        paginator = self.pagination_class
        page = paginator.paginate_queryset(otps, request, view=self)
        serializer = OTPSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        try:
            serializer = OTPSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "data": serializer.errors,
                        "response_status": {
                            "success": False,
                            "code": 400,
                            "message": "Validation error",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            otp = OTP.objects.create_otp(serializer.validated_data)
            return Response(
                {
                    "data": OTPSerializer(otp).data,
                    "response_status": {
                        "success": True,
                        "code": 201,
                        "message": "OTP created successfully",
                    },
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "data": None,
                    "response_status": {
                        "success": False,
                        "code": 500,
                        "message": str(e),
                    },
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OTPVerifyView(APIView):
    """Verify an OTP and mark it as used. Use this instead of updating OTP."""

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "data": serializer.errors,
                    "response_status": {
                        "success": False,
                        "code": 400,
                        "message": "Validation error",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data
        otp_instance = OTP.objects.get_otp_by_code(
            otp_code=data["otp"],
            task_type=data.get("task_type"),
        )
        if not otp_instance:
            return Response(
                {
                    "data": None,
                    "response_status": {
                        "success": False,
                        "code": 400,
                        "message": "Invalid, expired, or already used OTP",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        OTP.objects.mark_otp_used(otp_instance)
        return Response(
            {
                "data": None,
                "response_status": {
                    "success": True,
                    "code": 200,
                    "message": "OTP verified successfully",
                },
            },
            status=status.HTTP_200_OK
        )


class OTPRetrieveDeleteView(APIView):
    """GET and DELETE only. No update — use verify endpoint to consume OTP."""

    def get(self, request, pk):
        otp = OTP.objects.get_otp_by_id(pk)
        if not otp:
            return Response(
                {
                    "data": None,
                    "response_status": {
                        "success": False,
                        "code": 404,
                        "message": "OTP not found",
                    },
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "data": OTPSerializer(otp).data,
                "response_status": {
                    "success": True,
                    "code": 200,
                    "message": "OTP fetched successfully",
                },
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        try:
            otp = OTP.objects.get_otp_by_id(pk)
            if not otp:
                return Response(
                    {
                        "data": None,
                        "response_status": {
                            "success": False,
                            "code": 404,
                            "message": "OTP not found",
                        },
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            OTP.objects.delete_otp(otp)
            return Response(
                {
                    "data": None,
                    "response_status": {
                        "success": True,
                        "code": 204,
                        "message": "OTP deleted successfully",
                    },
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {
                    "data": None,
                    "response_status": {
                        "success": False,
                        "code": 500,
                        "message": str(e),
                    },
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )