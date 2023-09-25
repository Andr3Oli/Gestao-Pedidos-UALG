from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Faculdade(models.Model):
    nome = models.CharField(db_column='nome', max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.nome)
    
    class Meta:
        managed = True
        db_table = 'Faculdade'


class Departamento(models.Model):
    nome = models.CharField(db_column='nome', max_length=255, blank=False, null=False)
    faculdadeid = models.ForeignKey('Faculdade', models.CASCADE)
    
    def __str__(self):
        return str(self.nome)
    

    class Meta:
        managed = True
        db_table = 'Departamento'


class Utilizador(User):
    contacto = PhoneNumberField(max_length=20, blank=False, null=False)
    valido = models.CharField(max_length=255, blank=False, null=False)

    def getProfiles(self):
        type = ''
        if ProfessorUniversitario.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='ProfessorUniversitario')
        if Funcionario.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Funcionario')
        return type

    def concat(self, type, string):
        if type == '':
            type = string
        else:
            type += ', ' + string
        return type

    @property
    def firstProfile(self):
        return self.getProfiles().split(' ')[0]

    def getUser(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name="Funcionario").exists():
            result = Funcionario.objects.get(id=self.id)
        elif user.groups.filter(name="ProfessorUniversitario").exists():
            result = ProfessorUniversitario.objects.get(id=self.id)
        else:
            result = None
        return result

    def getProfile(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name="ProfessorUniversitario").exists():
            result = "ProfessorUniversitario"
        elif user.groups.filter(name="Funcionario").exists():
            result = "Funcionario"
        else:
            result = None
        return result

    # def emailValidoUO(self, uo):
    #     user = User.objects.get(email=self.email)
    #     if user.groups.filter(name="ProfessorUniversitario").exists():
    #         utilizador = ProfessorUniversitario.objects.get(email=self.email)
    #     elif user.groups.filter(name="Funcionario").exists():
    #         utilizador = Funcionario.objects.get(email=self.email)
    #     else:
    #         return False
    #     if utilizador.faculdade == uo:
    #         return True
    #     else:
    #         return False

    def emailValidoParticipante(self):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name="Administrador").exists():
            return True
        else:
            return False

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        managed = True
        db_table = 'Utilizador'


class ProfessorUniversitario(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.ForeignKey('Faculdade', models.CASCADE)

    departamento = models.ForeignKey('Departamento', models.CASCADE)

    def __str__(self):
        return str(super().full_name)
        #return str(self.gabinete) + ' ' + str(self.faculdade) + ' ' + str(self.departamento)

    class Meta:
        managed = True
        db_table = 'ProfessorUniversitario'


class Funcionario(Utilizador):
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=False, null=False)
    faculdade = models.ForeignKey('Faculdade', models.CASCADE)

    def __str__(self):
        return str(super().full_name)
        #return str(self.gabinete) + ' ' + str(self.faculdade)

    class Meta:
        managed = True
        db_table = 'Funcionario'
