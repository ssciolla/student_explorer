from advising.models import Student, Advisor, Cohort, StudentAdvisorRole
from rest_framework import serializers


class AdvisorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='advisor-detail',
                                               lookup_field='username')

    class Meta:
        model = Advisor
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'url')


class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('code', 'description', 'group')


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail',
                                               lookup_field='username')
    cohorts = CohortSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'cohorts', 'url')


# Serializations of the relationships between advisors and students.

class StudentAdvisorsSerializer(serializers.ModelSerializer):
    advisor = AdvisorSerializer(read_only=True)
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('role', 'advisor',)


class AdvisorStudentsSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('role', 'student',)