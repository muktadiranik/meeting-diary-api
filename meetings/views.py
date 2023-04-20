from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from meetings.models import *
from meetings.serializers import *
from meetings.tasks import *
from rest_framework.filters import SearchFilter
# Create your views here.


class SearchAPIView(APIView):
    def get(self, request):
        if request.GET.get("search"):
            search = request.GET.get("search")
            if request.user.is_superuser:
                departments = Department.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search) |
                    Q(user__email__icontains=search) |
                    Q(user__username__icontains=search)
                ).order_by("-id")
                committees = Committee.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(department__title__icontains=search) |
                    Q(department__description__icontains=search) |
                    Q(department__user__first_name__icontains=search) |
                    Q(department__user__last_name__icontains=search) |
                    Q(department__user__email__icontains=search) |
                    Q(department__user__username__icontains=search)
                ).order_by("-id")
                members = Member.objects.filter(
                    Q(full_name__icontains=search) |
                    Q(primary_phone__icontains=search) |
                    Q(secondary_phone__icontains=search) |
                    Q(email__icontains=search) |
                    Q(address__icontains=search) |
                    Q(designation__icontains=search) |
                    Q(department__title__icontains=search) |
                    Q(department__description__icontains=search) |
                    Q(department__user__first_name__icontains=search) |
                    Q(department__user__last_name__icontains=search) |
                    Q(department__user__email__icontains=search) |
                    Q(department__user__username__icontains=search)
                ).order_by("-id")
                meetings = Meeting.objects.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(content__icontains=search) |
                    Q(department__title__icontains=search) |
                    Q(department__description__icontains=search) |
                    Q(department__user__first_name__icontains=search) |
                    Q(department__user__last_name__icontains=search) |
                    Q(department__user__email__icontains=search) |
                    Q(department__user__username__icontains=search)
                ).order_by("-id")
                return Response({
                    "departments": SimpleDepartmentSerializer(departments, many=True).data,
                    "committees": SimpleCommitteeSerializer(committees, many=True).data,
                    "members": SimpleMemberSerializer(members, many=True).data,
                    "meetings": SimpleMeetingSerializer(meetings, many=True).data,
                })
            departments = Department.objects.filter(user=request.user.id).filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__username__icontains=search)
            ).order_by("-id")
            committees = Committee.objects.filter(department__user_id=request.user.id).ffilter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(department__title__icontains=search) |
                Q(department__description__icontains=search) |
                Q(department__user__first_name__icontains=search) |
                Q(department__user__last_name__icontains=search) |
                Q(department__user__email__icontains=search) |
                Q(department__user__username__icontains=search)
            ).order_by("-id")
            members = Member.objects.filter(department__user_id=request.user.id).filter(
                Q(full_name__icontains=search) |
                Q(primary_phone__icontains=search) |
                Q(secondary_phone__icontains=search) |
                Q(email__icontains=search) |
                Q(address__icontains=search) |
                Q(designation__icontains=search) |
                Q(department__title__icontains=search) |
                Q(department__description__icontains=search) |
                Q(department__user__first_name__icontains=search) |
                Q(department__user__last_name__icontains=search) |
                Q(department__user__email__icontains=search) |
                Q(department__user__username__icontains=search)
            ).order_by("-id")
            meetings = Meeting.objects.filter(department__user_id=request.user.id).filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(content__icontains=search) |
                Q(department__title__icontains=search) |
                Q(department__description__icontains=search) |
                Q(department__user__first_name__icontains=search) |
                Q(department__user__last_name__icontains=search) |
                Q(department__user__email__icontains=search) |
                Q(department__user__username__icontains=search)
            ).order_by("-id")
            return Response({
                "departments": SimpleDepartmentSerializer(departments, many=True).data,
                "committees": SimpleCommitteeSerializer(committees, many=True).data,
                "members": SimpleMemberSerializer(members, many=True).data,
                "meetings": SimpleMeetingSerializer(meetings, many=True).data,
            })
        if request.user.is_superuser:
            departments = Department.objects.all().order_by("-id")
            committees = Committee.objects.all().order_by("-id")
            members = Member.objects.all().order_by("-id")
            meetings = Meeting.objects.all().order_by("-id")
            return Response({
                "departments": SimpleDepartmentSerializer(departments, many=True).data,
                "committees": SimpleCommitteeSerializer(committees, many=True).data,
                "members": SimpleMemberSerializer(members, many=True).data,
                "meetings": SimpleMeetingSerializer(meetings, many=True).data,
            })
        departments = Department.objects.filter(
            user=request.user.id).order_by("-id")
        committees = Committee.objects.filter(
            department__user_id=request.user.id).order_by("-id")
        members = Member.objects.filter(
            department__user_id=request.user.id).order_by("-id")
        meetings = Meeting.objects.filter(
            department__user_id=request.user.id).order_by("-id")
        return Response({
            "departments": SimpleDepartmentSerializer(departments, many=True).data,
            "committees": SimpleCommitteeSerializer(committees, many=True).data,
            "members": SimpleMemberSerializer(members, many=True).data,
            "meetings": SimpleMeetingSerializer(meetings, many=True).data,
        })


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
