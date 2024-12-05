from core.models import PublishedModel
from django.db import models
from N1RV_Ann_A import settings

class Service(PublishedModel):
    title = models.CharField(("Название"), max_length=256)
    description = models.TextField(("Описание"))
    pub_date = models.DateTimeField(("Дата и время публикации услуги"),
                                    auto_now=False, auto_now_add=False,
                                    help_text="Если установить дату и \
время в будущем — можно делать отложенные публикации.")
    price = models.PositiveIntegerField(verbose_name='цена',)

    image = models.ImageField(verbose_name='Изображение',
                              null=True, blank=True)
    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class Hairdresser(PublishedModel):
    first_name = models.CharField(("Имя"), max_length=256)
    last_name = models.CharField(("Фамилия"), max_length=256)
    description = models.TextField(("Описание"))
    slug = models.SlugField(("Идентификатор"), unique=True,
                            help_text="Идентификатор страницы для URL; \
разрешены символы латиницы, цифры, дефис и подчёркивание.")

    image = models.ImageField(verbose_name='Изображение',
                              null=True, blank=True)

    services = models.ManyToManyField(
        Service,
        verbose_name="Оказываемые услуги"
    )

    class Meta:
        verbose_name = 'парикмахер'
        verbose_name_plural = 'Парикмахеры'

    def __str__(self):
        return self.slug

class OrderedServices(PublishedModel):
    hairdresser = models.ForeignKey(
        Hairdresser,
        on_delete=models.SET_NULL, null=True,
        verbose_name='парикмахер, оказывающий услугу',
        related_name='hairdresser',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='оказываемая услуга',
        related_name='service'
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Получатель услуги',
        on_delete=models.SET_NULL, null=True
    )

    serve_date = models.DateTimeField(("Дата и время оказания услуги"),
                                    auto_now=False, auto_now_add=False, editable=True,
                                    help_text="Необходимо установить время встречи не менее, чем за день до встречи.")


    payed = models.BooleanField(verbose_name='цена', default=False);

    comment = models.TextField(verbose_name='комментарий', null=True, blank=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'заказанная услуга'
        verbose_name_plural = 'Заказанные услуги'

    def __str__(self):
        return self.comment
