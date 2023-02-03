from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import DataMixin


class StudentMap(models.Model):
    """Модель с данными студента, связана с аккаунтом  User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    reiting = models.PositiveSmallIntegerField(_('Рейтинг'), default=0)
    start_study = models.DateTimeField(_('Начало обучения'), auto_now=True)
    graduate = models.BooleanField(_('Закончил курс'), default=False)

    class Meta:
        ordering = ['-reiting']

    def __str__(self):
        return f'Учебная карта {self.user.username}'


class PersonalMap(DataMixin, models.Model):
    """Модель с личными данными студента, связана с User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(_('О себе'), blank=True)

    class Institutions(models.IntegerChoices):
        """
        Выбор уровня образования.
        """
        NOCHOICE = 0, _('Не выбранно')
        NO = 1, _('Нет музыкального образования')
        SCHOOL = 2, _('Музыкальная школа')
        COLLEGE = 3, _('Среднее музыкальное образование')
        YNIVER = 4, _('Бакалавриат')
        MAG = 5, _('Магистратура')
        ASS = 6, _('Аспирантура')

    stady_level = models.PositiveSmallIntegerField(_('Уровень образования'),
                                                   choices=Institutions.choices,
                                                   default=0)

    class Course(models.IntegerChoices):
        """
        Выбор курса.
        """
        NOT = 0, _('Нет музыкального образования')
        ONE = 1, _('1й')
        THO = 2, _('2й')
        THREE = 3, _('3й')
        FOUR = 4, _('4й')
        FIVE = 5, _('5й')

    stady_course = models.PositiveSmallIntegerField(_('Курс'), choices=Course.choices, default=0)

    def get_stady_level(self):
        """Возвращает в шаблон уровень образования."""
        return self.data_stady_level[self.stady_level]

    def get_stady_course(self):
        """Возвращает в шаблон курс."""
        return self.data_course[self.stady_course]

    def __str__(self):
        return f'Персональная карта {self.user.get_full_name}'


class AboutSite(models.Model):
    """Модель информации о сайте, выходит на странице "О проекте"."""
    text = models.TextField(_('О сайте'), null=False, blank=False)
    page = models.PositiveSmallIntegerField(_('Страничка'))

    class Meta:
        ordering = ['page']

    def __str__(self):
        return f'О сайте страница - {self.page}'


class Feetback(models.Model):
    """Модель оценки сайта."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now=True)
    text = models.TextField(null=False, blank=False, verbose_name='Отзыв')
    stars = models.PositiveSmallIntegerField(verbose_name='Оценка')

    class Meta:
        ordering = ['-pub_time']
