from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    cargo = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Equipamento(models.Model):
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('EMPRESTADO', 'Emprestado'),
        ('FORNECIDO', 'Fornecido'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DISPONIVEL'
    )

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('FORNECIDO', 'Fornecido'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]

    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )
    data_emprestimo = models.DateField()
    data_prevista_devolucao = models.DateField()
    condicao_equipamento = models.TextField(
        blank=True,
        verbose_name='Condições do equipamento no empréstimo'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='EMPRESTADO'
    )
    data_devolucao = models.DateField(null=True, blank=True)
    observacao_devolucao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.equipamento} - {self.colaborador}'