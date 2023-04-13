from rest_framework.viewsets import ModelViewSet
from meetings.models import *
from meetings.serializers import *

# Create your views here.


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Department.objects.all().prefetch_related("committee_set").prefetch_related("member_set").order_by("-id")
        return Department.objects.filter(user=self.request.user.id).prefetch_related("committee_set").order_by("-id")


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        return Member.objects.filter(department=self.kwargs["department_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"]}


class CommitteeViewSet(ModelViewSet):
    serializer_class = CommitteeSerializer

    def get_queryset(self):
        return Committee.objects.filter(department=self.kwargs["department_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"]}


class MeetingViewSet(ModelViewSet):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return Meeting.objects.filter(department=self.kwargs["department_pk"], committee=self.kwargs["committee_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"], "committee_pk": self.kwargs["committee_pk"]}
