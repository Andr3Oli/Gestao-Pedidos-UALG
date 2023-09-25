# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime, timezone
from authmanager.models import ProfessorUniversitario, Faculdade, Departamento, Funcionario


class Categoriasala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CategoriaSala'


class Unidadecurricular(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    periodo = models.CharField(db_column='Periodo', max_length=255, null=True)  # Field name made lowercase.
    instituicao = models.CharField(db_column='Instituicao', max_length=255, null=True)  # Field name made lowercase.
    tipo = models.ForeignKey('Tiporegencia', models.CASCADE, db_column='TiporegenciaID',
                             null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Unidadecurricular'



# class Conta(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
#     ativo = models.TextField(db_column='Ativo', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
#     tipocontaid = models.ForeignKey('Tipoconta', models.CASCADE, db_column='TipoContaID')  # Field name made lowercase.
#
#     def __str__(self):
#         return str(self.nome)
#
#     class Meta:
#         managed = True
#         db_table = 'Conta'

# class Funcionario(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
#     ativo = models.TextField(db_column='Ativo', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
#
#     def __str__(self):
#         return str(self.nome)
#
#     class Meta:
#         managed = True
#         db_table = 'Funcionario'


class Conta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    ativo = models.TextField(db_column='Ativo', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tipocontaid = models.ForeignKey('Tipoconta', models.CASCADE, db_column='TipoContaID')  # Field name made lowercase.
    idanoletivo = models.ForeignKey('AnoLetivo', models.CASCADE, db_column='AnoLetivoID', null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.nome)

    class Meta:
        managed = True
        db_table = 'Conta'


class Dsd(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    unidadecurricularid = models.ForeignKey('Unidadecurricular', models.CASCADE,
                                            db_column='UnidadeCurricularID')  # Field name made lowercase.
    contaid = models.ForeignKey(Conta, models.CASCADE, db_column='ContaID')  # Field name made lowercase.
    turma = models.CharField(db_column='Turma', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idanoletivo = models.ForeignKey('AnoLetivo', models.CASCADE, db_column='AnoLetivoID', null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DSD'
        constraints = [
            models.UniqueConstraint(fields=['unidadecurricularid', 'turma'], name='aula')
        ]


class TipoPedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.nome)

    class Meta:
        managed = True
        db_table = 'TipoPedido'


class Pedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    estado = models.ForeignKey('EstadoPedido', models.CASCADE, db_column='EstadoID')
    tipo = models.ForeignKey('TipoPedido', models.CASCADE, db_column='TipoPedidoID', null=True)
    responsavel = models.ForeignKey(Funcionario, models.CASCADE, db_column='Responsavel', blank=True, null=True)  # Field name made lowercase.
    docente = models.ForeignKey(ProfessorUniversitario, models.CASCADE, db_column='Docente', blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assunto = models.CharField(db_column='Assunto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datacriacao = models.DateTimeField(db_column='DataCriacao', blank=True, null=True, default=datetime.now)  # Field name made lowercase.
    dataatribuicao = models.DateTimeField(db_column='DataAtribuicao', blank=True, null=True)
    dataresolvido = models.DateTimeField(db_column='DataResolvido', blank=True, null=True)  # Field name made lowercase.
    dataalvo = models.DateField(db_column='DataAlvo', blank=True, null=True)  # Field name made lowercase.
    anoletivo = models.ForeignKey('AnoLetivo', models.CASCADE, db_column='AnoLetivo', blank=True, null=True)
    tempoespera = models.CharField(db_column='TempoEspera', max_length=255, blank=True, null=True)
    tempoprocesso = models.CharField(db_column='TempoProcesso', max_length=255, blank=True, null=True)
    motivocancelmento = models.TextField(db_column='Cancelamento', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Pedido'


class Pedidohorario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pedido_ptr_id = models.ForeignKey('Pedido', models.CASCADE, db_column='pedido_ptr_id', unique=False,
                                      null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)
    tipoalteracaohorarioid = models.ForeignKey('Tipoalteracaohorario', models.CASCADE,
                                               db_column='TipoAlteracaoHorarioID', null=True)  # Field name made lowercase.
    dataorigem = models.DateField(db_column='DataOrigem', blank=True, null=True)  # Field name made lowercase.
    horaorigem = models.TimeField(db_column='HoraOrigem', null=True)  # Field name made lowercase.
    datamudanca = models.DateField(db_column='DataMundança', blank=True, null=True)  # Field name made lowercase.
    horamudanca = models.TimeField(db_column='HoraMudanca', null=True)  # Field name made lowercase.
    acao = models.ForeignKey('Acao', models.CASCADE, db_column='AcaoID', null=True)
    
    
    def __str__(self):
        return "id: " + str(self.id) + " tipopei " + str(self.acao) + " tipoal " + str(self.tipoalteracaohorarioid)

    class Meta:
        managed = True
        db_table = 'PedidoHorario'


class RUC(models.Model):
    iduc = models.ForeignKey('Unidadecurricular', models.CASCADE,
                             db_column='UnidadeCurricularID')  # Field name made lowercase.
    idconta = models.ForeignKey('Conta', models.CASCADE, db_column='ContaID')  # Field name made lowercase.
    idanoletivo = models.ForeignKey('AnoLetivo', models.CASCADE, db_column='AnoLetivoID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'RUC'


class Tiporegencia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Tiporegencia'


class AnoLetivo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    datainicio = models.DateField(db_column='DataInicio', blank=True, null=True)  # Field name made lowercase.
    datafim = models.DateField(db_column='DataFim', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'AnoLetivo'

    def __str__(self):
        return self.nome


class Pedidooutros(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pedido_ptr_id = models.ForeignKey('Pedido', models.CASCADE, db_column='pedido_ptr_id', unique=False,
                                      null=True)  # Field name made lowercase.
    assunto_pedido = models.CharField(db_column='Assunto', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    descricao_pedido = models.CharField(db_column='Descricao', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase.
    dataalvo_pedido = models.DateField(db_column='DataAlvo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return "id: " + str(self.id) + " assunto: " + str(self.assunto_pedido)

    class Meta:
        managed = True
        db_table = 'PedidoOutros'


class Pedidosala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pedido_ptr_id = models.ForeignKey('Pedido', models.CASCADE, db_column='pedido_ptr_id', unique=False,
                                      null=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    alunosprevistos = models.IntegerField(db_column='AlunosPrevistos', blank=True,
                                          null=True)  # Field name made lowercase.
    horainicio = models.TimeField(db_column='HoraInicio', blank=True, null=True)  # Field name made lowercase.
    horafim = models.TimeField(db_column='HoraFim', blank=True, null=True)  # Field name made lowercase.
    tipopedidosalaid = models.ForeignKey('Tipopedidosala', models.CASCADE,
                                            db_column='TipoPedidoSalaID', null=True)  # Field name made lowercase.
    categoriasalaid = models.ForeignKey('Categoriasala', models.CASCADE,
                                        db_column='CategoriaSalaID',null=True)  # Field name made lowercase.
    acao = models.ForeignKey('Acao', models.CASCADE, db_column='AcaoID', null=True)

    class Meta:
        managed = True
        db_table = 'PedidoSala'

class Pedidouc(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pedido_ptr_id = models.ForeignKey('Pedido', models.CASCADE, db_column='pedido_ptr_id', unique=False,
                                      null=True)  # Field name made lowercase.
    unidadecurricularid = models.ForeignKey('Unidadecurricular', models.CASCADE,
                                            db_column='UnidadeCurricularID', null=True)  # Field name made lowercase.
    tipoturmaid = models.ForeignKey('TipoTurma', models.CASCADE, db_column='TipoTurmaID', null=True)
    assunto = models.CharField(db_column='Assunto', max_length=255, blank=True,
                               null=True)  # Field name made lowercase.
    acao = models.ForeignKey('Acao', models.CASCADE, db_column='AcaoID', null=True)

    def __str__(self):
        return "id: " + str(self.id) + " unidadecurricularid: " + str(self.unidadecurricularid) + "pedido_ptr_id: " + str(self.pedido_ptr_id)

    class Meta:
        managed = True
        db_table = 'Pedidouc'


class Acao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)

    def __str__(self):
        return "nome: " + str(self.nome)

    class Meta:
        managed = True
        db_table = 'TipoAcao'


class Sala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    edificio = models.CharField(db_column='Edificio', max_length=255)  # Field name made lowercase.
    sala = models.CharField(db_column='Sala', max_length=255)  # Field name made lowercase.
    lotacao = models.IntegerField(db_column='Lotacao', blank=True, null=True)  # Field name made lowercase.
    categoriasalaid = models.ForeignKey(Categoriasala, models.DO_NOTHING,
                                        db_column='CategoriaSalaID', null=True)  # Field name made lowercase.
    idanoletivo = models.ForeignKey('AnoLetivo', models.CASCADE, db_column='AnoLetivoID', null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'Sala'


class TipoTurma(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TipoTurma'


class Tipoalteracaohorario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TipoAlteracaoHorario'


class Tipoconta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TipoConta'


class Tipopedidohorario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TipoPedidoHorario'
        
class Tipopedidosala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TipoPedidoSala'

class EstadoPedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'EstadoPedido'
