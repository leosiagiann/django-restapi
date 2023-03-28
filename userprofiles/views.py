from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile, DompetDigital
import re
import numbers


# Create your views here.
class UserProfileApiView(APIView):
    def listUserSaldoFormat(self, dataOld):
        data = list()
        for a in dataOld:
            dompet = DompetDigital.objects.filter(user_profiles__username=a.username)
            list_dompet = list()
            for d in dompet:
                temp_list_dompet = {
                    'saldo': d.saldo,
                    'type': d.type
                }
                list_dompet.append(temp_list_dompet)
            temp = {
                'username': a.username,
                'age': a.age,
                'status': a.status,
                'dompet': list_dompet
            }
            data.append(temp)
        return data

    # ONE TO ONE RELATIONSHIP
    # def singleUserSaldoFormat(self, dataOld):
    #     data = {
    #         'username': dataOld.username,
    #         'age': dataOld.age,
    #         'status': dataOld.status,
    #         'saldo': dataOld.dompetdigital.saldo,
    #     }
    #     return data

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        user_profiles = UserProfile.objects.all()
        if username:
            try:
                user_profiles = user_profiles.filter(username=username)
                return Response(self.listUserSaldoFormat(user_profiles), status=status.HTTP_200_OK)
            except:
                return Response({'status': 'Username not found!'}, status=status.HTTP_200_OK)
        if user_profiles:
            return Response(self.listUserSaldoFormat(user_profiles), status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Data empty!'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.data.get('username') or not request.data.get('age') or not request.data.get('status'):
            return Response({'status': 'Failed to create user row!'}, status=status.HTTP_400_BAD_REQUEST)
        up = {
            'username': "".join(re.split("[^a-zA-Z0-9]*", request.data.get('username'))).lower(),
            'age': request.data.get('age'),
            'status': "".join(re.split("[^a-zA-Z]*", request.data.get('status'))).lower(),
        }
        if up['age'] < 0 or up['username'] == '' or up['status'] == '':
            return Response({'status': 'Failed to create user row, data invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            UserProfile.objects.get(username=up['username'])
            return Response({'status': 'Username already taken by another user!'}, status.HTTP_400_BAD_REQUEST)
        except:
            profile = UserProfile(username=up['username'], age=up['age'], status=up['status'])
            profile.save()
            # ONE TO ONE RELATIONSHIP
            # dd = DompetDigital(userprofile=profile, saldo=0)
            # dd.save()
        return Response(up, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        if not request.GET.get('username'):
            return Response([{"info": "Username Must Be Included"}], status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('username') or not request.data.get('age') or not request.data.get('status'):
            return Response({'status': 'Failed to update user row!'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.GET.get('username')
        up = {
            'username': "".join(re.split("[^a-zA-Z0-9]*", request.data.get('username'))).lower(),
            'age': request.data.get('age'),
            'status': "".join(re.split("[^a-zA-Z]*", request.data.get('status'))).lower(),
        }
        if up['age'] < 0 or up['username'] == '' or up['status'] == '':
            return Response({'status': 'Failed to update user row, data invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profiles_old = UserProfile.objects.get(username=username)
            try:
                UserProfile.objects.get(username=up.get('username'))
                return Response({'status': 'Username already taken by another user!'}, status.HTTP_400_BAD_REQUEST)
            except:
                user_profiles_old.username = up.get('username')
                user_profiles_old.age = up.get('age')
                user_profiles_old.status = up.get('status')
                user_profiles_old.save()
                return Response(up, status=status.HTTP_200_OK)
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
                    'username': a.user_profiles.username,
                    'age': a.user_profiles.age,
                    'status': a.user_profiles.status,
                },
            }
            data.append(temp)
        return data

    # ONE TO ONE RELATIONSHIP
    # def singleSaldoUserFormat(self, dataOld):
    #     data = {
    #         'saldo': dataOld.saldo,
    #         'user': {
    #             'username': dataOld.user_profiles.username,
    #             'age': dataOld.user_profiles.age,
    #             'status': dataOld.user_profiles.status,
    #         }
    #     }
    #     return data

    def get(self, request):
        username = request.GET.get('username')
        if username:
            try:
                data = DompetDigital.objects.filter(user_profiles__username=username)
                return Response(self.listSaldoUserFormat(data), status=status.HTTP_200_OK)
            except:
                return Response({'status': 'Username not found!'}, status=status.HTTP_400_BAD_REQUEST)
        data = DompetDigital.objects.all()
        if data:
            return Response(self.listSaldoUserFormat(data), status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Data empty!'}, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.data.get('username'):
            return Response({"status": "Username Must Be Included!"}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        if not request.data.get('saldo'):
            return Response({'status': 'Failed to create dompet digital row, data invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(request.data.get('saldo'), numbers.Number):
            return Response({"status": "Saldo must be number"}, status.HTTP_400_BAD_REQUEST)
        req = {
            'saldo': request.data.get('saldo'),
            'type': request.data.get('type')
        }
        if req['saldo'] < 0:
            return Response({"status": "Saldo must be greater than 0"}, status.HTTP_400_BAD_REQUEST)
        if req['type'] not in ['O', 'D', 'G']:
            return Response({"status": "Type Choises only O, G, OR D"}, status.HTTP_400_BAD_REQUEST)
        try:
            data = DompetDigital.objects.get(user_profiles__username=username, type=req['type'])
            data.saldo = data.saldo + request.data.get('saldo')
            data.save()
            return Response({"current saldo": data.saldo}, status.HTTP_201_CREATED)
        except:
            try:
                user = UserProfile.objects.get(username=username)
                data = DompetDigital(user_profiles=user, saldo=req['saldo'], type=req['type'])
                data.save()
                return Response(req, status.HTTP_200_OK)
            except:
                return Response({"status": "Username Not Found!"}, status=status.HTTP_400_BAD_REQUEST)