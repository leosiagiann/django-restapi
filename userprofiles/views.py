from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile, DompetDigital


# Create your views here.
class UserProfileApiView(APIView):
    def listUserSaldoFormat(self, dataOld):
        data = list()
        for a in dataOld:
            temp = {
                'username': a.username,
                'age': a.age,
                'status': a.status,
                'saldo': a.dompetdigital.saldo
            }
            data.append(temp)
        return data

    def singleUserSaldoFormat(self, dataOld):
        data = {
            'username': dataOld.username,
            'age': dataOld.age,
            'status': dataOld.status,
            'saldo': dataOld.dompetdigital.saldo,
        }
        return data

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        user_profiles = UserProfile.objects.all()
        if username:
            try:
                user_profiles = user_profiles.get(username=username)
                return Response(self.singleUserSaldoFormat(user_profiles), status=status.HTTP_200_OK)
            except:
                return Response({'status': 'Username not found!'}, status=status.HTTP_200_OK)
        if user_profiles:
            return Response(self.listUserSaldoFormat(user_profiles), status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Data empty!'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        up = {
            'username': request.data.get('username'),
            'age': request.data.get('age'),
            'status': request.data.get('status'),
        }
        if not up['username'] or not up['age'] or not up['status']:
            return Response({'status': 'Failed to create user row'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            UserProfile.objects.get(username=up['username'])
            return Response({'status': 'Username already taken by another user!'}, status.HTTP_400_BAD_REQUEST)
        except:
            profile = UserProfile(username=up['username'], age=up['age'], status=up['status'])
            profile.save()
            dd = DompetDigital(userprofile=profile, saldo=0)
            dd.save()
        return Response(up, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return Response([{"info": "Username Must Be Included"}], status=status.HTTP_400_BAD_REQUEST)
        user_profiles = {
            'username': request.data.get('username'),
            'age': request.data.get('age'),
            'status': request.data.get('status'),
        }
        try:
            user_profiles_old = UserProfile.objects.get(username=username)
            if not user_profiles['username'] or not user_profiles['age'] or not user_profiles['status']:
                return Response({"status": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
            user_profiles_old.username = user_profiles.get('username')
            user_profiles_old.age = user_profiles.get('age')
            user_profiles_old.status = user_profiles.get('status')
            user_profiles_old.save()
            return Response(user_profiles, status=status.HTTP_200_OK)
        except:
            return Response({"status": "Username Not Found!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return Response({"status": "Username Must Be Included!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profiles_old = UserProfile.objects.get(username=username)
            user_profiles_old.delete()
            return Response({'status': 'User has been deleted!'}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "Username Not Found!"}, status=status.HTTP_400_BAD_REQUEST)


class DompetDigitalApiView(APIView):
    def listSaldoUserFormat(self, dataOld):
        data = list()
        for a in dataOld:
            temp = {
                'saldo': a.saldo,
                'user': {
                    'username': a.userprofile.username,
                    'age': a.userprofile.age,
                    'status': a.userprofile.status,
                },
            }
            data.append(temp)
        return data

    def singleSaldoUserFormat(self, dataOld):
        data = {
            'saldo': dataOld.saldo,
            'user': {
                'username': dataOld.userprofile.username,
                'age': dataOld.userprofile.age,
                'status': dataOld.userprofile.status,
            }
        }
        return data

    def get(self, request):
        username = request.GET.get('username')
        if username:
            try:
                data = DompetDigital.objects.get(userprofile__username=username)
                return Response(self.singleSaldoUserFormat(data), status=status.HTTP_200_OK)
            except:
                return Response({'status': 'Username not found!'}, status=status.HTTP_400_BAD_REQUEST)
        data = DompetDigital.objects.all()
        if data:
            return Response(self.listSaldoUserFormat(data), status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Data empty!'}, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"status": "Username Must Be Included!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = DompetDigital.objects.get(userprofile__username=username)
            data.saldo = data.saldo + request.data.get('saldo')
            data.save()
            return Response({"saldo update": data.saldo}, status.HTTP_200_OK)
        except:
            return Response({"status": "Username Profile Not Found!"}, status=status.HTTP_400_BAD_REQUEST)