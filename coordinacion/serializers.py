"""
Serializadores para convertir modelos Django a formato JSON
para ser consumidos por React
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

def serialize_empresa(empresa):
    """Serializar una empresa a formato JSON"""
    return {
        'id': empresa.id,
        'razon_social': empresa.razon_social,
        'nit': empresa.nit,
        'direccion': empresa.direccion,
        'telefono': empresa.telefono,
        'email': empresa.email,
        'ciudad': empresa.ciudad,
        'representante_nombre': empresa.representante_nombre,
        'representante_cargo': empresa.representante_cargo,
        'representante_email': empresa.representante_email,
        'representante_telefono': empresa.representante_telefono,
        'estado': empresa.estado,
        'fecha_registro': empresa.fecha_registro.isoformat() if empresa.fecha_registro else None,
        'fecha_aprobacion': empresa.fecha_aprobacion.isoformat() if empresa.fecha_aprobacion else None,
        'observaciones': empresa.observaciones or '',
        'aprobada_por': empresa.aprobada_por.nombre_completo if empresa.aprobada_por else None,
    }

def serialize_vacante(vacante):
    """Serializar una vacante a formato JSON"""
    return {
        'id': vacante.id,
        'titulo': vacante.titulo,
        'area_practica': vacante.area_practica,
        'descripcion': vacante.descripcion,
        'cantidad_cupos': vacante.cantidad_cupos,
        'cupos_ocupados': vacante.cupos_ocupados,
        'cupos_disponibles': vacante.cupos_disponibles,
        'programa_academico': vacante.programa_academico,
        'semestre_minimo': vacante.semestre_minimo,
        'horario': vacante.horario,
        'duracion_meses': vacante.duracion_meses,
        'estado': vacante.estado,
        'fecha_creacion': vacante.fecha_creacion.isoformat() if vacante.fecha_creacion else None,
        'fecha_publicacion': vacante.fecha_publicacion.isoformat() if vacante.fecha_publicacion else None,
        'empresa': {
            'id': vacante.empresa.id,
            'razon_social': vacante.empresa.razon_social,
            'nit': vacante.empresa.nit,
        },
        'creada_por': vacante.creada_por.nombre_completo if vacante.creada_por else None,
    }

def serialize_estudiante(estudiante):
    """Serializar un estudiante a formato JSON"""
    return {
        'id': estudiante.id,
        'codigo': estudiante.codigo,
        'nombre_completo': estudiante.nombre_completo,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'programa_academico': estudiante.programa_academico,
        'semestre': estudiante.semestre,
        'estado': estudiante.estado,
        'promedio_academico': float(estudiante.promedio_academico) if estudiante.promedio_academico else None,
        'fecha_registro': estudiante.fecha_registro.isoformat() if estudiante.fecha_registro else None,
    }

def serialize_postulacion(postulacion):
    """Serializar una postulación a formato JSON"""
    return {
        'id': postulacion.id,
        'estado': postulacion.estado,
        'fecha_postulacion': postulacion.fecha_postulacion.isoformat() if postulacion.fecha_postulacion else None,
        'fecha_respuesta': postulacion.fecha_respuesta.isoformat() if postulacion.fecha_respuesta else None,
        'observaciones': postulacion.observaciones or '',
        'estudiante': {
            'id': postulacion.estudiante.id,
            'codigo': postulacion.estudiante.codigo,
            'nombre_completo': postulacion.estudiante.nombre_completo,
            'programa_academico': postulacion.estudiante.programa_academico,
        },
        'vacante': {
            'id': postulacion.vacante.id,
            'titulo': postulacion.vacante.titulo,
            'empresa': postulacion.vacante.empresa.razon_social,
        },
        'postulado_por': postulacion.postulado_por.nombre_completo if postulacion.postulado_por else None,
    }

def serialize_practica(practica):
    """Serializar una práctica a formato JSON"""
    return {
        'id': practica.id,
        'estado': practica.estado,
        'fecha_inicio': practica.fecha_inicio.isoformat() if practica.fecha_inicio else None,
        'fecha_fin_estimada': practica.fecha_fin_estimada.isoformat() if practica.fecha_fin_estimada else None,
        'fecha_fin_real': practica.fecha_fin_real.isoformat() if practica.fecha_fin_real else None,
        'plan_aprobado': practica.plan_aprobado,
        'observaciones': practica.observaciones or '',
        'estudiante': {
            'id': practica.estudiante.id,
            'codigo': practica.estudiante.codigo,
            'nombre_completo': practica.estudiante.nombre_completo,
        },
        'empresa': {
            'id': practica.empresa.id,
            'razon_social': practica.empresa.razon_social,
        },
        'tutor_empresarial': {
            'id': practica.tutor_empresarial.id,
            'nombre_completo': practica.tutor_empresarial.nombre_completo,
        } if practica.tutor_empresarial else None,
        'docente_asesor': {
            'id': practica.docente_asesor.id,
            'nombre_completo': practica.docente_asesor.nombre_completo,
        } if practica.docente_asesor else None,
    }

def serialize_tutor(tutor):
    """Serializar un tutor empresarial a formato JSON"""
    return {
        'id': tutor.id,
        'nombre_completo': tutor.nombre_completo,
        'cargo': tutor.cargo,
        'email': tutor.email,
        'telefono': tutor.telefono,
        'activo': tutor.activo,
        'empresa': {
            'id': tutor.empresa.id,
            'razon_social': tutor.empresa.razon_social,
        },
    }

def serialize_docente(docente):
    """Serializar un docente asesor a formato JSON"""
    return {
        'id': docente.id,
        'nombre_completo': docente.nombre_completo,
        'email': docente.email,
        'telefono': docente.telefono,
        'especialidad': docente.especialidad,
        'activo': docente.activo,
    }

def serialize_sustentacion(sustentacion):
    """Serializar una sustentación a formato JSON"""
    return {
        'id': sustentacion.id,
        'fecha_programada': sustentacion.fecha_programada.isoformat() if sustentacion.fecha_programada else None,
        'lugar': sustentacion.lugar,
        'estado': sustentacion.estado,
        'calificacion': float(sustentacion.calificacion) if sustentacion.calificacion else None,
        'observaciones': sustentacion.observaciones or '',
        'practica': {
            'id': sustentacion.practica.id,
            'estudiante': sustentacion.practica.estudiante.nombre_completo,
        },
        'jurado_1': {
            'id': sustentacion.jurado_1.id,
            'nombre_completo': sustentacion.jurado_1.nombre_completo,
        } if sustentacion.jurado_1 else None,
        'jurado_2': {
            'id': sustentacion.jurado_2.id,
            'nombre_completo': sustentacion.jurado_2.nombre_completo,
        } if sustentacion.jurado_2 else None,
    }

def to_json(data):
    """Convertir datos a JSON de forma segura"""
    return json.dumps(data, cls=DjangoJSONEncoder)