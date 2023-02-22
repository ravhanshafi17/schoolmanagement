from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from .serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework import status
from .permissions import *
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import generics





class SchoolSignupView(APIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user =serializer.save()
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            response = {"tokens":tokens,
                        "user":serializer.data}

            
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class AdminSignupView(APIView):
    authentication_classes=[JWTAuthentication]
    # serializer_class = AdminSerializer
    permission_classes = [SchoolCRUDPermission]

    def post(self,request):
        if request.user.is_school:
            username = self.request.data['username']
            email = self.request.data['email']
            password = self.request.data['password']
            user = User.objects.create_user(username, email, password,is_admin=True)
            name = request.data['name']
            address = request.data['address']
            phone_number = request.data['phone_number']
            school = School.objects.get(user =request.user)
            admin=Admin.objects.create(user=user,school=school,phone_number=phone_number,name=name,address=address)
            admin.save()
            response =  {'status': "sucess"}
            return Response(response)
        raise PermissionDenied()


class TeacherSignupView(APIView):
    authentication_classes=[JWTAuthentication]
    # serializer_class = AdminSerializer
    permission_classes = [AdminCRUDPermission]

    def post(self,request):
        if request.user.is_admin:
            username = self.request.data['username']
            email = self.request.data['email']
            password = self.request.data['password']
            user = User.objects.create_user(username, email, password,is_teacher=True)
            name = request.data['name']
            address = request.data['address']
            phone_number = request.data['phone_number']
            
            admin = Admin.objects.get(user =request.user)
            school = admin.school
            teacher=Teacher.objects.create(user=user,admin=admin,school=school,phone_number=phone_number,name=name,address=address)
            teacher.save()
            response =  {'status': "sucess"}
            return Response(response)
        raise PermissionDenied()

    # def post(self, request):
    #     # Only schools can create admins
    #     if not request.user.is_school:
    #         return Response({'error': 'Only schools can create admins'}, status=status.HTTP_403_FORBIDDEN)

    #     serializer = self.serializer_class(data=request.data, context={'request': request})


    #     if serializer.is_valid():
    #         admin = serializer.save(user=request.user)
    #         refresh = RefreshToken.for_user(admin.user)

    #         response_data = {
    #             'tokens': {
    #                 'refresh': str(refresh),
    #                 'access': str(refresh.access_token)
    #             },
    #             'admin': serializer.data
    #         }

    #         return Response(response_data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class QuestionBankCreateView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [AdminCRUDPermission]

    def post(self, request, format=None):
        if request.user.is_admin:
            admin = Admin.objects.get(user=request.user)
            name = request.data.get('name')
            subject = request.data.get('subject')
            classes = request.data.get('classes')
            question_bank = QuestionBank.objects.create(admin=admin, name=name, subject=subject, classes=classes)
            question_bank.save()
            return Response({'message': 'Question bank created successfully'})
        else:
            raise PermissionDenied()



class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        teacher = self.request.user.teacher
        admin = teacher.admin
        school = teacher.school
        serializer.save(teacher=teacher, admin=admin, school=school)

# class QuestionCreateView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]


#     def post(self, request, pk):
#         """
#         Create a new question for the specified question bank
#         """
#         if request.user.is_teacher:
#             teacher = request.user.teacher
#             question_bank = QuestionBank.objects.get(id=pk, admin__school=teacher.school)
#             serializer = QuestionSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(question=question_bank, teacher=teacher)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, pk):
    #     try:
    #         question_bank = QuestionBank.objects.get(id=pk)
    #     except QuestionBank.DoesNotExist:
    #         return Response({'error': 'Question bank does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    #     if request.user.is_teacher:
    #         data = request.data
    #         data['question'] = question_bank.id
    #         serializer = QuestionSerializer(teacher=request.user,data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)





class AdminListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_school:
            school = School.objects.get(user=request.user)
            admins = Admin.objects.filter(school=school)
            serializer = AdminSerializer(admins, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class TeacherListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_admin :
            admin = Admin.objects.get(user =request.user)
            school = admin.school
            teachers = Teacher.objects.filter(school=school)
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data)
        elif request.user.is_school:
            school = School.objects.get(user=request.user)
            teachers = Teacher.objects.filter(school=school)
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)



class admin_school_questionbanks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self ,request):
        if request.user.is_admin :
            admin = request.user.admin
            school = request.user.admin.school
            questionbanks = QuestionBank.objects.filter(admin=admin, admin__school=school)
            serializer = QuestionBankSerializer(questionbanks, many=True)
            return Response(serializer.data)
        elif request.user.is_school:
            school = request.user.school
            questionbanks = QuestionBank.objects.filter(admin__school=school)
            serializer = QuestionBankSerializer(questionbanks, many=True)
            return Response(serializer.data)
        elif request.user.is_teacher:
            teacher = request.user.teacher
            school = teacher.school
            questionbanks = QuestionBank.objects.filter(admin__school=school, admin=teacher.admin)
            serializer = QuestionBankSerializer(questionbanks, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


# class user_school_questions(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self ,request):
#         if request.user.is_teacher:
#             teacher = request.user.teacher
#             questions = Question.objects.filter(teacher=teacher)
#             serializer = QuestionSerializer(questions, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif request.user.school:
#             school = request.user.school
#             question = Question.objects.filter(teacher__admin__school=school)
#             serializer = QuestionSerializer(question, many=True)
#             return Response(serializer.data)
#         elif request.user.admin:
#             admin = request.user.admin
#             question = Question.objects.filter(teacher__admin=admin)
#             serializer = QuestionSerializer(question, many=True)
#             return Response(serializer.data)
#         else:
#  
#            return Response(status=status.HTTP_404_NOT_FOUND)
class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Question.objects.filter(school=user.teacher.school)
        elif hasattr(user, 'admin'):
            return Question.objects.filter(school=user.admin.school)
        elif hasattr(user, 'school'):
            return Question.objects.filter(school=user.school)
        else:
            return Question.objects.none()
        

class SchoolDetail(generics.RetrieveAPIView):
    serializer_class = SchoolSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'school'):
            return user.school
        else:
            raise PermissionDenied("You are not authorized to access this resource.")


# class QuestionGeneratorAPIView(APIView):
    
#     def get(self, request):
#         # Retrieve the question_type and marks_type from the request query params
#         question_type = request.query_params.get('question_type')
#         marks_type = request.query_params.get('marks_type')

#         # Retrieve the list of questions that match the provided criteria
#         question_generators = Question.objects.filter(question_type=question_type, marks=marks_type)

#         # Extract the questions from the question_generators
#         questions = [question_generator.question for question_generator in question_generators]

#         # Serialize the questions and return the response
#         serialized_questions = QuestionSerializer(questions, many=True)
#         return Response(serialized_questions.data)
# class QuestionGeneratorView(APIView):
#     serializer_class = QuestionGeneratorSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         question_type = serializer.validated_data['question_type']
#         marks_type = serializer.validated_data['marks_type']
#         questions = Question.objects.filter(question_type=question_type, marks=marks_type)
#         count = questions.count()
#         return Response({'count': count})

import random
from django.db.models import Sum
from collections import defaultdict
class RandomQuestionView(APIView):
    question_serializer_class = QuestionSerializer
    generator_serializer_class = QuestionGeneratorSerializer

    def post(self, request):
        serializer = self.generator_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        question_types = serializer.validated_data['question_type']
        marks_types = serializer.validated_data['marks_type']
        results = []

        for marks_type in marks_types:
            total_weightage = 0
            questions = []

            for question_type in question_types:
                qs = Question.objects.filter(question_type=question_type).exclude(id__in=[q.question.id for q in questions])
                if qs.exists():
                    total_weightage += sum(q.marks for q in qs)
                    questions += [QuestionGenerator(question=q, marks_type=q.marks) for q in qs]

            if total_weightage < marks_type:
                results.append({"error": "Total weightage of questions is less than the provided markstype"})
            else:
                selected_questions = []
                selected_weightage = 0
                selected_question_ids = []

                while selected_weightage != marks_type:
                    question = random.choice(questions)
                    if question.question.id in selected_question_ids:
                        continue
                    if question.marks_type + selected_weightage > marks_type:
                        continue
                    selected_questions.append(question.question)
                    selected_weightage += question.marks_type
                    selected_question_ids.append(question.question.id)

                serialized_questions = self.question_serializer_class(selected_questions, many=True).data
                results.append(serialized_questions)

        return Response(results)

    # def post(self, request):
    #     serializer = self.generator_serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     question_types = serializer.validated_data['question_type']
    #     marks_types = serializer.validated_data['marks_type']
    #     questions = Question.objects.filter(question_type__in=question_types)
    #     results = []

    #     for marks_type in marks_types:
    #         total_weightage = sum(q.marks for q in questions)
    #         if total_weightage < marks_type:
    #             results.append({"error": "Total weightage of questions is less than the provided markstype"})
    #         else:
    #             selected_questions = []
    #             selected_weightage = 0

    #             while selected_weightage != marks_type:
    #                 selected_questions = []
    #                 selected_weightage = 0

    #                 for question_type in question_types:
    #                     qs = questions.filter(question_type=question_type)
    #                     if qs.exists():
    #                         question = random.choice(qs)
    #                         selected_questions.append(question)
    #                         selected_weightage += question.marks

    #                 if selected_weightage >= marks_type:
    #                     break

    #             serialized_questions = self.question_serializer_class(selected_questions, many=True).data
    #             results.append(serialized_questions)

    #     return Response(results)

    # def post(self, request):
    #     serializer = self.generator_serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     question_types = serializer.validated_data['question_type']
    #     marks_types = serializer.validated_data['marks_type']
    #     results = []

    #     for marks_type in marks_types:
    #         total_weightage = 0
    #         questions = []

    #         for question_type in question_types:
    #             qs = Question.objects.filter(question_type=question_type).exclude(id__in=[q.question.id for q in questions])
    #             if qs.exists():
    #                 total_weightage += sum(q.marks for q in qs)
    #                 questions += [QuestionGenerator(question=q, marks_type=q.marks) for q in qs]

    #         if total_weightage < marks_type:
    #             results.append({"error": "Total weightage of questions is less than the provided markstype"})
    #         else:
    #             selected_questions = []
    #             selected_weightage = 0

    #             while selected_weightage != marks_type:
    #                 question = random.choice(questions)
    #                 if question.marks_type + selected_weightage > marks_type:
    #                     continue
    #                 selected_questions.append(question.question)
    #                 selected_weightage += question.marks_type

    #             serialized_questions = self.question_serializer_class(selected_questions, many=True).data
    #             results.append(serialized_questions)

    #     return Response(results)

    # def post(self, request):
    #     serializer = self.generator_serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     question_types = serializer.validated_data['question_type']
    #     marks_types = serializer.validated_data['marks_type']
    #     questions = Question.objects.filter(question_type__in=question_types)
    #     results = []

    #     for marks_type in marks_types:
    #         total_weightage = sum(q.marks for q in questions)
    #         if total_weightage < marks_type:
    #             results.append({"error": "Total weightage of questions is less than the provided markstype"})
    #         else:
    #             selected_questions = []
    #             selected_weightage = 0

    #             while selected_weightage != marks_type:
    #                 for question_type in question_types:
    #                     qs = questions.filter(question_type=question_type)
    #                     if qs.exists():
    #                         question = random.choice(qs)
    #                         selected_questions.append(question)
    #                         selected_weightage += question.marks

    #                 if selected_weightage > marks_type:
    #                     selected_questions = []
    #                     selected_weightage = 0

    #             serialized_questions = self.question_serializer_class(selected_questions, many=True).data
    #             results.append(serialized_questions)

    #     return Response(results)
class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        question_bank_id = self.kwargs['question_bank_id']
        return Question.objects.filter(question=question_bank_id)