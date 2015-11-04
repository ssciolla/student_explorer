from django.db import models
from django.conf import settings
import importlib

# Note that these model definitions are overriden below if
# settings.ADVISING_PACKAGE is set. This allows for customized models to
# accommodate external databases and their schema differences.


class Student(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    advisors = models.ManyToManyField('Advisor', through='StudentAdvisorRole')
    mentors = models.ManyToManyField('Mentor', through='StudentCohortMentor')
    cohorts = models.ManyToManyField('Cohort', through='StudentCohortMentor')
    class_sites = models.ManyToManyField('ClassSite',
                                         through='StudentClassSiteStatus')
    statuses = models.ManyToManyField('Status',
                                      through='StudentClassSiteStatus')

    def __unicode__(self):
        return self.username


class Advisor(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    students = models.ManyToManyField('Student', through='StudentAdvisorRole')

    def __unicode__(self):
        return self.username


class AdvisorRole(models.Model):
    code = models.CharField(max_length=4)
    description = models.CharField(max_length=30)

    def __unicode__(self):
        return self.description


class StudentAdvisorRole(models.Model):
    student = models.ForeignKey(Student)
    advisor = models.ForeignKey(Advisor)
    role = models.ForeignKey(AdvisorRole)

    def __unicode__(self):
        return '%s advises %s as %s' % (self.advisor, self.student, self.role)

    class Meta:
        unique_together = ('student', 'advisor', 'role')


class Cohort(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    group = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description


class Mentor(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=16)
    univ_id = models.CharField(max_length=11)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    students = models.ManyToManyField('Student', through='StudentCohortMentor')

    def __unicode__(self):
        return self.username


class StudentCohortMentor(models.Model):
    student = models.ForeignKey(Student)
    mentor = models.ForeignKey(Mentor)
    cohort = models.ForeignKey(Cohort)

    def __unicode__(self):
        return '%s is in the %s cohort' % (self.student, self.cohort)


class ClassSite(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.description


class Status(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    order = models.IntegerField()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ('order',)


class StudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return '%s has status %s in %s' % (self.student, self.status,
                                           self.class_site)


class Assignment(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.description


class StudentClassSiteAssignment(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    assignment = models.ForeignKey(Assignment)
    points_possible = models.FloatField(max_length=10)
    points_earned = models.FloatField(max_length=10)
    class_points_possible = models.FloatField(max_length=10, default=0)
    class_points_earned = models.FloatField(max_length=10, default=0)
    included_in_grade = models.CharField(max_length=1)
    grader_comment = models.CharField(max_length=4000, null=True)
    weight = models.FloatField(max_length=126)
    due_date = models.DateField()

    def __unicode__(self):
        return '%s has assignemnt %s in %s' % (self.student, self.assignment,
                                               self.class_site)

    @property
    def percentage(self):
        if self.points_possible == 0:
            return 0.0
        return self.points_earned / self.points_possible * 100

    @property
    def class_percentage(self):
        if self.class_points_possible == 0:
            return 0.0
        return self.class_points_earned / self.class_points_possible * 100

    class Meta:
        ordering = ('due_date',)

if hasattr(settings, 'ADVISING_PACKAGE'):
    # Override the definitions above if an alternate package has been
    # specified.

    advising_models_module = settings.ADVISING_PACKAGE + '.models'
    advising_models = importlib.import_module(advising_models_module)

    Student = advising_models.Student
    Advisor = advising_models.Advisor
    Mentor = advising_models.Mentor
    AdvisorRole = advising_models.AdvisorRole
    StudentAdvisorRole = advising_models.StudentAdvisorRole
    Cohort = advising_models.Cohort
    StudentCohortMentor = advising_models.StudentCohortMentor
    ClassSite = advising_models.ClassSite
    Status = advising_models.Status
    StudentClassSiteStatus = advising_models.StudentClassSiteStatus
    Assignment = advising_models.Assignment
    StudentClassSiteAssignment = advising_models.StudentClassSiteAssignment
