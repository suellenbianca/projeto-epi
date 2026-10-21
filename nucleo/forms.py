from django import forms
from django.utils import timezone
from .models import Colaborador, Equipamento, Emprestimo


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = [
            'nome',
            'cpf',
            'cargo',
            'setor',
            'telefone',
            'email',
        ]
        labels = {
            'nome': 'Nome completo',
            'cpf': 'CPF (11 números)',
            'cargo': 'Cargo',
            'setor': 'Setor',
            'telefone': 'Telefone (11 números)',
            'email': 'E-mail',
        }
        widgets = {
            'cpf': forms.TextInput(attrs={
                'maxlength': '11',
                'minlength': '11',
                'inputmode': 'numeric',
                'pattern': '[0-9]{11}',
                'title': 'Digite exatamente 11 números, sem letras ou símbolos.',
                'placeholder': 'Digite 11 números',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 11)",
            }),
            'telefone': forms.TextInput(attrs={
                'maxlength': '11',
                'minlength': '11',
                'inputmode': 'numeric',
                'pattern': '[0-9]{11}',
                'title': 'Digite exatamente 11 números, incluindo o DDD.',
                'placeholder': 'Digite 11 números com DDD',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 11)",
            }),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError(
                'O CPF deve conter exatamente 11 números, sem pontos ou traços.'
            )
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not telefone.isdigit() or len(telefone) != 11:
            raise forms.ValidationError(
                'O telefone deve conter exatamente 11 números, incluindo o DDD.'
            )
        return telefone


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'descricao', 'status']
        labels = {
            'nome': 'Nome do equipamento',
            'descricao': 'Descrição',
            'status': 'Status',
        }


class EmprestimoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.edicao = kwargs.pop('edicao', False)
        super().__init__(*args, **kwargs)

        if not self.edicao:
            self.fields['status'].choices = [
                ('EMPRESTADO', 'Emprestado'),
                ('FORNECIDO', 'Fornecido'),
            ]
        else:
            campos_bloqueados = [
                'equipamento',
                'colaborador',
                'data_emprestimo',
                'data_prevista_devolucao',
            ]

            for campo in campos_bloqueados:
                self.fields[campo].disabled = True

    class Meta:
        model = Emprestimo
        fields = [
            'equipamento',
            'colaborador',
            'data_emprestimo',
            'data_prevista_devolucao',
            'condicao_equipamento',
            'status',
            'data_devolucao',
            'observacao_devolucao',
        ]
        labels = {
            'equipamento': 'Equipamento',
            'colaborador': 'Colaborador',
            'data_emprestimo': 'Data do empréstimo',
            'data_prevista_devolucao': 'Data prevista para devolução',
            'status': 'Status',
            'data_devolucao': 'Data da devolução ou ocorrência',
            'condicao_equipamento': 'Condição do equipamento',
            'observacao_devolucao': 'Observação',
        }
        widgets = {
            'data_emprestimo': forms.DateInput(
                 format='%Y-%m-%d',
                 attrs={'type': 'date'}
            ),
            'data_prevista_devolucao': forms.DateInput(
                 format='%Y-%m-%d',
                 attrs={'type': 'date'}
            ),
            'data_devolucao': forms.DateInput(
                 format='%Y-%m-%d',
                 attrs={'type': 'date'}
            ),
        }


    def clean(self):
     dados = super().clean()
     status = dados.get('status')
     equipamento = dados.get('equipamento')

     if status in ['DEVOLVIDO', 'DANIFICADO', 'PERDIDO']:
        if not dados.get('data_devolucao'):
            self.add_error(
                'data_devolucao',
                'Informe a data da devolução ou ocorrência.'
            )

        if not dados.get('observacao_devolucao'):
            self.add_error(
                'observacao_devolucao',
                'Preencha a observação para esse status.'
            )

     data_prevista = dados.get('data_prevista_devolucao')
 
     if (
          not self.edicao
          and data_prevista
          and data_prevista <= timezone.localdate()
    ):
         
         self.add_error(
          'data_prevista_devolucao',
          'A data prevista de devolução deve ser posterior à data de hoje.'
         )

     if equipamento and status in ['EMPRESTADO', 'FORNECIDO']:
        print("VALIDAÇÃO EXECUTADA:", equipamento, status)

        emprestimos_ativos = Emprestimo.objects.filter(
            equipamento=equipamento,
            status__in=['EMPRESTADO', 'FORNECIDO']
        )

        if self.instance and self.instance.pk:
            emprestimos_ativos = emprestimos_ativos.exclude(
                pk=self.instance.pk
            )

        if emprestimos_ativos.exists():
            self.add_error(
                'equipamento',
                'Este equipamento já possui um empréstimo ativo.'
            )

     return dados
