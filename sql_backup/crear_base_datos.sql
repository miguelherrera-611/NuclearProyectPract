-- ========================================================================================
-- SISTEMA DE PRÁCTICAS EMPRESARIALES — RESPALDO EXACTO DE db.sqlite3
-- ========================================================================================
-- Proyecto  : DjangoProject  (Django 5.2.7)
-- Motor     : MySQL / MariaDB  (XAMPP)
-- Charset   : utf8mb4 / utf8mb4_unicode_ci
-- Fuente    : exportado directamente desde db.sqlite3  (2026-05-05)
-- ========================================================================================
--
-- ╔══════════════════════════════════════════════════════════════════════════════════╗
-- ║  INSTRUCCIONES                                                                 ║
-- ╠══════════════════════════════════════════════════════════════════════════════════╣
-- ║  1. Importa este archivo en phpMyAdmin → pestaña SQL → Ejecutar               ║
-- ║     O por consola:  mysql -u root -p < crear_base_datos.sql                   ║
-- ║                                                                                ║
-- ║  2. Cambia DATABASES en config/settings.py a MySQL:                           ║
-- ║       'ENGINE': 'django.db.backends.mysql'                                    ║
-- ║       'NAME':   'practicas_empresariales'                                     ║
-- ║       'USER':   'root'                                                        ║
-- ║       'PASSWORD': ''                                                           ║
-- ║       'HOST':   'localhost'                                                    ║
-- ║       'PORT':   '3306'                                                        ║
-- ║     Instala el driver:  pip install mysqlclient                               ║
-- ║                                                                                ║
-- ║  3. Después de importar ejecuta:                                               ║
-- ║       python manage.py migrate --fake                                         ║
-- ║                                                                                ║
-- ╠══════════════════════════════════════════════════════════════════════════════════╣
-- ║  CONTRASEÑAS — usa las mismas que tenías antes.                               ║
-- ║  Los hashes son EXACTOS del db.sqlite3 original.                              ║
-- ║  Si olvidaste alguna contraseña:                                               ║
-- ║    python manage.py changepassword <username>                                 ║
-- ║                                                                                ║
-- ║  CUENTAS EXISTENTES:                                                          ║
-- ║    admin       (superusuario)                                                  ║
-- ║    coordinador (superusuario)                                                  ║
-- ║    coord001    (coordinador con perfil completo)                               ║
-- ║    docente001, docente002, docente003                                          ║
-- ║    est001 … est008                                                             ║
-- ║    tutor001                                                                    ║
-- ╚══════════════════════════════════════════════════════════════════════════════════╝

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

-- ========================================================================================
-- 1. CREAR BASE DE DATOS
-- ========================================================================================
CREATE DATABASE IF NOT EXISTS `practicas_empresariales`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `practicas_empresariales`;

-- ========================================================================================
-- 2. TABLAS DEL SISTEMA DJANGO
-- ========================================================================================

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id`        int          NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model`     varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`, `model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id`              bigint       NOT NULL AUTO_INCREMENT,
  `name`            varchar(255) NOT NULL,
  `content_type_id` int          NOT NULL,
  `codename`        varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_uniq` (`content_type_id`, `codename`),
  CONSTRAINT `auth_permission_content_type_id_fk`
    FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id`   bigint       NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id`            bigint NOT NULL AUTO_INCREMENT,
  `group_id`      bigint NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_uniq` (`group_id`, `permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_fk`
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissions_permission_id_fk`
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id`           bigint       NOT NULL AUTO_INCREMENT,
  `password`     varchar(128) NOT NULL,
  `last_login`   datetime(6)  DEFAULT NULL,
  `is_superuser` tinyint(1)   NOT NULL,
  `username`     varchar(150) NOT NULL,
  `first_name`   varchar(150) NOT NULL,
  `last_name`    varchar(150) NOT NULL,
  `email`        varchar(254) NOT NULL,
  `is_staff`     tinyint(1)   NOT NULL,
  `is_active`    tinyint(1)   NOT NULL,
  `date_joined`  datetime(6)  NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id`       bigint NOT NULL AUTO_INCREMENT,
  `user_id`  bigint NOT NULL,
  `group_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_uniq` (`user_id`, `group_id`),
  CONSTRAINT `auth_user_groups_group_id_fk`
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id`            bigint NOT NULL AUTO_INCREMENT,
  `user_id`       bigint NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_uniq` (`user_id`, `permission_id`),
  CONSTRAINT `auth_user_user_permissions_permission_id_fk`
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id`              int          NOT NULL AUTO_INCREMENT,
  `action_time`     datetime(6)  NOT NULL,
  `object_id`       longtext     DEFAULT NULL,
  `object_repr`     varchar(200) NOT NULL,
  `action_flag`     smallint     NOT NULL,
  `change_message`  longtext     NOT NULL,
  `content_type_id` int          DEFAULT NULL,
  `user_id`         bigint       NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `django_admin_log_content_type_id_fk`
    FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id`      bigint       NOT NULL AUTO_INCREMENT,
  `app`     varchar(255) NOT NULL,
  `name`    varchar(255) NOT NULL,
  `applied` datetime(6)  NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key`  varchar(40) NOT NULL,
  `session_data` longtext    NOT NULL,
  `expire_date`  datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_idx` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ========================================================================================
-- 3. TABLAS DE LA APLICACIÓN
-- ========================================================================================

CREATE TABLE IF NOT EXISTS `coordinacion_coordinador` (
  `id`              bigint       NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(200) NOT NULL,
  `email`           varchar(254) NOT NULL,
  `telefono`        varchar(20)  DEFAULT NULL,
  `foto_perfil`     varchar(100) DEFAULT NULL,
  `fecha_creacion`  datetime(6)  NOT NULL,
  `activo`          tinyint(1)   NOT NULL DEFAULT 1,
  `user_id`         bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `coordinacion_coordinador_user_id_uniq` (`user_id`),
  CONSTRAINT `coordinacion_coordinador_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_empresa` (
  `id`                     bigint       NOT NULL AUTO_INCREMENT,
  `razon_social`           varchar(300) NOT NULL,
  `nit`                    varchar(20)  NOT NULL,
  `direccion`              varchar(300) NOT NULL,
  `telefono`               varchar(20)  NOT NULL,
  `email`                  varchar(254) NOT NULL,
  `ciudad`                 varchar(100) NOT NULL,
  `representante_nombre`   varchar(200) NOT NULL,
  `representante_cargo`    varchar(100) NOT NULL,
  `representante_email`    varchar(254) NOT NULL,
  `representante_telefono` varchar(20)  NOT NULL,
  `camara_comercio`        varchar(100) DEFAULT NULL,
  `rut`                    varchar(100) DEFAULT NULL,
  `estado`                 varchar(20)  NOT NULL DEFAULT 'PENDIENTE',
  `fecha_registro`         datetime(6)  NOT NULL,
  `fecha_aprobacion`       datetime(6)  DEFAULT NULL,
  `observaciones`          longtext     DEFAULT NULL,
  `aprobada_por_id`        bigint       DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nit` (`nit`),
  KEY `coordinacion_empresa_aprobada_por_id_idx` (`aprobada_por_id`),
  CONSTRAINT `coordinacion_empresa_aprobada_por_id_fk`
    FOREIGN KEY (`aprobada_por_id`) REFERENCES `coordinacion_coordinador` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_docenteasesor` (
  `id`              bigint       NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(200) NOT NULL,
  `cedula`          varchar(20)  DEFAULT NULL,
  `email`           varchar(254) NOT NULL,
  `telefono`        varchar(20)  NOT NULL,
  `especialidad`    varchar(200) NOT NULL,
  `foto_perfil`     varchar(100) DEFAULT NULL,
  `activo`          tinyint(1)   NOT NULL DEFAULT 1,
  `fecha_registro`  datetime(6)  NOT NULL,
  `user_id`         bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `coordinacion_docenteasesor_user_id_uniq` (`user_id`),
  CONSTRAINT `coordinacion_docenteasesor_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_tutorempresarial` (
  `id`              bigint       NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(200) NOT NULL,
  `cargo`           varchar(100) NOT NULL,
  `email`           varchar(254) NOT NULL,
  `telefono`        varchar(20)  NOT NULL,
  `foto_perfil`     varchar(100) DEFAULT NULL,
  `activo`          tinyint(1)   NOT NULL DEFAULT 1,
  `fecha_registro`  datetime(6)  NOT NULL,
  `empresa_id`      bigint       NOT NULL,
  `user_id`         bigint       DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coordinacion_tutorempresarial_user_id_uniq` (`user_id`),
  KEY `coordinacion_tutorempresarial_empresa_id_idx` (`empresa_id`),
  CONSTRAINT `coordinacion_tutorempresarial_empresa_id_fk`
    FOREIGN KEY (`empresa_id`) REFERENCES `coordinacion_empresa` (`id`),
  CONSTRAINT `coordinacion_tutorempresarial_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_estudiante` (
  `id`                 bigint       NOT NULL AUTO_INCREMENT,
  `codigo`             varchar(20)  NOT NULL,
  `nombre_completo`    varchar(200) NOT NULL,
  `email`              varchar(254) NOT NULL,
  `telefono`           varchar(20)  NOT NULL,
  `programa_academico` varchar(200) NOT NULL,
  `semestre`           int          NOT NULL,
  `foto_perfil`        varchar(100) DEFAULT NULL,
  `hoja_vida`          varchar(100) DEFAULT NULL,
  `estado`             varchar(20)  NOT NULL DEFAULT 'APTO',
  `promedio_academico` decimal(3,2) DEFAULT NULL,
  `fecha_registro`     datetime(6)  NOT NULL,
  `user_id`            bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  UNIQUE KEY `coordinacion_estudiante_user_id_uniq` (`user_id`),
  CONSTRAINT `coordinacion_estudiante_user_id_fk`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_vacante` (
  `id`                     bigint       NOT NULL AUTO_INCREMENT,
  `titulo`                 varchar(300) NOT NULL,
  `area_practica`          varchar(200) NOT NULL,
  `descripcion`            longtext     NOT NULL,
  `cantidad_cupos`         int          NOT NULL DEFAULT 1,
  `cupos_ocupados`         int          NOT NULL DEFAULT 0,
  `programa_academico`     varchar(200) NOT NULL,
  `semestre_minimo`        int          NOT NULL,
  `habilidades_requeridas` longtext     DEFAULT NULL,
  `horario`                varchar(200) NOT NULL,
  `duracion_meses`         int          NOT NULL DEFAULT 6,
  `estado`                 varchar(20)  NOT NULL DEFAULT 'DISPONIBLE',
  `fecha_creacion`         datetime(6)  NOT NULL,
  `fecha_publicacion`      datetime(6)  DEFAULT NULL,
  `fecha_cierre`           datetime(6)  DEFAULT NULL,
  `empresa_id`             bigint       NOT NULL,
  `creada_por_id`          bigint       NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coordinacion_vacante_empresa_id_idx` (`empresa_id`),
  KEY `coordinacion_vacante_creada_por_id_idx` (`creada_por_id`),
  CONSTRAINT `coordinacion_vacante_empresa_id_fk`
    FOREIGN KEY (`empresa_id`) REFERENCES `coordinacion_empresa` (`id`),
  CONSTRAINT `coordinacion_vacante_creada_por_id_fk`
    FOREIGN KEY (`creada_por_id`) REFERENCES `coordinacion_coordinador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_postulacion` (
  `id`                bigint      NOT NULL AUTO_INCREMENT,
  `estado`            varchar(20) NOT NULL DEFAULT 'POSTULADO',
  `fecha_postulacion` datetime(6) NOT NULL,
  `fecha_respuesta`   datetime(6) DEFAULT NULL,
  `observaciones`     longtext    DEFAULT NULL,
  `estudiante_id`     bigint      NOT NULL,
  `postulado_por_id`  bigint      NOT NULL,
  `vacante_id`        bigint      NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coordinacion_postulacion_vacante_estudiante_uniq` (`vacante_id`, `estudiante_id`),
  KEY `coordinacion_postulacion_estudiante_id_idx` (`estudiante_id`),
  KEY `coordinacion_postulacion_postulado_por_id_idx` (`postulado_por_id`),
  CONSTRAINT `coordinacion_postulacion_estudiante_id_fk`
    FOREIGN KEY (`estudiante_id`) REFERENCES `coordinacion_estudiante` (`id`),
  CONSTRAINT `coordinacion_postulacion_postulado_por_id_fk`
    FOREIGN KEY (`postulado_por_id`) REFERENCES `coordinacion_coordinador` (`id`),
  CONSTRAINT `coordinacion_postulacion_vacante_id_fk`
    FOREIGN KEY (`vacante_id`) REFERENCES `coordinacion_vacante` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_practicaempresarial` (
  `id`                   bigint       NOT NULL AUTO_INCREMENT,
  `fecha_inicio`         date         NOT NULL,
  `fecha_fin_estimada`   date         NOT NULL,
  `fecha_fin_real`       date         DEFAULT NULL,
  `plan_practica`        varchar(100) DEFAULT NULL,
  `plan_aprobado`        tinyint(1)   NOT NULL DEFAULT 0,
  `estado`               varchar(20)  NOT NULL DEFAULT 'EN_CURSO',
  `fecha_creacion`       datetime(6)  NOT NULL,
  `observaciones`        longtext     DEFAULT NULL,
  `asignada_por_id`      bigint       NOT NULL,
  `docente_asesor_id`    bigint       DEFAULT NULL,
  `empresa_id`           bigint       NOT NULL,
  `estudiante_id`        bigint       NOT NULL,
  `tutor_empresarial_id` bigint       DEFAULT NULL,
  `vacante_id`           bigint       DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `coordinacion_practicaempresarial_asignada_por_id_idx`      (`asignada_por_id`),
  KEY `coordinacion_practicaempresarial_docente_asesor_id_idx`    (`docente_asesor_id`),
  KEY `coordinacion_practicaempresarial_empresa_id_idx`           (`empresa_id`),
  KEY `coordinacion_practicaempresarial_estudiante_id_idx`        (`estudiante_id`),
  KEY `coordinacion_practicaempresarial_tutor_empresarial_id_idx` (`tutor_empresarial_id`),
  KEY `coordinacion_practicaempresarial_vacante_id_idx`           (`vacante_id`),
  CONSTRAINT `coordinacion_practicaempresarial_asignada_por_id_fk`
    FOREIGN KEY (`asignada_por_id`) REFERENCES `coordinacion_coordinador` (`id`),
  CONSTRAINT `coordinacion_practicaempresarial_docente_asesor_id_fk`
    FOREIGN KEY (`docente_asesor_id`) REFERENCES `coordinacion_docenteasesor` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `coordinacion_practicaempresarial_empresa_id_fk`
    FOREIGN KEY (`empresa_id`) REFERENCES `coordinacion_empresa` (`id`),
  CONSTRAINT `coordinacion_practicaempresarial_estudiante_id_fk`
    FOREIGN KEY (`estudiante_id`) REFERENCES `coordinacion_estudiante` (`id`),
  CONSTRAINT `coordinacion_practicaempresarial_tutor_empresarial_id_fk`
    FOREIGN KEY (`tutor_empresarial_id`) REFERENCES `coordinacion_tutorempresarial` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `coordinacion_practicaempresarial_vacante_id_fk`
    FOREIGN KEY (`vacante_id`) REFERENCES `coordinacion_vacante` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_sustentacion` (
  `id`                bigint       NOT NULL AUTO_INCREMENT,
  `fecha_programada`  datetime(6)  NOT NULL,
  `lugar`             varchar(200) NOT NULL,
  `estado`            varchar(20)  NOT NULL DEFAULT 'PROGRAMADA',
  `calificacion`      decimal(3,1) DEFAULT NULL,
  `observaciones`     longtext     DEFAULT NULL,
  `acta_sustentacion` varchar(100) DEFAULT NULL,
  `fecha_registro`    datetime(6)  NOT NULL,
  `jurado_1_id`       bigint       DEFAULT NULL,
  `jurado_2_id`       bigint       DEFAULT NULL,
  `practica_id`       bigint       NOT NULL,
  `registrada_por_id` bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coordinacion_sustentacion_practica_id_uniq` (`practica_id`),
  KEY `coordinacion_sustentacion_jurado_1_id_idx`       (`jurado_1_id`),
  KEY `coordinacion_sustentacion_jurado_2_id_idx`       (`jurado_2_id`),
  KEY `coordinacion_sustentacion_registrada_por_id_idx` (`registrada_por_id`),
  CONSTRAINT `coordinacion_sustentacion_jurado_1_id_fk`
    FOREIGN KEY (`jurado_1_id`) REFERENCES `coordinacion_docenteasesor` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `coordinacion_sustentacion_jurado_2_id_fk`
    FOREIGN KEY (`jurado_2_id`) REFERENCES `coordinacion_docenteasesor` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `coordinacion_sustentacion_practica_id_fk`
    FOREIGN KEY (`practica_id`) REFERENCES `coordinacion_practicaempresarial` (`id`),
  CONSTRAINT `coordinacion_sustentacion_registrada_por_id_fk`
    FOREIGN KEY (`registrada_por_id`) REFERENCES `coordinacion_coordinador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Nota: columna usa la ñ exacta del campo Python del modelo
CREATE TABLE IF NOT EXISTS `coordinacion_evaluacion` (
  `id`                     bigint       NOT NULL AUTO_INCREMENT,
  `tipo`                   varchar(20)  NOT NULL,
  `desempeño_tecnico`      decimal(3,1) NOT NULL,
  `cumplimiento_objetivos` decimal(3,1) NOT NULL,
  `trabajo_equipo`         decimal(3,1) NOT NULL,
  `iniciativa`             decimal(3,1) NOT NULL,
  `presentacion_informes`  decimal(3,1) NOT NULL,
  `calificacion_final`     decimal(3,1) NOT NULL,
  `observaciones`          longtext     DEFAULT NULL,
  `fecha_evaluacion`       datetime(6)  NOT NULL,
  `evaluado_por_id`        bigint       NOT NULL,
  `practica_id`            bigint       NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coordinacion_evaluacion_evaluado_por_id_idx` (`evaluado_por_id`),
  KEY `coordinacion_evaluacion_practica_id_idx`     (`practica_id`),
  CONSTRAINT `coordinacion_evaluacion_evaluado_por_id_fk`
    FOREIGN KEY (`evaluado_por_id`) REFERENCES `coordinacion_docenteasesor` (`id`),
  CONSTRAINT `coordinacion_evaluacion_practica_id_fk`
    FOREIGN KEY (`practica_id`) REFERENCES `coordinacion_practicaempresarial` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_seguimientosemanal` (
  `id`                     bigint       NOT NULL AUTO_INCREMENT,
  `semana_numero`          int          NOT NULL,
  `fecha_inicio`           date         NOT NULL,
  `fecha_fin`              date         NOT NULL,
  `actividades_realizadas` longtext     NOT NULL,
  `logros`                 longtext     DEFAULT NULL,
  `dificultades`           longtext     DEFAULT NULL,
  `evidencia`              varchar(100) DEFAULT NULL,
  `estado`                 varchar(20)  NOT NULL DEFAULT 'PENDIENTE',
  `validado_tutor`         tinyint(1)   NOT NULL DEFAULT 0,
  `validado_docente`       tinyint(1)   NOT NULL DEFAULT 0,
  `calificacion`           decimal(3,1) DEFAULT NULL,
  `observaciones_tutor`    longtext     DEFAULT NULL,
  `observaciones_docente`  longtext     DEFAULT NULL,
  `fecha_revision_docente` datetime(6)  DEFAULT NULL,
  `fecha_registro`         datetime(6)  NOT NULL,
  `fecha_actualizacion`    datetime(6)  NOT NULL,
  `practica_id`            bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coordinacion_seguimientosemanal_practica_semana_uniq` (`practica_id`, `semana_numero`),
  CONSTRAINT `coordinacion_seguimientosemanal_practica_id_fk`
    FOREIGN KEY (`practica_id`) REFERENCES `coordinacion_practicaempresarial` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_mensaje` (
  `id`              bigint       NOT NULL AUTO_INCREMENT,
  `contenido`       longtext     NOT NULL,
  `archivo_adjunto` varchar(100) DEFAULT NULL,
  `leido`           tinyint(1)   NOT NULL DEFAULT 0,
  `fecha_envio`     datetime(6)  NOT NULL,
  `fecha_lectura`   datetime(6)  DEFAULT NULL,
  `practica_id`     bigint       NOT NULL,
  `remitente_id`    bigint       NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coordinacion_mensaje_practica_id_idx`  (`practica_id`),
  KEY `coordinacion_mensaje_remitente_id_idx` (`remitente_id`),
  CONSTRAINT `coordinacion_mensaje_practica_id_fk`
    FOREIGN KEY (`practica_id`) REFERENCES `coordinacion_practicaempresarial` (`id`),
  CONSTRAINT `coordinacion_mensaje_remitente_id_fk`
    FOREIGN KEY (`remitente_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_encuesta` (
  `id`             bigint       NOT NULL AUTO_INCREMENT,
  `titulo`         varchar(300) NOT NULL,
  `descripcion`    longtext     NOT NULL,
  `estado`         varchar(20)  NOT NULL DEFAULT 'ACTIVA',
  `fecha_creacion` datetime(6)  NOT NULL,
  `fecha_inicio`   date         NOT NULL,
  `fecha_fin`      date         NOT NULL,
  `creada_por_id`  bigint       NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coordinacion_encuesta_creada_por_id_idx` (`creada_por_id`),
  CONSTRAINT `coordinacion_encuesta_creada_por_id_fk`
    FOREIGN KEY (`creada_por_id`) REFERENCES `coordinacion_coordinador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_preguntaencuesta` (
  `id`             bigint      NOT NULL AUTO_INCREMENT,
  `texto_pregunta` longtext    NOT NULL,
  `tipo`           varchar(20) NOT NULL DEFAULT 'CALIFICACION',
  `orden`          int         NOT NULL DEFAULT 0,
  `requerida`      tinyint(1)  NOT NULL DEFAULT 1,
  `opciones`       json        DEFAULT NULL,
  `encuesta_id`    bigint      NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coordinacion_preguntaencuesta_encuesta_id_idx` (`encuesta_id`),
  CONSTRAINT `coordinacion_preguntaencuesta_encuesta_id_fk`
    FOREIGN KEY (`encuesta_id`) REFERENCES `coordinacion_encuesta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_respuestaencuesta` (
  `id`                    bigint       NOT NULL AUTO_INCREMENT,
  `estado`                varchar(20)  NOT NULL DEFAULT 'EN_PROGRESO',
  `calificacion_promedio` decimal(3,1) DEFAULT NULL,
  `fecha_inicio`          datetime(6)  NOT NULL,
  `fecha_completado`      datetime(6)  DEFAULT NULL,
  `encuesta_id`           bigint       NOT NULL,
  `practica_id`           bigint       NOT NULL,
  `tutor_id`              bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coordinacion_respuestaencuesta_encuesta_practica_tutor_uniq`
    (`encuesta_id`, `practica_id`, `tutor_id`),
  KEY `coordinacion_respuestaencuesta_practica_id_idx` (`practica_id`),
  KEY `coordinacion_respuestaencuesta_tutor_id_idx`    (`tutor_id`),
  CONSTRAINT `coordinacion_respuestaencuesta_encuesta_id_fk`
    FOREIGN KEY (`encuesta_id`) REFERENCES `coordinacion_encuesta` (`id`),
  CONSTRAINT `coordinacion_respuestaencuesta_practica_id_fk`
    FOREIGN KEY (`practica_id`) REFERENCES `coordinacion_practicaempresarial` (`id`),
  CONSTRAINT `coordinacion_respuestaencuesta_tutor_id_fk`
    FOREIGN KEY (`tutor_id`) REFERENCES `coordinacion_tutorempresarial` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `coordinacion_detallerespuestaencuesta` (
  `id`                    bigint       NOT NULL AUTO_INCREMENT,
  `calificacion`          int          DEFAULT NULL,
  `texto_respuesta`       longtext     DEFAULT NULL,
  `opcion_seleccionada`   varchar(500) DEFAULT NULL,
  `pregunta_id`           bigint       NOT NULL,
  `respuesta_encuesta_id` bigint       NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coordinacion_detallerespuestaencuesta_respuesta_pregunta_uniq`
    (`respuesta_encuesta_id`, `pregunta_id`),
  KEY `coordinacion_detallerespuestaencuesta_pregunta_id_idx` (`pregunta_id`),
  CONSTRAINT `coordinacion_detallerespuestaencuesta_pregunta_id_fk`
    FOREIGN KEY (`pregunta_id`) REFERENCES `coordinacion_preguntaencuesta` (`id`),
  CONSTRAINT `coordinacion_detallerespuestaencuesta_respuesta_encuesta_id_fk`
    FOREIGN KEY (`respuesta_encuesta_id`) REFERENCES `coordinacion_respuestaencuesta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ========================================================================================
-- 4. DATOS DEL SISTEMA DJANGO
-- ========================================================================================

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1,  'admin',        'logentry'),
(2,  'auth',         'permission'),
(3,  'auth',         'group'),
(4,  'auth',         'user'),
(5,  'contenttypes', 'contenttype'),
(6,  'sessions',     'session'),
(7,  'coordinacion', 'coordinador'),
(8,  'coordinacion', 'empresa'),
(9,  'coordinacion', 'vacante'),
(10, 'coordinacion', 'estudiante'),
(11, 'coordinacion', 'postulacion'),
(12, 'coordinacion', 'tutorempresarial'),
(13, 'coordinacion', 'docenteasesor'),
(14, 'coordinacion', 'practicaempresarial'),
(15, 'coordinacion', 'sustentacion'),
(16, 'coordinacion', 'evaluacion'),
(17, 'coordinacion', 'seguimientosemanal'),
(18, 'coordinacion', 'mensaje'),
(19, 'coordinacion', 'encuesta'),
(20, 'coordinacion', 'preguntaencuesta'),
(21, 'coordinacion', 'respuestaencuesta'),
(22, 'coordinacion', 'detallerespuestaencuesta');

ALTER TABLE `django_content_type` AUTO_INCREMENT = 23;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1,  'Can add log entry',                    1,  'add_logentry'),
(2,  'Can change log entry',                 1,  'change_logentry'),
(3,  'Can delete log entry',                 1,  'delete_logentry'),
(4,  'Can view log entry',                   1,  'view_logentry'),
(5,  'Can add permission',                   2,  'add_permission'),
(6,  'Can change permission',                2,  'change_permission'),
(7,  'Can delete permission',                2,  'delete_permission'),
(8,  'Can view permission',                  2,  'view_permission'),
(9,  'Can add group',                        3,  'add_group'),
(10, 'Can change group',                     3,  'change_group'),
(11, 'Can delete group',                     3,  'delete_group'),
(12, 'Can view group',                       3,  'view_group'),
(13, 'Can add user',                         4,  'add_user'),
(14, 'Can change user',                      4,  'change_user'),
(15, 'Can delete user',                      4,  'delete_user'),
(16, 'Can view user',                        4,  'view_user'),
(17, 'Can add content type',                 5,  'add_contenttype'),
(18, 'Can change content type',              5,  'change_contenttype'),
(19, 'Can delete content type',              5,  'delete_contenttype'),
(20, 'Can view content type',                5,  'view_contenttype'),
(21, 'Can add session',                      6,  'add_session'),
(22, 'Can change session',                   6,  'change_session'),
(23, 'Can delete session',                   6,  'delete_session'),
(24, 'Can view session',                     6,  'view_session'),
(25, 'Can add coordinador empresarial',      7,  'add_coordinador'),
(26, 'Can change coordinador empresarial',   7,  'change_coordinador'),
(27, 'Can delete coordinador empresarial',   7,  'delete_coordinador'),
(28, 'Can view coordinador empresarial',     7,  'view_coordinador'),
(29, 'Can add empresa formadora',            8,  'add_empresa'),
(30, 'Can change empresa formadora',         8,  'change_empresa'),
(31, 'Can delete empresa formadora',         8,  'delete_empresa'),
(32, 'Can view empresa formadora',           8,  'view_empresa'),
(33, 'Can add vacante de práctica',          9,  'add_vacante'),
(34, 'Can change vacante de práctica',       9,  'change_vacante'),
(35, 'Can delete vacante de práctica',       9,  'delete_vacante'),
(36, 'Can view vacante de práctica',         9,  'view_vacante'),
(37, 'Can add estudiante',                   10, 'add_estudiante'),
(38, 'Can change estudiante',                10, 'change_estudiante'),
(39, 'Can delete estudiante',                10, 'delete_estudiante'),
(40, 'Can view estudiante',                  10, 'view_estudiante'),
(41, 'Can add postulación',                  11, 'add_postulacion'),
(42, 'Can change postulación',               11, 'change_postulacion'),
(43, 'Can delete postulación',               11, 'delete_postulacion'),
(44, 'Can view postulación',                 11, 'view_postulacion'),
(45, 'Can add tutor empresarial',            12, 'add_tutorempresarial'),
(46, 'Can change tutor empresarial',         12, 'change_tutorempresarial'),
(47, 'Can delete tutor empresarial',         12, 'delete_tutorempresarial'),
(48, 'Can view tutor empresarial',           12, 'view_tutorempresarial'),
(49, 'Can add docente asesor',               13, 'add_docenteasesor'),
(50, 'Can change docente asesor',            13, 'change_docenteasesor'),
(51, 'Can delete docente asesor',            13, 'delete_docenteasesor'),
(52, 'Can view docente asesor',              13, 'view_docenteasesor'),
(53, 'Can add práctica empresarial',         14, 'add_practicaempresarial'),
(54, 'Can change práctica empresarial',      14, 'change_practicaempresarial'),
(55, 'Can delete práctica empresarial',      14, 'delete_practicaempresarial'),
(56, 'Can view práctica empresarial',        14, 'view_practicaempresarial'),
(57, 'Can add sustentación',                 15, 'add_sustentacion'),
(58, 'Can change sustentación',              15, 'change_sustentacion'),
(59, 'Can delete sustentación',              15, 'delete_sustentacion'),
(60, 'Can view sustentación',                15, 'view_sustentacion'),
(61, 'Can add evaluación',                   16, 'add_evaluacion'),
(62, 'Can change evaluación',                16, 'change_evaluacion'),
(63, 'Can delete evaluación',                16, 'delete_evaluacion'),
(64, 'Can view evaluación',                  16, 'view_evaluacion'),
(65, 'Can add seguimiento semanal',          17, 'add_seguimientosemanal'),
(66, 'Can change seguimiento semanal',       17, 'change_seguimientosemanal'),
(67, 'Can delete seguimiento semanal',       17, 'delete_seguimientosemanal'),
(68, 'Can view seguimiento semanal',         17, 'view_seguimientosemanal'),
(69, 'Can add mensaje',                      18, 'add_mensaje'),
(70, 'Can change mensaje',                   18, 'change_mensaje'),
(71, 'Can delete mensaje',                   18, 'delete_mensaje'),
(72, 'Can view mensaje',                     18, 'view_mensaje'),
(73, 'Can add encuesta',                     19, 'add_encuesta'),
(74, 'Can change encuesta',                  19, 'change_encuesta'),
(75, 'Can delete encuesta',                  19, 'delete_encuesta'),
(76, 'Can view encuesta',                    19, 'view_encuesta'),
(77, 'Can add pregunta de encuesta',         20, 'add_preguntaencuesta'),
(78, 'Can change pregunta de encuesta',      20, 'change_preguntaencuesta'),
(79, 'Can delete pregunta de encuesta',      20, 'delete_preguntaencuesta'),
(80, 'Can view pregunta de encuesta',        20, 'view_preguntaencuesta'),
(81, 'Can add respuesta de encuesta',        21, 'add_respuestaencuesta'),
(82, 'Can change respuesta de encuesta',     21, 'change_respuestaencuesta'),
(83, 'Can delete respuesta de encuesta',     21, 'delete_respuestaencuesta'),
(84, 'Can view respuesta de encuesta',       21, 'view_respuestaencuesta'),
(85, 'Can add detalle respuesta encuesta',   22, 'add_detallerespuestaencuesta'),
(86, 'Can change detalle respuesta encuesta',22, 'change_detallerespuestaencuesta'),
(87, 'Can delete detalle respuesta encuesta',22, 'delete_detallerespuestaencuesta'),
(88, 'Can view detalle respuesta encuesta',  22, 'view_detallerespuestaencuesta');

ALTER TABLE `auth_permission` AUTO_INCREMENT = 89;

INSERT INTO `django_migrations` (`app`, `name`, `applied`) VALUES
('contenttypes', '0001_initial',                                '2025-11-04 22:33:00.000000'),
('contenttypes', '0002_remove_content_type_name',               '2025-11-04 22:33:00.100000'),
('auth',         '0001_initial',                                '2025-11-04 22:33:00.200000'),
('auth',         '0002_alter_permission_name_max_length',       '2025-11-04 22:33:00.300000'),
('auth',         '0003_alter_user_email_max_length',            '2025-11-04 22:33:00.400000'),
('auth',         '0004_alter_user_username_opts',               '2025-11-04 22:33:00.500000'),
('auth',         '0005_alter_user_last_login_null',             '2025-11-04 22:33:00.600000'),
('auth',         '0006_require_contenttypes_0002',              '2025-11-04 22:33:00.700000'),
('auth',         '0007_alter_validators_add_error_messages',    '2025-11-04 22:33:00.800000'),
('auth',         '0008_alter_user_username_max_length',         '2025-11-04 22:33:00.900000'),
('auth',         '0009_alter_user_last_name_max_length',        '2025-11-04 22:33:01.000000'),
('auth',         '0010_alter_group_name_max_length',            '2025-11-04 22:33:01.100000'),
('auth',         '0011_update_proxy_permissions',               '2025-11-04 22:33:01.200000'),
('auth',         '0012_alter_user_first_name_max_length',       '2025-11-04 22:33:01.300000'),
('coordinacion', '0001_initial',                                '2025-11-04 22:33:02.000000'),
('coordinacion', '0002_docenteasesor_empresa_estudiante_practicaempresarial_and_more', '2025-11-04 22:33:02.100000'),
('coordinacion', '0003_alter_practicaempresarial_estado',       '2025-11-04 22:33:02.200000'),
('coordinacion', '0004_alter_sustentacion_estado',              '2025-11-04 22:33:02.300000'),
('coordinacion', '0005_seguimientosemanal_estado_and_more',     '2025-11-04 22:33:02.400000'),
('coordinacion', '0006_seguimientosemanal_calificacion',        '2025-11-04 22:33:02.500000'),
('coordinacion', '0007_coordinador_foto_perfil_docenteasesor_cedula_and_more', '2025-11-04 22:33:02.600000'),
('coordinacion', '0008_encuesta_preguntaencuesta_respuestaencuesta_and_more',  '2025-11-04 22:33:02.700000'),
('coordinacion', '0009_tutorempresarial_foto_perfil_tutorempresarial_user',    '2025-11-04 22:33:02.800000'),
('admin',        '0001_initial',                                '2025-11-04 22:33:03.000000'),
('admin',        '0002_logentry_remove_auto_add',               '2025-11-04 22:33:03.100000'),
('admin',        '0003_logentry_add_action_flag_choices',       '2025-11-04 22:33:03.200000'),
('sessions',     '0001_initial',                                '2025-11-04 22:33:04.000000');


-- ========================================================================================
-- 5. DATOS REALES — EXPORTADOS DESDE db.sqlite3
-- ========================================================================================

-- ------------------------------------------------
-- auth_user  (hashes exactos del original — mismas contraseñas)
-- ------------------------------------------------
INSERT INTO `auth_user`
  (`id`, `password`, `last_login`, `is_superuser`, `username`,
   `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`)
VALUES
(1,
 'pbkdf2_sha256$1000000$vJpqd6oYIxItwHH6qzde5K$ft0ERJVmOCJIYvaOVxJCc/POojIkpAXaukdm9NenjJU=',
 '2025-11-04 22:34:46.617393', 1, 'admin', '', '', 'gamerly9060@gmail.com',
 1, 1, '2025-11-04 22:33:32.876430'),
(2,
 'pbkdf2_sha256$1000000$jFAN6z9NApOb3bbjYEBRT9$jKYhLTCZcjMJnLrTjGsl7nUo3zPQkGhGukqE77xKqoA=',
 '2025-11-29 00:58:49.536339', 1, 'coordinador', '', '', 'cordemphumbldt_115@gmail.com',
 1, 1, '2025-11-04 22:41:25.877571'),
(56,
 'pbkdf2_sha256$1000000$tpscNIvY1e9dmJGMHbqaXn$f1v9lVI+Da4YHNG214U1VIBp4WHJuY+mifZZiF4JmOI=',
 '2025-12-02 22:23:06.182053', 0, 'coord001', 'María', 'García',
 'coordinador@universidad.edu', 0, 1, '2025-11-30 19:36:27.688079'),
(57,
 'pbkdf2_sha256$1000000$jJwCjU1odnchutVJ1QDnG8$hK1FN7PlVjflnKmFgEuhGPQwXB/xuWs/XAtrCML+b0Y=',
 '2025-12-02 21:36:04.021633', 0, 'docente001', 'Carlos', 'López',
 'carlos.perez@universidad.edu', 0, 1, '2025-11-30 19:36:28.338273'),
(58,
 'pbkdf2_sha256$1000000$04Q4SwRWPpbmIW29UIDBjb$8Lf4w7hLxnHoBI9S5TXVnoDYbktD5OsF2w4HmRvpy2w=',
 NULL, 0, 'docente002', 'Ana', 'Gómez',
 'ana.gomez@universidad.edu', 0, 1, '2025-11-30 19:36:28.979963'),
(59,
 'pbkdf2_sha256$1000000$c6yKeaICI0xlpcBnrNuuLZ$JqFdfBPoWI1DVx9i6slrpoLC0Ih8ypJfs5S9XkN545o=',
 NULL, 0, 'docente003', 'Luis', 'Torres',
 'luis.torres@universidad.edu', 0, 1, '2025-11-30 19:36:29.603606'),
(60,
 'pbkdf2_sha256$1000000$J4azKL4qq3H032aqowRFcO$y/+1ipGFhjdhaBnajEarGoZizmx42L1TJljJE/y/s5w=',
 '2025-12-16 03:32:08.573563', 0, 'est001', 'Juan', 'Martínez',
 'juan.martinez@estudiante.edu', 0, 1, '2025-11-30 19:36:30.262986'),
(61,
 'pbkdf2_sha256$1000000$4ZwHt3WCSyUzx0SwZorbdY$xswqw9a+8l9y7FlXO6KJOiy8Gspm6r1Si3ph5ldVGUg=',
 NULL, 0, 'est002', 'María', 'Rodríguez',
 'maria.rodriguez@estudiante.edu', 0, 1, '2025-11-30 19:36:30.913161'),
(62,
 'pbkdf2_sha256$1000000$x8G6r2Jb4nA1UUI4FlYaj7$KdcZJvuWekTHudWS5VYFFVXLnaA12dl8VrfFWAik60I=',
 NULL, 0, 'est003', 'Carlos', 'López',
 'carlos.lopez@estudiante.edu', 0, 1, '2025-11-30 19:36:31.535322'),
(63,
 'pbkdf2_sha256$1000000$a34CJtwwv7XFTfRIwWS9wt$2FQgBJGJaQSYndKZR6vY1Urj8dhZ9cfix1Z3jBqnDls=',
 NULL, 0, 'est004', 'Laura', 'Gómez',
 'laura.gomez@estudiante.edu', 0, 1, '2025-11-30 19:36:32.186014'),
(64,
 'pbkdf2_sha256$1000000$VLlfZbhW9FKqYLrguVbNG6$/eC7UGFsOP5gs43YDXVw0O+egr9Y2vcszc9qNd1qM7k=',
 NULL, 0, 'est005', 'Santiago', 'Hernández',
 'santiago.hernandez@estudiante.edu', 0, 1, '2025-11-30 19:36:32.804365'),
(65,
 'pbkdf2_sha256$1000000$bsaKirBMTQrtkkfXjkbpb2$VXNicjp8AsM9QLNLbGSidUkKIxnB5vEudK80vRGTlBg=',
 NULL, 0, 'est006', 'Daniela', 'Castro',
 'daniela.castro@estudiante.edu', 0, 1, '2025-11-30 19:36:33.458638'),
(66,
 'pbkdf2_sha256$1000000$e84g12C633IHYBYqTg1FVX$oM/yrGxz/hgOWrVjZb8i+vMsk4qjaenTn/3acfBdx18=',
 NULL, 0, 'est007', 'Andrés', 'Morales',
 'andres.morales@estudiante.edu', 0, 1, '2025-11-30 19:36:34.109733'),
(67,
 'pbkdf2_sha256$1000000$sdIDPqV7hPhnwwbAAyPsop$QnaUXUqkVuDkXxileCXn6EZIvt/u7YDHDfkgSomxWQw=',
 NULL, 0, 'est008', 'Isabella', 'Ramírez',
 'isabella.ramirez@estudiante.edu', 0, 1, '2025-11-30 19:36:34.765542'),
(68,
 'pbkdf2_sha256$1000000$5NgKHPtX9OsTs0Hfnk4IqW$aQr0pGXOi4jYuBtRtlZWp+hc1D8tLzpSHItaRwOZp98=',
 '2025-12-01 18:20:06.207087', 0, 'tutor001', 'Roberto', 'Sánchez',
 'tutor@empresa.com', 0, 1, '2025-12-01 13:06:24.297518');

ALTER TABLE `auth_user` AUTO_INCREMENT = 69;

-- ------------------------------------------------
-- coordinacion_coordinador
-- ------------------------------------------------
INSERT INTO `coordinacion_coordinador`
  (`id`, `nombre_completo`, `email`, `telefono`, `foto_perfil`, `fecha_creacion`, `activo`, `user_id`)
VALUES
(7, 'María García Rodríguez', 'coordinador@universidad.edu', '3001234567',
 'coordinadores/fotos_perfil/descargar.jpg',
 '2025-11-30 19:36:28.318752', 1, 56);

ALTER TABLE `coordinacion_coordinador` AUTO_INCREMENT = 8;

-- ------------------------------------------------
-- coordinacion_empresa
-- ------------------------------------------------
INSERT INTO `coordinacion_empresa`
  (`id`, `razon_social`, `nit`, `direccion`, `telefono`, `email`, `ciudad`,
   `representante_nombre`, `representante_cargo`, `representante_email`, `representante_telefono`,
   `camara_comercio`, `rut`, `estado`, `fecha_registro`, `fecha_aprobacion`, `observaciones`, `aprobada_por_id`)
VALUES
(11, 'TechSolutions S.A.S',       '900123456-1', 'Cra 7 #32-40, Bogotá',          '6013001234',
 'contacto@techsolutions.com', 'Bogotá',
 'Carlos Alberto Pérez',    'Gerente General',             'carlos.perez@techsolutions.com', '3001112233',
 '', '', 'APROBADA', '2025-11-30 19:36:35.411230', NULL, NULL, 7),
(12, 'Manufacturas Industriales Ltda', '800234567-2', 'Autopista Norte Km 15, Bogotá', '6014002345',
 'rrhh@manufacturas.com',      'Bogotá',
 'María Victoria Gómez',    'Gerente de Recursos Humanos', 'maria.gomez@manufacturas.com',   '3002223344',
 '', '', 'APROBADA', '2025-11-30 19:36:35.465819', NULL, NULL, 7),
(13, 'Comercializadora Global S.A', '900345678-3', 'Av. El Dorado #68-55, Bogotá', '6015003456',
 'info@comercializadora.com',   'Bogotá',
 'Jorge Luis Ramírez',      'Gerente General',             'jorge.ramirez@comercializadora.com', '3003334455',
 '', '', 'APROBADA', '2025-11-30 19:36:35.520372', NULL, NULL, 7);

ALTER TABLE `coordinacion_empresa` AUTO_INCREMENT = 14;

-- ------------------------------------------------
-- coordinacion_docenteasesor
-- ------------------------------------------------
INSERT INTO `coordinacion_docenteasesor`
  (`id`, `nombre_completo`, `cedula`, `email`, `telefono`, `especialidad`, `foto_perfil`, `activo`, `fecha_registro`, `user_id`)
VALUES
(9,  'Ingeniero Arle Morales',    NULL, 'carlos.perez@universidad.edu', '3101234567',
 'Ingeniería de Software',       'docentes/fotos_perfil/descargar_1.jpg', 1, '2025-11-30 19:36:28.961428', 57),
(10, 'Dra. Ana María Gómez',      NULL, 'ana.gomez@universidad.edu',    '3102234567',
 'Ingeniería Industrial',        '', 1, '2025-11-30 19:36:29.588347', 58),
(11, 'Mg. Luis Alberto Torres',   NULL, 'luis.torres@universidad.edu',  '3103234567',
 'Administración de Empresas',   '', 1, '2025-11-30 19:36:30.241330', 59);

ALTER TABLE `coordinacion_docenteasesor` AUTO_INCREMENT = 12;

-- ------------------------------------------------
-- coordinacion_tutorempresarial
-- ------------------------------------------------
INSERT INTO `coordinacion_tutorempresarial`
  (`id`, `nombre_completo`, `cargo`, `email`, `telefono`, `foto_perfil`, `activo`, `fecha_registro`, `empresa_id`, `user_id`)
VALUES
(7,  'Ing. Roberto Sánchez', 'Director de TI',
 'roberto.sanchez@techsolutions.com',   '3301234567', '', 1, '2025-11-30 19:36:35.427467', 11, NULL),
(8,  'Ing. Patricia Vega',   'Jefe de Producción',
 'patricia.vega@manufacturas.com',      '3302234567', '', 1, '2025-11-30 19:36:35.486304', 12, NULL),
(9,  'Adm. Claudia Moreno',  'Gerente de Talento Humano',
 'claudia.moreno@comercializadora.com', '3303234567', '', 1, '2025-11-30 19:36:35.538941', 13, NULL),
(10, 'Ing. Roberto Sánchez', 'Jefe de Desarrollo',
 'tutor@empresa.com',                   '3001234567',
 'tutores/fotos_perfil/images.jpg',     1, '2025-12-01 13:16:56.746086', 13, 68);

ALTER TABLE `coordinacion_tutorempresarial` AUTO_INCREMENT = 11;

-- ------------------------------------------------
-- coordinacion_estudiante
-- ------------------------------------------------
INSERT INTO `coordinacion_estudiante`
  (`id`, `codigo`, `nombre_completo`, `email`, `telefono`, `programa_academico`,
   `semestre`, `foto_perfil`, `hoja_vida`, `estado`, `promedio_academico`, `fecha_registro`, `user_id`)
VALUES
(38, 'IS2021001', 'Arle',                      'juan.martinez@estudiante.edu',    '3201234567',
 'Ingeniería de Software',       5, 'estudiantes/fotos_perfil/descargar_2.jpg', '', 'EN_PRACTICA', 4.20, '2025-11-30 19:36:30.893755', 60),
(39, 'IS2021002', 'María Camila Rodríguez',    'maria.rodriguez@estudiante.edu',  '3202234567',
 'Ingeniería de Software',       6, '', '', 'APTO',        4.50, '2025-11-30 19:36:31.516345', 61),
(40, 'IS2022001', 'Carlos Andrés López',       'carlos.lopez@estudiante.edu',     '3203234567',
 'Ingeniería de Software',       4, '', '', 'APTO',        4.00, '2025-11-30 19:36:32.166983', 62),
(41, 'II2021001', 'Laura Valentina Gómez',     'laura.gomez@estudiante.edu',      '3204234567',
 'Ingeniería Industrial',        5, '', '', 'APTO',        4.30, '2025-11-30 19:36:32.782843', 63),
(42, 'II2021002', 'Santiago Hernández',        'santiago.hernandez@estudiante.edu','3205234567',
 'Ingeniería Industrial',        6, '', '', 'APTO',        4.10, '2025-11-30 19:36:33.431730', 64),
(43, 'AE2022001', 'Daniela Alejandra Castro',  'daniela.castro@estudiante.edu',   '3206234567',
 'Administración de Empresas',   3, '', '', 'FINALIZADO',  4.40, '2025-11-30 19:36:34.092633', 65),
(44, 'AE2022002', 'Andrés Felipe Morales',     'andres.morales@estudiante.edu',   '3207234567',
 'Administración de Empresas',   4, '', '', 'EN_PRACTICA', 3.90, '2025-11-30 19:36:34.746760', 66),
(45, 'AE2023001', 'Isabella Ramírez',          'isabella.ramirez@estudiante.edu', '3208234567',
 'Administración de Empresas',   2, '', '', 'APTO',        4.00, '2025-11-30 19:36:35.391270', 67);

ALTER TABLE `coordinacion_estudiante` AUTO_INCREMENT = 46;

-- ------------------------------------------------
-- coordinacion_vacante
-- ------------------------------------------------
INSERT INTO `coordinacion_vacante`
  (`id`, `titulo`, `area_practica`, `descripcion`, `cantidad_cupos`, `cupos_ocupados`,
   `programa_academico`, `semestre_minimo`, `habilidades_requeridas`, `horario`,
   `duracion_meses`, `estado`, `fecha_creacion`, `fecha_publicacion`, `fecha_cierre`,
   `empresa_id`, `creada_por_id`)
VALUES
(14, 'Practicante Desarrollo de Software', 'Desarrollo de Software',
 'Apoyo en desarrollo de aplicaciones web con React y Django',
 2, 1, 'Ingeniería de Software', 4,
 'Python, JavaScript, React, Django',
 'Lunes a Viernes 8:00 AM - 2:00 PM', 6, 'DISPONIBLE',
 '2025-11-30 19:36:35.446000', NULL, NULL, 11, 7),
(15, 'Practicante Ingeniería de Procesos', 'Procesos Industriales',
 'Apoyo en optimización de procesos productivos',
 1, 0, 'Ingeniería Industrial', 4,
 'Lean Manufacturing, Six Sigma, Análisis de procesos',
 'Lunes a Viernes 7:00 AM - 1:00 PM', 6, 'DISPONIBLE',
 '2025-11-30 19:36:35.504762', NULL, NULL, 12, 7),
(16, 'Practicante Administración', 'Gestión Administrativa',
 'Apoyo en gestión administrativa y comercial',
 2, 1, 'Administración de Empresas', 2,
 'Excel, gestión documental, atención al cliente',
 'Lunes a Viernes 8:00 AM - 3:00 PM', 6, 'DISPONIBLE',
 '2025-11-30 19:36:35.552772', NULL, NULL, 13, 7),
(17, 'ejemploooo', 'Desarrollo de Software',
 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 1, 1, 'ingeniería de software', 4,
 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
 'Lunes a Viernes 8:00am - 5:00pm', 3, 'OCUPADA',
 '2025-12-02 22:15:23.515174', '2025-12-02 22:15:23.511042', NULL, 13, 7);

ALTER TABLE `coordinacion_vacante` AUTO_INCREMENT = 18;

-- ------------------------------------------------
-- coordinacion_postulacion
-- ------------------------------------------------
INSERT INTO `coordinacion_postulacion`
  (`id`, `estado`, `fecha_postulacion`, `fecha_respuesta`, `observaciones`,
   `estudiante_id`, `postulado_por_id`, `vacante_id`)
VALUES
(34, 'VINCULADO',
 '2025-11-30 19:52:08.258795', '2025-11-30 20:12:43.089338',
 'Postulación aprobada y estudiante vinculado',
 38, 7, 14),
(35, 'SELECCIONADO',
 '2025-11-30 19:55:04.217249', '2025-11-30 19:55:15.299463',
 'Postulación aprobada y estudiante vinculado\n\nDESVINCULADO: kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 45, 7, 16),
(36, 'VINCULADO',
 '2025-12-01 13:31:43.893258', '2025-12-01 13:31:58.965076',
 'Postulación aprobada y estudiante vinculado',
 43, 7, 16),
(37, 'VINCULADO',
 '2025-12-02 22:24:58.530596', '2025-12-02 22:25:12.042574',
 'Postulación aprobada y estudiante vinculado',
 44, 7, 17);

ALTER TABLE `coordinacion_postulacion` AUTO_INCREMENT = 38;

-- ------------------------------------------------
-- coordinacion_practicaempresarial
-- ------------------------------------------------
INSERT INTO `coordinacion_practicaempresarial`
  (`id`, `fecha_inicio`, `fecha_fin_estimada`, `fecha_fin_real`,
   `plan_practica`, `plan_aprobado`, `estado`, `fecha_creacion`, `observaciones`,
   `asignada_por_id`, `docente_asesor_id`, `empresa_id`, `estudiante_id`,
   `tutor_empresarial_id`, `vacante_id`)
VALUES
(9,  '2025-11-30', '2026-02-28', '2025-11-30',
 '', 0, 'CANCELADA', '2025-11-30 19:56:03.355441',
 'Práctica creada desde postulación #35\n\nCANCELADA: kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 7, 9, 13, 45, 9, 16),
(10, '2025-11-30', '2026-02-28', NULL,
 '', 0, 'EN_CURSO',  '2025-11-30 20:13:06.335978',
 'Práctica creada desde postulación #34',
 7, 9, 11, 38, 7, 14),
(11, '2025-12-01', '2026-03-01', NULL,
 '', 0, 'FINALIZADA','2025-12-01 13:33:20.633055',
 'Práctica creada desde postulación #36',
 7, 9, 13, 43, 10, 16);

ALTER TABLE `coordinacion_practicaempresarial` AUTO_INCREMENT = 12;

-- ------------------------------------------------
-- coordinacion_sustentacion
-- ------------------------------------------------
INSERT INTO `coordinacion_sustentacion`
  (`id`, `fecha_programada`, `lugar`, `estado`, `calificacion`,
   `observaciones`, `acta_sustentacion`, `fecha_registro`,
   `jurado_1_id`, `jurado_2_id`, `practica_id`, `registrada_por_id`)
VALUES
(6, '2026-01-01 13:33:00.000000', 'Sala de Conferencias A',
 'PROGRAMADA', NULL, NULL, NULL,
 '2025-12-01 13:34:03.872172',
 9, 10, 11, 7);

ALTER TABLE `coordinacion_sustentacion` AUTO_INCREMENT = 7;

-- coordinacion_evaluacion — sin registros en la BD original
ALTER TABLE `coordinacion_evaluacion` AUTO_INCREMENT = 1;

-- ------------------------------------------------
-- coordinacion_seguimientosemanal
-- ------------------------------------------------
INSERT INTO `coordinacion_seguimientosemanal`
  (`id`, `semana_numero`, `fecha_inicio`, `fecha_fin`,
   `actividades_realizadas`, `logros`, `dificultades`, `evidencia`,
   `estado`, `validado_tutor`, `validado_docente`, `calificacion`,
   `observaciones_tutor`, `observaciones_docente`, `fecha_revision_docente`,
   `fecha_registro`, `fecha_actualizacion`, `practica_id`)
VALUES
(1, 1, '2025-11-10', '2025-11-17',
 'ene sta semana kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 'practicas/seguimientos/sociales_guia_8_4gWRdzg.docx',
 'APROBADO', 0, 1, NULL,
 NULL, 'esta muy bonito mi muchacho',
 '2025-11-30 20:53:31.823256',
 '2025-11-30 20:17:24.319151', '2025-11-30 20:53:31.824171',
 10),
(2, 2, '2025-10-27', '2025-11-03',
 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 '',
 'APROBADO', 0, 1, 3.0,
 NULL, 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk fghggggggggggggggggggggggggggggggggggggg',
 '2025-11-30 22:44:48.290183',
 '2025-11-30 21:41:59.774787', '2025-11-30 22:44:48.292997',
 10);

ALTER TABLE `coordinacion_seguimientosemanal` AUTO_INCREMENT = 3;

-- ------------------------------------------------
-- coordinacion_mensaje
-- ------------------------------------------------
INSERT INTO `coordinacion_mensaje`
  (`id`, `contenido`, `archivo_adjunto`, `leido`, `fecha_envio`, `fecha_lectura`, `practica_id`, `remitente_id`)
VALUES
(1, 'hola',    NULL,                                                     1, '2025-12-01 00:27:08.450919', '2025-12-01 00:37:32.765308', 10, 60),
(2, '',        'mensajes/adjuntos/sociales_guia_8_4gWRdzg_1.docx',       1, '2025-12-01 00:27:16.846973', '2025-12-01 00:37:32.765308', 10, 60),
(3, 'gracias', NULL,                                                     1, '2025-12-01 00:37:42.980253', '2025-12-01 00:52:07.203922', 10, 57),
(4, 'hola',    NULL,                                                     1, '2025-12-01 01:27:19.941746', '2025-12-01 02:03:12.776667', 10, 60),
(5, '?',       NULL,                                                     1, '2025-12-01 02:00:56.319147', '2025-12-01 02:03:12.776667', 10, 60),
(6, '',        'mensajes/adjuntos/imagen_2025-11-30_210707481.png',       1, '2025-12-01 02:07:10.369741', '2025-12-01 02:19:47.651368', 10, 60),
(7, 'hola',    NULL,                                                     1, '2025-12-01 02:41:18.453778', '2025-12-01 05:03:50.548746', 10, 57),
(8, 'como estas?', NULL,                                                 1, '2025-12-01 02:47:47.546134', '2025-12-01 05:03:50.548746', 10, 57);

ALTER TABLE `coordinacion_mensaje` AUTO_INCREMENT = 9;

-- ------------------------------------------------
-- coordinacion_encuesta
-- ------------------------------------------------
INSERT INTO `coordinacion_encuesta`
  (`id`, `titulo`, `descripcion`, `estado`, `fecha_creacion`, `fecha_inicio`, `fecha_fin`, `creada_por_id`)
VALUES
(1, 'Evaluación prueba',
 'kkkkkkkkkkkkkk',
 'ACTIVA', '2025-12-01 17:36:36.516592', '2025-12-01', '2025-12-31', 7),
(2, 'Practicante de Ingeniería Industrial - Tech Solutions SAS',
 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
 'ACTIVA', '2025-12-16 03:29:35.674168', '2025-12-09', '2026-01-02', 7);

ALTER TABLE `coordinacion_encuesta` AUTO_INCREMENT = 3;

-- coordinacion_preguntaencuesta — sin registros en la BD original
ALTER TABLE `coordinacion_preguntaencuesta` AUTO_INCREMENT = 1;

-- ------------------------------------------------
-- coordinacion_respuestaencuesta
-- ------------------------------------------------
INSERT INTO `coordinacion_respuestaencuesta`
  (`id`, `estado`, `calificacion_promedio`, `fecha_inicio`, `fecha_completado`,
   `encuesta_id`, `practica_id`, `tutor_id`)
VALUES
(1, 'EN_PROGRESO', NULL, '2025-12-01 18:27:13.262662', NULL, 1, 11, 10);

ALTER TABLE `coordinacion_respuestaencuesta` AUTO_INCREMENT = 2;

-- coordinacion_detallerespuestaencuesta — sin registros en la BD original
ALTER TABLE `coordinacion_detallerespuestaencuesta` AUTO_INCREMENT = 1;


-- ========================================================================================
-- 6. RESTAURAR VERIFICACIONES DE CLAVES FORÁNEAS
-- ========================================================================================
SET FOREIGN_KEY_CHECKS = 1;

-- ========================================================================================
-- FIN DEL SCRIPT
-- ========================================================================================
-- Base de datos    : practicas_empresariales
-- Origen           : db.sqlite3  (DjangoProject)
-- Tablas creadas   : 26  (10 sistema + 16 aplicación)
-- Registros totales:
--   auth_user               : 15   coordinacion_coordinador       : 1
--   coordinacion_empresa    :  3   coordinacion_docenteasesor     : 3
--   coordinacion_tutorempresarial : 4   coordinacion_estudiante   : 8
--   coordinacion_vacante    :  4   coordinacion_postulacion       : 4
--   coordinacion_practicaempresarial : 3   coordinacion_sustentacion : 1
--   coordinacion_seguimientosemanal  : 2   coordinacion_mensaje   : 8
--   coordinacion_encuesta   :  2   coordinacion_respuestaencuesta : 1
--   (evaluacion, preguntaencuesta, detallerespuesta: vacías en el original)
-- ========================================================================================
