from rest_framework import serializers
from call.models import ClassOfStudent, Company, Student, Call
from django.utils import timezone

class CallSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ('student', 'present', 'date')

    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d')        

    def save(self, **kwargs):

        call = Call.objects.filter(student=self.validated_data.get('student'), date__date=timezone.now().date())

        if call.exists():
            call = call.first()
            call.present = self.validated_data.get('present')

        else:
            call = Call(
                student=self.validated_data.get('student'),
                present=self.validated_data.get('present')
            )

        call.save()

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

    def save(self, **kwargs):
        classOfStudent = ClassOfStudent.objects.filter(id=self.validated_data.get('classId')).first()
  
        student = Student(
            name=self.validated_data.get('name'),
            identification_number=self.validated_data.get('identification_number'),
            classOfStudent=classOfStudent
        )

        student.save()

        return student

class ClassOfStudentSerializer(serializers.ModelSerializer):

    company = serializers.IntegerField(
        write_only=True,
        required=True
    )

    class Meta:
        model = ClassOfStudent
        fields = ('id', 'name', 'company')

    def save(self, **kwargs):
        company = Company.objects.filter(id=self.validated_data.get('company')).first()

        classOfStudent = ClassOfStudent(
            company=company,
            name=self.validated_data.get('name')
        )

        classOfStudent.save()

        return classOfStudent
