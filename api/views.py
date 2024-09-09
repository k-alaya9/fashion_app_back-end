import json
import smtplib
import ssl
import certifi
import subprocess
import os
from rest_framework.views import APIView
from rest_framework import viewsets , status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db import IntegrityError
from email.message import EmailMessage
from .serializers import UserSerializer,ClothesSerializer,SavedSerializer,ExperimentSerializer,FeedbackSerializer,HistorySerializer,BugReportSerializer,ChangePasswordSerializer,CategorySerializer
from .models import Clothes , Saved , Experiment ,History, Feedback,Category
from django.http import FileResponse, Http404


class AuthView(APIView):

    def post(self, request, *args, **kwargs):
        if 'register' in request.path:
            return self.register(request)
        elif 'logout' in request.path:
            return self.logout(request)

    def register (self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "user": serializer.data,
                "refresh_token": str(refresh),
                "access_token": access_token
            }, status=status.HTTP_201_CREATED)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):  
        permission_classes = [IsAuthenticated]
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request) 
            return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet (viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_user(self,request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ClothesListView(viewsets.ModelViewSet):
    queryset=Clothes.objects.all()
    serializer_class=ClothesSerializer
    permission_classes=[IsAuthenticated]

    # def get(self, request):
    #     item_id = request.query_params.get('id')  
    #     if item_id:
    #         return self.get_item(request, item_id)

    #     clothes = Clothes.objects.all()
    #     serializer = ClothesSerializer(clothes, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ClothesSerializer(data = request.data)

        if serializer.is_valid() :
            serializer.save()
            return Response (data=serializer.data, status=status.HTTP_200_OK)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # def get_item(self, request, pk):
    #     try:
    #         item = Clothes.objects.get(pk=pk)
    #     except Clothes.DoesNotExist:
    #         raise Http404
        
    #     serializer = ClothesSerializer(item)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
        

class SavedViewSet(viewsets.ModelViewSet):
    serializer_class=SavedSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):

        queryset = Saved.objects.all()
        user = self.request.user
        return queryset.filter(user=user)

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        
        clothes_id = data["clothes"]
        print(self.request.user)
        user = self.request.user

        if not clothes_id:
            return Response({"detail": "cloth_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            clothes=Clothes.objects.get(id=clothes_id)
            save = Saved.objects.create(clothes=clothes, user=user)
            return Response({"id": save.id}, status=status.HTTP_201_CREATED)
        except Clothes.DoesNotExist:
            return Response({"detail": "Clothes with the given id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"detail": "A saved item with this cloth_id already exists for the user."}, status=status.HTTP_400_BAD_REQUEST)

    def unsave(self, request, *args, **kwargs):

        clothes_id = kwargs.get('pk')
        user = self.request.user
        
        try:
            saved_item = Saved.objects.get(clothes_id=clothes_id, user=user)
            saved_item.delete()
            return Response({"detail": "Item unsaved successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Saved.DoesNotExist:
            return Response({"detail": "Saved item does not exist for the current user."}, status=status.HTTP_404_NOT_FOUND)


class BugReportView(APIView):

    serializer_class=BugReportSerializer
    permission_classes = [IsAuthenticated]

    def post (self, request):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            report = serializer.validated_data['report']
            user_email = request.user.email

            try:
             
                msg = EmailMessage()
                msg.set_content(report)
                msg['Subject'] = "Bug Report"
                msg['from'] = user_email
                msg['To'] = 'projectit2f@gmail.com'
                
                ssl_context = ssl.create_default_context(cafile=certifi.where())

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls(context=ssl_context)
                    server.login('boustatifarah@gmail.com', 'bceh xtjd gxgd srqa')
                    server.send_message(msg)

                return Response({"message": "Bug report sent successfully!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):

    serializer_class=ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        user = request.user
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({"message": "password changed successfully!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset=Experiment.objects.all()
    serializer_class=ExperimentSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request,*args, **kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        file1=request.data.get('user_photo_path')
        file2=request.data.get('clothes_photo_path')
        if serializer.is_valid():
            instance = serializer.save()
            #move images
            move = f'cmd.exe /C C: && cd C:\\Users\\Asus\\Desktop\\FashionAppBackend-main\\api && python move.py "C:\\Users\\ASUS\\Desktop\\FashionAppBackend-main\\static\\media\\media\\user_photo\\{file1}" "C:\\Users\\ASUS\\Desktop\\hd\\test\\image" "C:\\Users\\ASUS\\Desktop\\FashionAppBackend-main\\static\\media\\media\\cloths_photo\\{file2}" "C:\\Users\\ASUS\\Desktop\\hd\\test\\cloth"'
            subprocess.call(move, shell=True)
            
            # Resize and Rename Cloth|Pose
            resize_rename_cloth_pose = r'cmd.exe /C C: && cd C:\Users\Asus\Desktop\FashionAppBackend-main\api  && python resize.py'
            subprocess.call(resize_rename_cloth_pose, shell=True)
        
            #Open Pose 
            openpose = r'cmd.exe /C C: && cd C:\Users\ASUS\HR-VITON\Mediapipe-to-OpenPose-JSON\src && python mediapipe_JSON.py'
            subprocess.call(openpose, shell=True)

            #rename and move files
            rename = r'cmd.exe /C C: && cd C:\Users\Asus\Desktop\FashionAppBackend-main\api  && python rename.py'
            subprocess.call(rename, shell=True)

            #Human Parse
            human_parse = r'cmd.exe /C C: && cd C:\Users\ASUS\HR-VITON && python Self-Correction-Human-Parsing/simple_extractor.py  --dataset lip --model-restore Self-Correction-Human-Parsing/checkpoints/final.pth --input-dir C:/Users/ASUS/Desktop/hd/test/image/ --output-dir C:\Users\ASUS\Desktop\hd\test\image-parse-v3'
            subprocess.call(human_parse, shell=True)

            #Dense Pose
            densepose = r'cmd.exe /C C: && python C:/Users/ASUS/HR-VITON/detectron2/projects/DensePose/apply_net.py show C:/Users/ASUS/HR-VITON/detectron2/projects/DensePose/configs/densepose_rcnn_R_50_FPN_s1x.yaml https://dl.fbaipublicfiles.com/densepose/densepose_rcnn_R_50_FPN_s1x/165712039/model_final_162be9.pkl "C:/Users/ASUS/Desktop/hd/test/image/" dp_segm -v'
            subprocess.call(densepose,shell=True)

            #Cloth Mask
            cloth_mask = r'cmd.exe /C C: && cd C:\Users\Asus\Desktop\FashionAppBackend-main\api && python ClothMask.py'
            subprocess.call(cloth_mask,shell=True)

            # Human  Agnostic
            human_Agnostic=r'cmd.exe /C C: && cd C:\Users\Asus\Desktop\FashionAppBackend-main\api && python HumanAgnostic.py'
            subprocess.call(human_Agnostic,shell=True)

            #Parse Agnostic
            parse_Agnostic=r'cmd.exe /C C: && cd C:\Users\Asus\Desktop\FashionAppBackend-main\api && python ParseAgnostic.py'
            subprocess.call(parse_Agnostic,shell=True)

            #HR-VITON
            HR_VITON=r'cmd.exe /C C: && cd C:\Users\ASUS\HR-VITON && python test_generator.py --occlusion --cuda {True} --gpu_ids {0} --dataroot C:\Users\ASUS\Desktop\hd --data_list amma.txt --output_dir output/'
            subprocess.call(HR_VITON,shell=True)

            # Copy Output to HRVITON/OUTPUT
            copy_HRVITON_output_to_output = r'cmd.exe /C C: && cd C:\Users\Asus\Desktop\FashionAppBackend-main\api && python copy_HRVITION_Output.py'
            subprocess.call(copy_HRVITON_output_to_output, shell=True)


            instance_id = instance.id

            original_image_path = r"C:\Users\ASUS\Desktop\FashionAppBackend-main\static\media\media\model_photo\0_0.png"
            new_image_name = f"{instance_id}.png"
            new_image_path = os.path.join(
                r"C:\Users\ASUS\Desktop\FashionAppBackend-main\static\media\media\model_photo", new_image_name)


            os.rename(original_image_path, new_image_path)

            edit=Experiment.objects.get(pk=instance_id)
            print(edit)
            edit.models_photo_path = f"media/model_photo/{new_image_name}"
            print(edit.models_photo_path)
            print(edit)
            edit.save()
            print(edit)
            # serializer =ExperimentSerializer(edit)
            data=self.serializer_class(edit).data
            return Response(data, status=status.HTTP_201_CREATED)



class HistoryView(APIView):
    serializer_class=HistorySerializer
    permission_classes=[IsAuthenticated]

    def get(self,request):
        queryset =History.objects.all()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return Response(queryset, status=status.HTTP_201_CREATED)


class FeedBackViewSet(viewsets.ModelViewSet):
    queryset=Feedback.objects.all()
    serializer_class=FeedbackSerializer
    permission_classes=[IsAuthenticated] 


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticated] 

    @action(detail=True, methods=['get'], url_path='clothes')
    def clothes_by_category(self, request, pk):
        category = self.get_object()  
        clothes = Clothes.objects.filter(category=category)  
        serializer = ClothesSerializer(clothes, context={'request':request},many=True)  
        return Response(serializer.data,status=status.HTTP_200_OK) 


