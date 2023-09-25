from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)


User = get_user_model()


class Reviews(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор_отзыва'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )

    mark = models.PositiveIntegerField(        
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Используйте число от 1 до 10!'
            ),
            MaxValueValidator(
                10,
                message='Используйте число от 1 до 10!'
            ),
        ]
    )

    public_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        db_index=True
    )

    #titles = models.ForeignKey()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:20]    
