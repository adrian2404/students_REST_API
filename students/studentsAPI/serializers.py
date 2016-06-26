from rest_framework import serializers
from studentsAPI.models.students import Student
from studentsAPI.models.groups import Group


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'middle_name', 'last_name',
                  'student_group', 'birthday', 'ticket', 'notes')


class GroupSerializer(serializers.ModelSerializer):

    students = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='students-detail')

    class Meta:
        model = Group
        fields = ('id', 'title', 'leader', 'notes', 'students')
