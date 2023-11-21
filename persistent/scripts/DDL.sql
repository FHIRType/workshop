-- SCHEMA: FhirType
-- AUTHOR: Imgyeong Lee
-- LAST_UPDATED: Nov 21, 2023

-- DROP SCHEMA IF EXISTS fhirtype CASCADE;
CREATE SCHEMA IF NOT EXISTS fhirtype AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA fhirtype
    IS 'standard public schema';

GRANT USAGE ON SCHEMA fhirtype TO PUBLIC;

GRANT ALL ON SCHEMA fhirtype TO pg_database_owner;


-- Table: fhirtype.identifier
DROP SEQUENCE IF EXISTS fhirtype.identifier_identifier_id_seq;
CREATE SEQUENCE fhirtype.identifier_identifier_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

DROP TABLE IF EXISTS fhirtype.identifier;
CREATE TABLE IF NOT EXISTS FhirType.identifier
(
    identifier_id integer NOT NULL DEFAULT nextval('fhirtype.identifier_identifier_id_seq'::regclass),
    code text COLLATE "C" NOT NULL,
    display text COLLATE "C",
    system text COLLATE "C",
    value text COLLATE "C" NOT NULL,
    use text COLLATE "C"
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS FhirType.identifier OWNER to postgres;

-- Table: fhirtype.location
DROP SEQUENCE IF EXISTS fhirtype.location_location_id_seq;
CREATE SEQUENCE fhirtype.location_location_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

DROP TABLE IF EXISTS fhirtype.location;
CREATE TABLE IF NOT EXISTS fhirtype.location
(
    location_id integer NOT NULL DEFAULT nextval('fhirtype.location_location_id_seq'::regclass),
    version_id text COLLATE "C" NOT NULL,
    last_updated date NOT NULL,
    status boolean,
    name text COLLATE "C",
    phone_number character varying(12) COLLATE "C",
    fax_number character varying(10) COLLATE "C",
    longitude numeric(5,2) NOT NULL,
    latitude numeric(5,2) NOT NULL,
    address_line text COLLATE "C",
    address_city text COLLATE "C",
    address_state character varying(2) COLLATE "C",
    postal_code text COLLATE "C" NOT NULL,
    CONSTRAINT location_pkey PRIMARY KEY (location_id)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS fhirtype.location OWNER to postgres;

-- Table: fhirtype.organization
DROP SEQUENCE IF EXISTS fhirtype.organization_organization_id_seq;
CREATE SEQUENCE fhirtype.organization_organization_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;


DROP TABLE IF EXISTS fhirtype.organization;
CREATE TABLE IF NOT EXISTS fhirtype.organization
(
    organization_id integer NOT NULL DEFAULT nextval('fhirtype.organization_organization_id_seq'::regclass),
    version_id text COLLATE "C" NOT NULL,
    last_updated date NOT NULL,
    status boolean,
    name text COLLATE "C" NOT NULL,
    phone_number character varying(12) COLLATE "C",
    fax_number character varying(10) COLLATE "C",
    longitude numeric(5,2),
    latitude numeric(5,2),
    address_line text COLLATE "C",
    address_city text COLLATE "C",
    address_state character varying(2) COLLATE "C",
    postal_code text COLLATE "C",
    CONSTRAINT organization_pkey PRIMARY KEY (organization_id)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS fhirtype.organization OWNER to postgres;


-- Table: fhirtype.practitioner
DROP SEQUENCE IF EXISTS fhirtype.practitioner_practitioner_id_seq;
CREATE SEQUENCE fhirtype.practitioner_practitioner_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

DROP TABLE IF EXISTS fhirtype.practitioner;
CREATE TABLE IF NOT EXISTS fhirtype.practitioner
(
    practitioner_id integer NOT NULL DEFAULT nextval('fhirtype.practitioner_practitioner_id_seq'::regclass),
    version_id text COLLATE "C" NOT NULL,
    last_updated date NOT NULL,
    active boolean,
    gender text COLLATE "C",
    name_use text COLLATE "C",
    name_family text COLLATE "C",
    name_given text[] COLLATE "C",
    name_full text COLLATE "C",
    CONSTRAINT practitioner_pkey PRIMARY KEY (practitioner_id)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS fhirtype.practitioner OWNER to postgres;

-- Table: fhirtype.practitioner_role
DROP SEQUENCE IF EXISTS fhirtype.practitioner_role_practitioner_role_id_seq;
CREATE SEQUENCE fhirtype.practitioner_role_practitioner_role_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

DROP TABLE IF EXISTS fhirtype.practitioner_role;
CREATE TABLE IF NOT EXISTS fhirtype.practitioner_role
(
    practitioner_role_id integer NOT NULL DEFAULT nextval('fhirtype.practitioner_role_practitioner_role_id_seq'::regclass),
    version_id text COLLATE "C" NOT NULL,
    last_updated date NOT NULL,
    active boolean,
    CONSTRAINT practitioner_role_pkey PRIMARY KEY (practitioner_role_id)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS fhirtype.practitioner_role OWNER to postgres;


-- Table: fhirtype.practitioner_role_taxanomy
DROP SEQUENCE IF EXISTS fhirtype.practitioner_role_taxanomy_practitioner_role_taxanomy_id_seq;
CREATE SEQUENCE fhirtype.practitioner_role_taxanomy_practitioner_role_taxanomy_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

DROP TABLE IF EXISTS fhirtype.practitioner_role_taxanomy;
CREATE TABLE IF NOT EXISTS fhirtype.practitioner_role_taxanomy
(
    practitioner_role_taxanomy_id integer NOT NULL DEFAULT nextval('fhirtype.practitioner_role_taxanomy_practitioner_role_taxanomy_id_seq'::regclass),
    CONSTRAINT practitioner_role_taxanomy_pkey PRIMARY KEY (practitioner_role_taxanomy_id)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS fhirtype.practitioner_role_taxanomy OWNER to postgres;


-- Table: fhirtype.taxonomy
DROP SEQUENCE IF EXISTS fhirtype.taxonomy_taxonomy_id_seq;
CREATE SEQUENCE fhirtype.taxonomy_taxonomy_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

DROP TABLE IF EXISTS fhirtype.taxonomy;
CREATE TABLE IF NOT EXISTS fhirtype.taxonomy
(
    taxonomy_id integer NOT NULL DEFAULT nextval('fhirtype.taxonomy_taxonomy_id_seq'::regclass),
    code character varying(10) COLLATE "C",
    display text COLLATE "C",
    system text COLLATE "C",
    CONSTRAINT taxonomy_pkey PRIMARY KEY (taxonomy_id)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS fhirtype.taxonomy OWNER to postgres;