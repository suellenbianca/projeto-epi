"""
URL configuration for epi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    # Página inicial e colaboradores
    path('', views.home, name='home'),

    path(
        'colaboradores/novo/',
        views.cadastrar_colaborador,
        name='cadastrar_colaborador'
    ),
    path(
        'colaboradores/<int:id>/editar/',
        views.editar_colaborador,
        name='editar_colaborador'
    ),
    path(
        'colaboradores/<int:id>/excluir/',
        views.excluir_colaborador,
        name='excluir_colaborador'
    ),

    # Equipamentos
    path(
        'equipamentos/',
        views.listar_equipamentos,
        name='listar_equipamentos'
    ),
    path(
        'equipamentos/novo/',
        views.cadastrar_equipamento,
        name='cadastrar_equipamento'
    ),
    path(
        'equipamentos/<int:id>/editar/',
        views.editar_equipamento,
        name='editar_equipamento'
    ),
    path(
        'equipamentos/<int:id>/excluir/',
        views.excluir_equipamento,
        name='excluir_equipamento'
    ),

    # Empréstimos e controle de EPI
    path(
        'emprestimos/',
        views.listar_emprestimos,
        name='listar_emprestimos'
    ),
    path(
        'emprestimos/novo/',
        views.cadastrar_emprestimo,
        name='cadastrar_emprestimo'
    ),
    path(
        'emprestimos/<int:id>/editar/',
        views.editar_emprestimo,
        name='editar_emprestimo'
    ),
    path(
        'emprestimos/<int:id>/excluir/',
        views.excluir_emprestimo,
        name='excluir_emprestimo'
    ),
    path('controle-epi/', 
         views.controle_epi, 
         name='controle_epi'
    ),
    path('perfil/', views.perfil, name='perfil'),
    path('sistema/', views.sistema, name='sistema'),
    path('sair/', views.sair, name='sair'),
]