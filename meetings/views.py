from rest_framework.viewsets import ModelViewSet
from meetings.models import *
from meetings.serializers import *
from meetings.tasks import *
from rest_framework.filters import SearchFilter
# Create your views here.


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Department.objects.all().prefetch_related("committee_set").prefetch_related("member_set").order_by("-id")
        return Department.objects.filter(user=self.request.user.id).prefetch_related("committee_set").order_by("-id")


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ["full_name", "primary_phone",
                     "secondary_phone", "email",
                     "address", "designation"]

    def get_queryset(self):
        return Member.objects.filter(department=self.kwargs["department_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"]}


class CommitteeViewSet(ModelViewSet):
    serializer_class = CommitteeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Committee.objects.filter(department=self.kwargs["department_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"]}


class MeetingViewSet(ModelViewSet):
    serializer_class = MeetingSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description",
                     "content", "meeting_time"]

    def get_queryset(self):
        return Meeting.objects.filter(department=self.kwargs["department_pk"], committee=self.kwargs["committee_pk"]).order_by("-id")

    def get_serializer_context(self):
        return {"department_pk": self.kwargs["department_pk"], "committee_pk": self.kwargs["committee_pk"]}
