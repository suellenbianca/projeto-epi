from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Colaborador, Equipamento, Emprestimo
from .forms import ColaboradorForm, EquipamentoForm, EmprestimoForm
from django.utils import timezone
from django.contrib.auth import logout


def atualizar_status_equipamento(equipamento):
    emprestimos_ativos = Emprestimo.objects.filter(
        equipamento=equipamento,
        status__in=['EMPRESTADO', 'FORNECIDO']
    ).order_by('-data_emprestimo', '-id')

    if emprestimos_ativos.exists():
        equipamento.status = emprestimos_ativos.first().status
    else:
        ultimo_emprestimo = Emprestimo.objects.filter(
            equipamento=equipamento
        ).order_by('-data_emprestimo', '-id').first()

        if ultimo_emprestimo and ultimo_emprestimo.status in [
            'DANIFICADO', 'PERDIDO'
        ]:
            equipamento.status = ultimo_emprestimo.status
        else:
            equipamento.status = 'DISPONIVEL'

    equipamento.save(update_fields=['status'])



def home(request):
    colaboradores = Colaborador.objects.all().order_by('nome')
    return render(request, 'nucleo/index.html',
                  {'colaboradores': colaboradores})


def cadastrar_colaborador(request):
    form = ColaboradorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Colaborador cadastrado com sucesso!')
        return redirect('home')
    return render(request, 'nucleo/forms/form_colaborador.html',
                  {'form': form, 'titulo': 'Cadastrar colaborador'})


def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    form = ColaboradorForm(request.POST or None, instance=colaborador)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Colaborador atualizado!')
        return redirect('home')
    return render(request, 'nucleo/forms/form_colaborador.html',
                  {'form': form, 'titulo': 'Editar colaborador'})


def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if request.method == 'POST':
        try:
            colaborador.delete()
            messages.success(request, 'Colaborador excluído com sucesso!')
            return redirect('home')
        except Exception:
            messages.error(
                request,
                'Não foi possível excluir este colaborador, '
                'pois ele possui empréstimos vinculados. '
                'Verifique os registros antes de tentar novamente.'
            )
            return redirect('home')

    return render(request, 'nucleo/confirmar_exclusao.html', {
        'objeto': colaborador,
        'titulo': 'Excluir colaborador',
        'cancel_url': 'home'
    })


def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all().order_by('nome')
    return render(request, 'nucleo/equipamentos.html',
                  {'equipamentos': equipamentos})


def cadastrar_equipamento(request):
    form = EquipamentoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Equipamento cadastrado!')
        return redirect('listar_equipamentos')
    return render(request, 'nucleo/forms/form_equipamento.html', {'form': form})


def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    form = EquipamentoForm(request.POST or None, instance=equipamento)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Equipamento atualizado!')
        return redirect('listar_equipamentos')
    return render(request, 'nucleo/forms/form_equipamento.html', {'form': form})


def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == 'POST':
        try:
            equipamento.delete()
            messages.success(request, 'Equipamento excluído!')
        except Exception:
            messages.error(request, 'Não foi possível excluir este equipamento.')
        return redirect('listar_equipamentos')
    return render(request, 'nucleo/confirmar_exclusao.html', {
    'objeto': equipamento,
    'titulo': 'Excluir equipamento',
    'cancel_url': 'listar_equipamentos'
})


def listar_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related(
        'equipamento', 'colaborador'
    ).all().order_by('-data_emprestimo')

    # Indicadores gerais da tela
    total_disponiveis = Equipamento.objects.filter(
        status='DISPONIVEL'
    ).count()

    total_emprestados = Emprestimo.objects.filter(
        status='EMPRESTADO'
    ).count()

    total_vencidos = Emprestimo.objects.filter(
        status='EMPRESTADO',
        data_prevista_devolucao__lt=timezone.localdate()
    ).count()

    # Filtros da pesquisa
    busca = request.GET.get('busca', '').strip()
    equipamento = request.GET.get('equipamento', '').strip()
    status = request.GET.get('status', '')

    if busca:
        emprestimos = emprestimos.filter(
            colaborador__nome__icontains=busca
        )

    if equipamento:
        emprestimos = emprestimos.filter(
            equipamento__nome__icontains=equipamento
        )

    if status:
        emprestimos = emprestimos.filter(status=status)

    return render(request, 'nucleo/emprestimos.html', {
        'emprestimos': emprestimos,
        'busca': busca,
        'equipamento': equipamento,
        'status': status,
        'total_disponiveis': total_disponiveis,
        'total_emprestados': total_emprestados,
        'total_vencidos': total_vencidos,
    })


def cadastrar_emprestimo(request):
    form = EmprestimoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        emprestimo = form.save()
        atualizar_status_equipamento(emprestimo.equipamento)

        messages.success(request, 'Empréstimo registrado!')
        return redirect('listar_emprestimos')

    return render(
        request,
        'nucleo/forms/form_emprestimo.html',
        {'form': form}
    )



def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    equipamento_anterior = emprestimo.equipamento

    form = EmprestimoForm(
        request.POST or None,
        instance=emprestimo
    )

    if request.method == 'POST' and form.is_valid():
        emprestimo_atualizado = form.save()

        atualizar_status_equipamento(equipamento_anterior)

        if emprestimo_atualizado.equipamento_id != equipamento_anterior.id:
            atualizar_status_equipamento(
                emprestimo_atualizado.equipamento
            )

        messages.success(request, 'Empréstimo atualizado!')
        return redirect('listar_emprestimos')

    return render(
        request,
        'nucleo/forms/form_emprestimo.html',
        {'form': form}
    )



def excluir_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)

    if request.method == 'POST':
        equipamento = emprestimo.equipamento
        emprestimo.delete()

        atualizar_status_equipamento(equipamento)

        messages.success(request, 'Empréstimo excluído!')
        return redirect('listar_emprestimos')

    return render(request, 'nucleo/confirmar_exclusao.html', {
        'objeto': emprestimo,
        'titulo': 'Excluir empréstimo',
        'cancel_url': 'listar_emprestimos'
    })



def controle_epi(request):
    emprestimos = Emprestimo.objects.select_related(
        'equipamento', 'colaborador'
    ).all().order_by('-data_emprestimo')

    busca = request.GET.get('busca', '').strip()
    equipamento = request.GET.get('equipamento', '').strip()
    status = request.GET.get('status', '')

    if busca:
        emprestimos = emprestimos.filter(
            colaborador__nome__icontains=busca
        )

    if equipamento:
        emprestimos = emprestimos.filter(
            equipamento__nome__icontains=equipamento
        )

    if status:
        emprestimos = emprestimos.filter(status=status)

    return render(request, 'nucleo/controle_epi.html', {
        'emprestimos': emprestimos,
        'busca': busca,
        'equipamento': equipamento,
        'status': status,
    })


def perfil(request):
    return render(request, 'nucleo/perfil.html')


def sistema(request):
    return render(request, 'nucleo/sistema.html')


def sair(request):
    logout(request)
    return redirect('home')
