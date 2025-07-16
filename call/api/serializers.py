from rest_framework import serializers
from call.models import ClassOfStudent, Company, Student, Call
from django.utils import timezone
from validate_docbr import CPF
import pytz

class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        fields = ('student', 'present', 'date')

    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d')        

    def save(self, **kwargs):
        student = self.validated_data.get('student')
        date = self.validated_data.get('date')
        present = self.validated_data.get('present')

        call = Call.objects.filter(student=student, date=date)

        if call.exists():
            # Atualiza diretamente no banco
            call.update(present=present)
            call = call.first()  # Obtém a instância atualizada

        else:
            call = Call.objects.create(student=student, present=present, date=date)

        return call

class StudentSerializer(serializers.ModelSerializer):

    present = serializers.BooleanField(required=False)
    date = serializers.DateField(required=False)
    classId = serializers.IntegerField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Student
        fields = ('id', 'name', 'identification_number', 'classId', 'present', 'date')

    def validate_identification_number(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError('CPF inválido')
        
        return value        

    def save(self, **kwargs):
        classOfStudent = ClassOfStudent.objects.filter(id=self.validated_data.get('classId')).first()
  
        student = Student(
            name=self.validated_data.get('name'),
            identification_number=self.validated_data.get('identification_number'),
            classOfStudent=classOfStudent
        )

        student.save()

        return student
    
class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'name', 'identification_number')

    def validate_identification_number(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError('CPF inválido')
        
        return value        

    def save(self):

        Student = self.instance.first()

        Student.name = self.validated_data.get('name', Student.name)
        Student.identification_number = self.validated_data.get('identification_number')

        Student.save()

        return Student

class ClassOfStudentSerializer(serializers.ModelSerializer):

    company = serializers.IntegerField(write_only=True, required=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = ClassOfStudent
        fields = ('id', 'name', 'company', 'student_count')

    def get_student_count(self, obj):
        return Student.objects.filter(classOfStudent=obj, is_active=True).count()

    def save(self, **kwargs):
        company = Company.objects.filter(id=self.validated_data.get('company')).first()
        
        classOfStudent = ClassOfStudent(
            company=company,
            name=self.validated_data.get('name')
        )
        classOfStudent.save()

        return classOfStudent
    
class ClassOfStudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassOfStudent
        fields = ('id', 'name')

    def save(self):

        Class = self.instance.first()

        Class.name = self.validated_data.get('name', Class.name)

        Class.save()

        return Class
    
class StudentDisableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'is_active')

    def save(self, **kwargs):

        Student = self.instance.first()

        if Student.is_active:
            Student.is_active = False
            Student.date_disable = timezone.now().astimezone(pytz.timezone('America/Sao_Paulo')).date()
            Student.save()

            return Student
        
        Student.is_active = True
        Student.date_disable = None

        Student.save()

        return Student
    
    
class ClassOfStudentDisableSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassOfStudent
        fields = ('id', 'is_active')

    def save(self, **kwargs):

        Class = self.instance.first()

        if Class.is_active:
            Class.is_active = False

            Class.save()

            return Class

        Class.is_active = True

        Class.save()

        return Class

