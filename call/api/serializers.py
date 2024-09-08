from rest_framework import serializers
from call.models import ClassOfStudent, Company, Student

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'name', 'identification_number')

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
