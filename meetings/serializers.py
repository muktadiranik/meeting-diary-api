from rest_framework import serializers
from meetings.models import *


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def create(self, validated_data):
        instance = Member.objects.create(
            department=Department.objects.get(
                pk=self.context["department_pk"]
            ),
            full_name=validated_data["full_name"],
            primary_phone=validated_data["primary_phone"],
            secondary_phone=validated_data["secondary_phone"],
            email=validated_data["email"],
            address=validated_data["address"],
            designation=validated_data["designation"],
        )
        return instance


class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = '__all__'

    def create(self, validated_data):
        instance = Committee.objects.create(
            department=Department.objects.get(
                pk=self.context["department_pk"]
            ),
            title=validated_data["title"],
            description=validated_data["description"],
        )
        for i in validated_data["member"]:
            instance.member.add(i)
        return instance


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

    def create(self, validated_data):
        instance = Meeting.objects.create(
            department=Department.objects.get(
                pk=self.context["department_pk"]
            ),
            committee=Committee.objects.get(
                pk=self.context["committee_pk"]
            ),
            title=validated_data["title"],
            description=validated_data["description"],
            content=validated_data["content"],
            meeting_time=validated_data["meeting_time"],
        )
        for i in validated_data["invited_member"]:
            instance.invited_member.add(i)
        for i in validated_data["acknowledged_member"]:
            instance.acknowledged_member.add(i)
        for i in validated_data["attended_member"]:
            instance.attended_member.add(i)
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    committee_set = CommitteeSerializer(
        "committee_set", many=True, read_only=True)
    member_set = MemberSerializer("member_set", many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'
