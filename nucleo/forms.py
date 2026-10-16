from django import forms
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
            'data_emprestimo': forms.DateInput(attrs={'type': 'date'}),
            'data_prevista_devolucao': forms.DateInput(attrs={'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        dados = super().clean()
        status = dados.get('status')

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

        return dados