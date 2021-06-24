from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from subsidio.models import *

admin.site.site_header = 'SC19 | Adminsitración'

class TipoSubsidioAdmin (admin.ModelAdmin):
    list_display = ('nombre_tipo_subsidio',)

class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre_zona',)
    
class DepartamentoAdmin(admin.ModelAdmin):
    search_fields = ['nombre_departamento','nombre_zona']
    list_display = ('nombre_departamento','codigo_zona',)
    
class MunicipioAdmin(admin.ModelAdmin):
    search_fields = ['nombre_municipio','codigo_departamento']
    list_display = ('nombre_municipio','codigo_departamento',)
    list_filter = ['nombre_municipio', 'codigo_departamento']
    
class BeneficiarioAdmin(admin.ModelAdmin):
    search_fields = ['codigo_usuario','DUI','NIT']
    list_display = ('codigo_usuario','codigo_municipio','DUI','NIT',)
    
class BeneficiarioTipoSubsidioAdmin(admin.ModelAdmin):
    list_display = ('codigo_subsidio','codigo_beneficiario','cantidad','fecha',)
    

admin.site.register(TipoSubsidio, TipoSubsidioAdmin)
admin.site.register(Beneficiario, BeneficiarioAdmin)
admin.site.register(BeneficiarioTipoSubsidio,BeneficiarioTipoSubsidioAdmin)
admin.site.register(Zona, ZonaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.unregister(Group)