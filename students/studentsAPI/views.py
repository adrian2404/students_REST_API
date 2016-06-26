from rest_framework.response import Response
from studentsAPI.models.students import Student
from studentsAPI.models.groups import Group
from django.db.models.deletion import ProtectedError
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import filters, viewsets, generics, status
from studentsAPI.serializers import StudentSerializer, GroupSerializer


def validate_leader(method_to_decorate):
    def wrapper(self, request, pk=0):
        leader = request.POST.get('leader')
        if bool(leader):
            student = Student.objects.get(pk=leader)
            if (student.student_group and student.student_group.id) != int(pk):
                return Response({'status': 'invalid student, choose a student from appropirate group'},
                                status=status.HTTP_400_BAD_REQUEST)
        return method_to_decorate(self, request, pk)
    return wrapper


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'students': reverse('students-list', request=request, format=format),
        'groups': reverse('groups-list', request=request, format=format)
    })


class StudentsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for students.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('student_group',)


class GroupsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @validate_leader
    def create(self, request, pk=None):
        """
        Adding some customization for validation leader field.
        """
        return super(GroupsViewSet, self).create(request)

    @validate_leader
    def update(self, request, pk):
        """
        Adding some customization for validation leader field.
        """
        return super(GroupsViewSet, self).update(request, pk)

    def destroy(self, request, pk):
        try:
            return super(GroupsViewSet, self).destroy(request, pk)
        except ProtectedError as error:
            return Response({'status': 'can\'t delete unless a student is in a group'},
                            status=status.HTTP_400_BAD_REQUEST)
