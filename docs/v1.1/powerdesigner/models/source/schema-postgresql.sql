-- Esquema PostgreSQL del SaaS de reclutamiento (base reclutamiento, develop 2621bee).
-- Origen: pg_dump --schema-only --no-owner --no-privileges del contenedor postgres (PostgreSQL 17.11).
-- Limpieza para el parser 'PostgreSQL 9.x' de PowerDesigner 16.6, sin cambiar el esquema:
--   quitadas las metaordenes restrict/unrestrict de psql y las lineas SET/set_config de sesion;
--   quitado 'AS integer' de las secuencias (sintaxis PG10+);
--   EXECUTE FUNCTION -> EXECUTE PROCEDURE en el trigger (equivalente en PG9);
--   quitado el prefijo de esquema 'public.';
--   ALTER TABLE ONLY -> ALTER TABLE (ONLY solo excluye tablas heredadas, que este esquema no tiene).
-- Sin datos ni credenciales.

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.11
-- Dumped by pg_dump version 17.11

--
-- Name: audit_logs_append_only(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION audit_logs_append_only() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF TG_OP = 'UPDATE'
            AND OLD.user_id IS NOT NULL
            AND NEW.user_id IS NULL
            AND (to_jsonb(NEW) - 'user_id') = (to_jsonb(OLD) - 'user_id') THEN
            RETURN NEW;
        END IF;

        RAISE EXCEPTION 'audit_logs es de solo inserción: operación % no permitida.', TG_OP
            USING ERRCODE = 'insufficient_privilege';
    END;
    $$;

--
-- Name: application_stage_histories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE application_stage_histories (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    application_id bigint NOT NULL,
    from_status character varying(20),
    to_status character varying(20) NOT NULL,
    changed_by bigint NOT NULL,
    comment text,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

--
-- Name: application_stage_histories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE application_stage_histories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: application_stage_histories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE application_stage_histories_id_seq OWNED BY application_stage_histories.id;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE applications (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    vacancy_id bigint NOT NULL,
    candidate_id bigint NOT NULL,
    candidate_document_id bigint,
    status character varying(20) DEFAULT 'postulado'::character varying NOT NULL,
    applied_at timestamp(0) without time zone NOT NULL,
    stage_changed_at timestamp(0) without time zone,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT applications_status_valid CHECK (((status)::text = ANY ((ARRAY['postulado'::character varying, 'preseleccionado'::character varying, 'en_evaluacion'::character varying, 'en_entrevista'::character varying, 'finalista'::character varying, 'seleccionado'::character varying, 'no_seleccionado'::character varying, 'descartado'::character varying])::text[])))
);

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE applications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE applications_id_seq OWNED BY applications.id;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE audit_logs (
    id bigint NOT NULL,
    organization_id bigint,
    user_id bigint,
    action character varying(80) NOT NULL,
    auditable_type character varying(60) NOT NULL,
    auditable_id bigint NOT NULL,
    metadata jsonb,
    ip_address character varying(45),
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE audit_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE audit_logs_id_seq OWNED BY audit_logs.id;

--
-- Name: cache; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE cache (
    key character varying(255) NOT NULL,
    value text NOT NULL,
    expiration bigint NOT NULL
);

--
-- Name: cache_locks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE cache_locks (
    key character varying(255) NOT NULL,
    owner character varying(255) NOT NULL,
    expiration bigint NOT NULL
);

--
-- Name: candidate_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE candidate_documents (
    id bigint NOT NULL,
    candidate_profile_id bigint NOT NULL,
    type character varying(20) NOT NULL,
    original_name character varying(255) NOT NULL,
    stored_path character varying(255) NOT NULL,
    mime_type character varying(100) NOT NULL,
    size_bytes integer NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT candidate_documents_size_positive CHECK ((size_bytes > 0)),
    CONSTRAINT candidate_documents_type_valid CHECK (((type)::text = 'cv'::text))
);

--
-- Name: candidate_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE candidate_documents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: candidate_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE candidate_documents_id_seq OWNED BY candidate_documents.id;

--
-- Name: candidate_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE candidate_profiles (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    phone character varying(20),
    city character varying(80),
    education_level character varying(20),
    professional_title character varying(150),
    years_of_experience smallint,
    summary text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT candidate_profiles_education_valid CHECK (((education_level IS NULL) OR ((education_level)::text = ANY ((ARRAY['secundaria'::character varying, 'tecnico'::character varying, 'bachiller'::character varying, 'titulado'::character varying, 'maestria'::character varying, 'doctorado'::character varying])::text[])))),
    CONSTRAINT candidate_profiles_experience_range CHECK (((years_of_experience IS NULL) OR ((years_of_experience >= 0) AND (years_of_experience <= 60))))
);

--
-- Name: candidate_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE candidate_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: candidate_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE candidate_profiles_id_seq OWNED BY candidate_profiles.id;

--
-- Name: evaluation_criteria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE evaluation_criteria (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    vacancy_id bigint NOT NULL,
    name character varying(120) NOT NULL,
    stage character varying(20) NOT NULL,
    weight numeric(6,2) NOT NULL,
    min_score numeric(6,2) NOT NULL,
    max_score numeric(6,2) NOT NULL,
    "position" smallint DEFAULT '0'::smallint NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT evaluation_criteria_range_valid CHECK (((min_score >= (0)::numeric) AND (max_score > min_score))),
    CONSTRAINT evaluation_criteria_stage_valid CHECK (((stage)::text = ANY ((ARRAY['evaluacion'::character varying, 'entrevista'::character varying])::text[]))),
    CONSTRAINT evaluation_criteria_weight_positive CHECK ((weight > (0)::numeric))
);

--
-- Name: evaluation_criteria_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE evaluation_criteria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: evaluation_criteria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE evaluation_criteria_id_seq OWNED BY evaluation_criteria.id;

--
-- Name: evaluation_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE evaluation_results (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    evaluation_id bigint NOT NULL,
    evaluation_criterion_id bigint NOT NULL,
    score numeric(6,2) NOT NULL,
    comment character varying(500),
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT evaluation_results_score_non_negative CHECK ((score >= (0)::numeric))
);

--
-- Name: evaluation_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE evaluation_results_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: evaluation_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE evaluation_results_id_seq OWNED BY evaluation_results.id;

--
-- Name: evaluations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE evaluations (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    application_id bigint NOT NULL,
    evaluator_id bigint NOT NULL,
    scheduled_by bigint NOT NULL,
    type character varying(20) NOT NULL,
    modality character varying(20) NOT NULL,
    location character varying(200) NOT NULL,
    scheduled_at timestamp(0) without time zone NOT NULL,
    duration_minutes smallint,
    instructions text,
    status character varying(20) DEFAULT 'programada'::character varying NOT NULL,
    invitation_sent_at timestamp(0) without time zone,
    completed_at timestamp(0) without time zone,
    observations text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT evaluations_completion_consistent CHECK ((((status)::text = 'realizada'::text) = (completed_at IS NOT NULL))),
    CONSTRAINT evaluations_duration_range CHECK (((duration_minutes IS NULL) OR ((duration_minutes >= 15) AND (duration_minutes <= 480)))),
    CONSTRAINT evaluations_modality_valid CHECK (((modality)::text = ANY ((ARRAY['presencial'::character varying, 'virtual'::character varying])::text[]))),
    CONSTRAINT evaluations_status_valid CHECK (((status)::text = ANY ((ARRAY['programada'::character varying, 'realizada'::character varying])::text[]))),
    CONSTRAINT evaluations_type_valid CHECK (((type)::text = ANY ((ARRAY['conocimientos'::character varying, 'clase_modelo'::character varying, 'practica'::character varying, 'otra'::character varying])::text[])))
);

--
-- Name: evaluations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE evaluations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: evaluations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE evaluations_id_seq OWNED BY evaluations.id;

--
-- Name: failed_jobs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE failed_jobs (
    id bigint NOT NULL,
    uuid character varying(255) NOT NULL,
    connection character varying(255) NOT NULL,
    queue character varying(255) NOT NULL,
    payload text NOT NULL,
    exception text NOT NULL,
    failed_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

--
-- Name: failed_jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE failed_jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: failed_jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE failed_jobs_id_seq OWNED BY failed_jobs.id;

--
-- Name: interview_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE interview_results (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    interview_id bigint NOT NULL,
    evaluation_criterion_id bigint NOT NULL,
    score numeric(6,2) NOT NULL,
    comment character varying(500),
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT interview_results_score_non_negative CHECK ((score >= (0)::numeric))
);

--
-- Name: interview_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE interview_results_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: interview_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE interview_results_id_seq OWNED BY interview_results.id;

--
-- Name: interviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE interviews (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    application_id bigint NOT NULL,
    evaluator_id bigint NOT NULL,
    scheduled_by bigint NOT NULL,
    modality character varying(20) NOT NULL,
    location character varying(200) NOT NULL,
    scheduled_at timestamp(0) without time zone NOT NULL,
    duration_minutes smallint,
    instructions text,
    status character varying(20) DEFAULT 'programada'::character varying NOT NULL,
    outcome character varying(30),
    invitation_sent_at timestamp(0) without time zone,
    completed_at timestamp(0) without time zone,
    observations text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT interviews_duration_range CHECK (((duration_minutes IS NULL) OR ((duration_minutes >= 15) AND (duration_minutes <= 480)))),
    CONSTRAINT interviews_modality_valid CHECK (((modality)::text = ANY ((ARRAY['presencial'::character varying, 'virtual'::character varying])::text[]))),
    CONSTRAINT interviews_outcome_valid CHECK (((outcome IS NULL) OR ((outcome)::text = ANY ((ARRAY['recomendado'::character varying, 'recomendado_con_reservas'::character varying, 'no_recomendado'::character varying])::text[])))),
    CONSTRAINT interviews_status_consistent CHECK (((((status)::text = 'programada'::text) AND (completed_at IS NULL) AND (outcome IS NULL)) OR (((status)::text = 'realizada'::text) AND (completed_at IS NOT NULL) AND (outcome IS NOT NULL))))
);

--
-- Name: interviews_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE interviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: interviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE interviews_id_seq OWNED BY interviews.id;

--
-- Name: job_batches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE job_batches (
    id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    total_jobs integer NOT NULL,
    pending_jobs integer NOT NULL,
    failed_jobs integer NOT NULL,
    failed_job_ids text NOT NULL,
    options text,
    cancelled_at integer,
    created_at integer NOT NULL,
    finished_at integer
);

--
-- Name: job_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE job_profiles (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    vacancy_id bigint NOT NULL,
    education character varying(200) NOT NULL,
    experience character varying(200) NOT NULL,
    functions text NOT NULL,
    competencies text NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);

--
-- Name: job_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE job_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: job_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE job_profiles_id_seq OWNED BY job_profiles.id;

--
-- Name: job_request_status_histories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE job_request_status_histories (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    job_request_id bigint NOT NULL,
    from_status character varying(20),
    to_status character varying(20) NOT NULL,
    changed_by bigint NOT NULL,
    comment text,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

--
-- Name: job_request_status_histories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE job_request_status_histories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: job_request_status_histories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE job_request_status_histories_id_seq OWNED BY job_request_status_histories.id;

--
-- Name: job_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE job_requests (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    requested_by bigint NOT NULL,
    code character varying(20) NOT NULL,
    position_title character varying(150) NOT NULL,
    area character varying(120) NOT NULL,
    headcount smallint NOT NULL,
    contract_type character varying(20) NOT NULL,
    justification text NOT NULL,
    required_by date,
    status character varying(20) DEFAULT 'borrador'::character varying NOT NULL,
    observation text,
    submitted_at timestamp(0) without time zone,
    validated_by bigint,
    validated_at timestamp(0) without time zone,
    decided_by bigint,
    decided_at timestamp(0) without time zone,
    decision_comment text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT job_requests_contract_type_valid CHECK (((contract_type)::text = ANY ((ARRAY['tiempo_completo'::character varying, 'tiempo_parcial'::character varying, 'por_horas'::character varying, 'plazo_fijo'::character varying])::text[]))),
    CONSTRAINT job_requests_headcount_positive CHECK ((headcount >= 1)),
    CONSTRAINT job_requests_status_valid CHECK (((status)::text = ANY ((ARRAY['borrador'::character varying, 'enviado'::character varying, 'observado'::character varying, 'validado'::character varying, 'aprobado'::character varying, 'rechazado'::character varying])::text[])))
);

--
-- Name: job_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE job_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: job_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE job_requests_id_seq OWNED BY job_requests.id;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE jobs (
    id bigint NOT NULL,
    queue character varying(255) NOT NULL,
    payload text NOT NULL,
    attempts smallint NOT NULL,
    reserved_at integer,
    available_at integer NOT NULL,
    created_at integer NOT NULL
);

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE jobs_id_seq OWNED BY jobs.id;

--
-- Name: migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE migrations (
    id integer NOT NULL,
    migration character varying(255) NOT NULL,
    batch integer NOT NULL
);

--
-- Name: migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE migrations_id_seq OWNED BY migrations.id;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE notifications (
    id uuid NOT NULL,
    type character varying(255) NOT NULL,
    notifiable_type character varying(255) NOT NULL,
    notifiable_id bigint NOT NULL,
    data jsonb NOT NULL,
    read_at timestamp(0) without time zone,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE organizations (
    id bigint NOT NULL,
    name character varying(150) NOT NULL,
    slug character varying(80) NOT NULL,
    tax_id character varying(20),
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE organizations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE organizations_id_seq OWNED BY organizations.id;

--
-- Name: passkeys; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE passkeys (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    name character varying(255) NOT NULL,
    credential_id character varying(255) NOT NULL,
    credential json NOT NULL,
    last_used_at timestamp(0) without time zone,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);

--
-- Name: passkeys_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE passkeys_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: passkeys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE passkeys_id_seq OWNED BY passkeys.id;

--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE password_reset_tokens (
    email character varying(255) NOT NULL,
    token character varying(255) NOT NULL,
    created_at timestamp(0) without time zone
);

--
-- Name: selection_decisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE selection_decisions (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    vacancy_id bigint NOT NULL,
    selected_application_id bigint NOT NULL,
    decided_by bigint NOT NULL,
    justification text NOT NULL,
    selected_position smallint NOT NULL,
    selected_score numeric(6,2) NOT NULL,
    ranked_candidates smallint NOT NULL,
    decided_at timestamp(0) without time zone NOT NULL,
    selection_registered_by bigint,
    selection_registered_at timestamp(0) without time zone,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT selection_decisions_position_valid CHECK (((selected_position >= 1) AND (ranked_candidates >= selected_position))),
    CONSTRAINT selection_decisions_registration_consistent CHECK (((selection_registered_by IS NULL) = (selection_registered_at IS NULL))),
    CONSTRAINT selection_decisions_score_range CHECK (((selected_score >= (0)::numeric) AND (selected_score <= (100)::numeric)))
);

--
-- Name: selection_decisions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE selection_decisions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: selection_decisions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE selection_decisions_id_seq OWNED BY selection_decisions.id;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE sessions (
    id character varying(255) NOT NULL,
    user_id bigint,
    ip_address character varying(45),
    user_agent text,
    payload text NOT NULL,
    last_activity integer NOT NULL
);

--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE users (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    email_verified_at timestamp(0) without time zone,
    password character varying(255) NOT NULL,
    remember_token character varying(100),
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    two_factor_secret text,
    two_factor_recovery_codes text,
    two_factor_confirmed_at timestamp(0) without time zone,
    organization_id bigint,
    role character varying(20) DEFAULT 'postulante'::character varying NOT NULL,
    CONSTRAINT users_role_organization CHECK (((((role)::text = 'postulante'::text) AND (organization_id IS NULL)) OR (((role)::text <> 'postulante'::text) AND (organization_id IS NOT NULL)))),
    CONSTRAINT users_role_valid CHECK (((role)::text = ANY ((ARRAY['solicitante'::character varying, 'rrhh'::character varying, 'aprobador'::character varying, 'evaluador'::character varying, 'postulante'::character varying])::text[])))
);

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;

--
-- Name: vacancies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE vacancies (
    id bigint NOT NULL,
    organization_id bigint NOT NULL,
    job_request_id bigint NOT NULL,
    code character varying(20) NOT NULL,
    title character varying(150) NOT NULL,
    summary text NOT NULL,
    location character varying(120) NOT NULL,
    contract_type character varying(20) NOT NULL,
    positions smallint NOT NULL,
    opens_at date,
    closes_at date,
    status character varying(20) DEFAULT 'borrador'::character varying NOT NULL,
    created_by bigint NOT NULL,
    published_by bigint,
    published_at timestamp(0) without time zone,
    closed_by bigint,
    closed_at timestamp(0) without time zone,
    closure_type character varying(20),
    closure_notes text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    target_completion_at timestamp(0) without time zone,
    CONSTRAINT vacancies_closure_consistent CHECK (((((status)::text = 'cerrada'::text) AND (closed_at IS NOT NULL) AND ((closure_type)::text = ANY ((ARRAY['con_seleccion'::character varying, 'desierta'::character varying])::text[]))) OR (((status)::text <> 'cerrada'::text) AND (closure_type IS NULL)))),
    CONSTRAINT vacancies_dates_consistent CHECK (((opens_at IS NULL) OR (closes_at IS NULL) OR (closes_at >= opens_at))),
    CONSTRAINT vacancies_positions_positive CHECK ((positions >= 1)),
    CONSTRAINT vacancies_status_valid CHECK (((status)::text = ANY ((ARRAY['borrador'::character varying, 'publicada'::character varying, 'cerrada'::character varying])::text[]))),
    CONSTRAINT vacancies_target_after_close CHECK (((target_completion_at IS NULL) OR (closes_at IS NULL) OR (target_completion_at > closes_at)))
);

--
-- Name: vacancies_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE vacancies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: vacancies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE vacancies_id_seq OWNED BY vacancies.id;

--
-- Name: application_stage_histories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE application_stage_histories ALTER COLUMN id SET DEFAULT nextval('application_stage_histories_id_seq'::regclass);

--
-- Name: applications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE applications ALTER COLUMN id SET DEFAULT nextval('applications_id_seq'::regclass);

--
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE audit_logs ALTER COLUMN id SET DEFAULT nextval('audit_logs_id_seq'::regclass);

--
-- Name: candidate_documents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE candidate_documents ALTER COLUMN id SET DEFAULT nextval('candidate_documents_id_seq'::regclass);

--
-- Name: candidate_profiles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE candidate_profiles ALTER COLUMN id SET DEFAULT nextval('candidate_profiles_id_seq'::regclass);

--
-- Name: evaluation_criteria id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE evaluation_criteria ALTER COLUMN id SET DEFAULT nextval('evaluation_criteria_id_seq'::regclass);

--
-- Name: evaluation_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE evaluation_results ALTER COLUMN id SET DEFAULT nextval('evaluation_results_id_seq'::regclass);

--
-- Name: evaluations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE evaluations ALTER COLUMN id SET DEFAULT nextval('evaluations_id_seq'::regclass);

--
-- Name: failed_jobs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE failed_jobs ALTER COLUMN id SET DEFAULT nextval('failed_jobs_id_seq'::regclass);

--
-- Name: interview_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE interview_results ALTER COLUMN id SET DEFAULT nextval('interview_results_id_seq'::regclass);

--
-- Name: interviews id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE interviews ALTER COLUMN id SET DEFAULT nextval('interviews_id_seq'::regclass);

--
-- Name: job_profiles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE job_profiles ALTER COLUMN id SET DEFAULT nextval('job_profiles_id_seq'::regclass);

--
-- Name: job_request_status_histories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE job_request_status_histories ALTER COLUMN id SET DEFAULT nextval('job_request_status_histories_id_seq'::regclass);

--
-- Name: job_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE job_requests ALTER COLUMN id SET DEFAULT nextval('job_requests_id_seq'::regclass);

--
-- Name: jobs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE jobs ALTER COLUMN id SET DEFAULT nextval('jobs_id_seq'::regclass);

--
-- Name: migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE migrations ALTER COLUMN id SET DEFAULT nextval('migrations_id_seq'::regclass);

--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE organizations ALTER COLUMN id SET DEFAULT nextval('organizations_id_seq'::regclass);

--
-- Name: passkeys id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE passkeys ALTER COLUMN id SET DEFAULT nextval('passkeys_id_seq'::regclass);

--
-- Name: selection_decisions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions ALTER COLUMN id SET DEFAULT nextval('selection_decisions_id_seq'::regclass);

--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

--
-- Name: vacancies id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE vacancies ALTER COLUMN id SET DEFAULT nextval('vacancies_id_seq'::regclass);

--
-- Name: application_stage_histories application_stage_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE application_stage_histories
    ADD CONSTRAINT application_stage_histories_pkey PRIMARY KEY (id);

--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);

--
-- Name: applications applications_vacancy_id_candidate_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE applications
    ADD CONSTRAINT applications_vacancy_id_candidate_id_unique UNIQUE (vacancy_id, candidate_id);

--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);

--
-- Name: cache_locks cache_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE cache_locks
    ADD CONSTRAINT cache_locks_pkey PRIMARY KEY (key);

--
-- Name: cache cache_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE cache
    ADD CONSTRAINT cache_pkey PRIMARY KEY (key);

--
-- Name: candidate_documents candidate_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE candidate_documents
    ADD CONSTRAINT candidate_documents_pkey PRIMARY KEY (id);

--
-- Name: candidate_documents candidate_documents_stored_path_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE candidate_documents
    ADD CONSTRAINT candidate_documents_stored_path_unique UNIQUE (stored_path);

--
-- Name: candidate_profiles candidate_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE candidate_profiles
    ADD CONSTRAINT candidate_profiles_pkey PRIMARY KEY (id);

--
-- Name: candidate_profiles candidate_profiles_user_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE candidate_profiles
    ADD CONSTRAINT candidate_profiles_user_id_unique UNIQUE (user_id);

--
-- Name: evaluation_criteria evaluation_criteria_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_criteria
    ADD CONSTRAINT evaluation_criteria_pkey PRIMARY KEY (id);

--
-- Name: evaluation_criteria evaluation_criteria_vacancy_id_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_criteria
    ADD CONSTRAINT evaluation_criteria_vacancy_id_name_unique UNIQUE (vacancy_id, name);

--
-- Name: evaluation_results evaluation_results_evaluation_id_evaluation_criterion_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_results
    ADD CONSTRAINT evaluation_results_evaluation_id_evaluation_criterion_id_unique UNIQUE (evaluation_id, evaluation_criterion_id);

--
-- Name: evaluation_results evaluation_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_results
    ADD CONSTRAINT evaluation_results_pkey PRIMARY KEY (id);

--
-- Name: evaluations evaluations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluations
    ADD CONSTRAINT evaluations_pkey PRIMARY KEY (id);

--
-- Name: failed_jobs failed_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE failed_jobs
    ADD CONSTRAINT failed_jobs_pkey PRIMARY KEY (id);

--
-- Name: failed_jobs failed_jobs_uuid_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE failed_jobs
    ADD CONSTRAINT failed_jobs_uuid_unique UNIQUE (uuid);

--
-- Name: interview_results interview_results_interview_id_evaluation_criterion_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interview_results
    ADD CONSTRAINT interview_results_interview_id_evaluation_criterion_id_unique UNIQUE (interview_id, evaluation_criterion_id);

--
-- Name: interview_results interview_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interview_results
    ADD CONSTRAINT interview_results_pkey PRIMARY KEY (id);

--
-- Name: interviews interviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interviews
    ADD CONSTRAINT interviews_pkey PRIMARY KEY (id);

--
-- Name: job_batches job_batches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_batches
    ADD CONSTRAINT job_batches_pkey PRIMARY KEY (id);

--
-- Name: job_profiles job_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_profiles
    ADD CONSTRAINT job_profiles_pkey PRIMARY KEY (id);

--
-- Name: job_profiles job_profiles_vacancy_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_profiles
    ADD CONSTRAINT job_profiles_vacancy_id_unique UNIQUE (vacancy_id);

--
-- Name: job_request_status_histories job_request_status_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_request_status_histories
    ADD CONSTRAINT job_request_status_histories_pkey PRIMARY KEY (id);

--
-- Name: job_requests job_requests_organization_id_code_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_requests
    ADD CONSTRAINT job_requests_organization_id_code_unique UNIQUE (organization_id, code);

--
-- Name: job_requests job_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_requests
    ADD CONSTRAINT job_requests_pkey PRIMARY KEY (id);

--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);

--
-- Name: migrations migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE migrations
    ADD CONSTRAINT migrations_pkey PRIMARY KEY (id);

--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);

--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);

--
-- Name: organizations organizations_slug_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE organizations
    ADD CONSTRAINT organizations_slug_unique UNIQUE (slug);

--
-- Name: organizations organizations_tax_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE organizations
    ADD CONSTRAINT organizations_tax_id_unique UNIQUE (tax_id);

--
-- Name: passkeys passkeys_credential_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE passkeys
    ADD CONSTRAINT passkeys_credential_id_unique UNIQUE (credential_id);

--
-- Name: passkeys passkeys_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE passkeys
    ADD CONSTRAINT passkeys_pkey PRIMARY KEY (id);

--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (email);

--
-- Name: selection_decisions selection_decisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_pkey PRIMARY KEY (id);

--
-- Name: selection_decisions selection_decisions_vacancy_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_vacancy_id_unique UNIQUE (vacancy_id);

--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);

--
-- Name: users users_email_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE users
    ADD CONSTRAINT users_email_unique UNIQUE (email);

--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

--
-- Name: vacancies vacancies_job_request_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_job_request_id_unique UNIQUE (job_request_id);

--
-- Name: vacancies vacancies_organization_id_code_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_organization_id_code_unique UNIQUE (organization_id, code);

--
-- Name: vacancies vacancies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_pkey PRIMARY KEY (id);

--
-- Name: application_stage_histories_application_id_created_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX application_stage_histories_application_id_created_at_index ON application_stage_histories USING btree (application_id, created_at);

--
-- Name: applications_candidate_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX applications_candidate_id_index ON applications USING btree (candidate_id);

--
-- Name: applications_one_selected_per_vacancy; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX applications_one_selected_per_vacancy ON applications USING btree (vacancy_id) WHERE ((status)::text = 'seleccionado'::text);

--
-- Name: applications_organization_id_status_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX applications_organization_id_status_index ON applications USING btree (organization_id, status);

--
-- Name: applications_vacancy_id_status_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX applications_vacancy_id_status_index ON applications USING btree (vacancy_id, status);

--
-- Name: audit_logs_action_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_action_index ON audit_logs USING btree (action);

--
-- Name: audit_logs_auditable_type_auditable_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_auditable_type_auditable_id_index ON audit_logs USING btree (auditable_type, auditable_id);

--
-- Name: audit_logs_organization_id_created_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_logs_organization_id_created_at_index ON audit_logs USING btree (organization_id, created_at);

--
-- Name: cache_expiration_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cache_expiration_index ON cache USING btree (expiration);

--
-- Name: cache_locks_expiration_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cache_locks_expiration_index ON cache_locks USING btree (expiration);

--
-- Name: candidate_documents_candidate_profile_id_type_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX candidate_documents_candidate_profile_id_type_index ON candidate_documents USING btree (candidate_profile_id, type);

--
-- Name: evaluations_application_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX evaluations_application_id_index ON evaluations USING btree (application_id);

--
-- Name: evaluations_evaluator_id_status_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX evaluations_evaluator_id_status_index ON evaluations USING btree (evaluator_id, status);

--
-- Name: evaluations_organization_id_scheduled_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX evaluations_organization_id_scheduled_at_index ON evaluations USING btree (organization_id, scheduled_at);

--
-- Name: failed_jobs_connection_queue_failed_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX failed_jobs_connection_queue_failed_at_index ON failed_jobs USING btree (connection, queue, failed_at);

--
-- Name: interviews_application_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interviews_application_id_index ON interviews USING btree (application_id);

--
-- Name: interviews_evaluator_id_status_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interviews_evaluator_id_status_index ON interviews USING btree (evaluator_id, status);

--
-- Name: interviews_organization_id_scheduled_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX interviews_organization_id_scheduled_at_index ON interviews USING btree (organization_id, scheduled_at);

--
-- Name: job_request_status_histories_job_request_id_created_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX job_request_status_histories_job_request_id_created_at_index ON job_request_status_histories USING btree (job_request_id, created_at);

--
-- Name: job_requests_organization_id_status_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX job_requests_organization_id_status_index ON job_requests USING btree (organization_id, status);

--
-- Name: job_requests_requested_by_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX job_requests_requested_by_index ON job_requests USING btree (requested_by);

--
-- Name: jobs_queue_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX jobs_queue_index ON jobs USING btree (queue);

--
-- Name: notifications_notifiable_type_notifiable_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX notifications_notifiable_type_notifiable_id_index ON notifications USING btree (notifiable_type, notifiable_id);

--
-- Name: notifications_notifiable_type_notifiable_id_read_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX notifications_notifiable_type_notifiable_id_read_at_index ON notifications USING btree (notifiable_type, notifiable_id, read_at);

--
-- Name: passkeys_user_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX passkeys_user_id_index ON passkeys USING btree (user_id);

--
-- Name: selection_decisions_organization_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX selection_decisions_organization_id_index ON selection_decisions USING btree (organization_id);

--
-- Name: sessions_last_activity_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sessions_last_activity_index ON sessions USING btree (last_activity);

--
-- Name: sessions_user_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sessions_user_id_index ON sessions USING btree (user_id);

--
-- Name: users_organization_id_role_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_organization_id_role_index ON users USING btree (organization_id, role);

--
-- Name: vacancies_organization_id_status_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vacancies_organization_id_status_index ON vacancies USING btree (organization_id, status);

--
-- Name: vacancies_status_closes_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vacancies_status_closes_at_index ON vacancies USING btree (status, closes_at);

--
-- Name: audit_logs audit_logs_append_only; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER audit_logs_append_only BEFORE DELETE OR UPDATE ON audit_logs FOR EACH ROW EXECUTE PROCEDURE audit_logs_append_only();

--
-- Name: application_stage_histories application_stage_histories_application_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE application_stage_histories
    ADD CONSTRAINT application_stage_histories_application_id_foreign FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE;

--
-- Name: application_stage_histories application_stage_histories_changed_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE application_stage_histories
    ADD CONSTRAINT application_stage_histories_changed_by_foreign FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: application_stage_histories application_stage_histories_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE application_stage_histories
    ADD CONSTRAINT application_stage_histories_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: applications applications_candidate_document_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE applications
    ADD CONSTRAINT applications_candidate_document_id_foreign FOREIGN KEY (candidate_document_id) REFERENCES candidate_documents(id) ON DELETE RESTRICT;

--
-- Name: applications applications_candidate_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE applications
    ADD CONSTRAINT applications_candidate_id_foreign FOREIGN KEY (candidate_id) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: applications applications_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE applications
    ADD CONSTRAINT applications_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: applications applications_vacancy_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE applications
    ADD CONSTRAINT applications_vacancy_id_foreign FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE RESTRICT;

--
-- Name: audit_logs audit_logs_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE audit_logs
    ADD CONSTRAINT audit_logs_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: audit_logs audit_logs_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE audit_logs
    ADD CONSTRAINT audit_logs_user_id_foreign FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;

--
-- Name: candidate_documents candidate_documents_candidate_profile_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE candidate_documents
    ADD CONSTRAINT candidate_documents_candidate_profile_id_foreign FOREIGN KEY (candidate_profile_id) REFERENCES candidate_profiles(id) ON DELETE CASCADE;

--
-- Name: candidate_profiles candidate_profiles_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE candidate_profiles
    ADD CONSTRAINT candidate_profiles_user_id_foreign FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

--
-- Name: evaluation_criteria evaluation_criteria_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_criteria
    ADD CONSTRAINT evaluation_criteria_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: evaluation_criteria evaluation_criteria_vacancy_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_criteria
    ADD CONSTRAINT evaluation_criteria_vacancy_id_foreign FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE;

--
-- Name: evaluation_results evaluation_results_evaluation_criterion_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_results
    ADD CONSTRAINT evaluation_results_evaluation_criterion_id_foreign FOREIGN KEY (evaluation_criterion_id) REFERENCES evaluation_criteria(id) ON DELETE RESTRICT;

--
-- Name: evaluation_results evaluation_results_evaluation_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_results
    ADD CONSTRAINT evaluation_results_evaluation_id_foreign FOREIGN KEY (evaluation_id) REFERENCES evaluations(id) ON DELETE CASCADE;

--
-- Name: evaluation_results evaluation_results_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluation_results
    ADD CONSTRAINT evaluation_results_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: evaluations evaluations_application_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluations
    ADD CONSTRAINT evaluations_application_id_foreign FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE RESTRICT;

--
-- Name: evaluations evaluations_evaluator_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluations
    ADD CONSTRAINT evaluations_evaluator_id_foreign FOREIGN KEY (evaluator_id) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: evaluations evaluations_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluations
    ADD CONSTRAINT evaluations_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: evaluations evaluations_scheduled_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE evaluations
    ADD CONSTRAINT evaluations_scheduled_by_foreign FOREIGN KEY (scheduled_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: interview_results interview_results_evaluation_criterion_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interview_results
    ADD CONSTRAINT interview_results_evaluation_criterion_id_foreign FOREIGN KEY (evaluation_criterion_id) REFERENCES evaluation_criteria(id) ON DELETE RESTRICT;

--
-- Name: interview_results interview_results_interview_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interview_results
    ADD CONSTRAINT interview_results_interview_id_foreign FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE;

--
-- Name: interview_results interview_results_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interview_results
    ADD CONSTRAINT interview_results_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: interviews interviews_application_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interviews
    ADD CONSTRAINT interviews_application_id_foreign FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE RESTRICT;

--
-- Name: interviews interviews_evaluator_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interviews
    ADD CONSTRAINT interviews_evaluator_id_foreign FOREIGN KEY (evaluator_id) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: interviews interviews_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interviews
    ADD CONSTRAINT interviews_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: interviews interviews_scheduled_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE interviews
    ADD CONSTRAINT interviews_scheduled_by_foreign FOREIGN KEY (scheduled_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: job_profiles job_profiles_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_profiles
    ADD CONSTRAINT job_profiles_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: job_profiles job_profiles_vacancy_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_profiles
    ADD CONSTRAINT job_profiles_vacancy_id_foreign FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE;

--
-- Name: job_request_status_histories job_request_status_histories_changed_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_request_status_histories
    ADD CONSTRAINT job_request_status_histories_changed_by_foreign FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: job_request_status_histories job_request_status_histories_job_request_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_request_status_histories
    ADD CONSTRAINT job_request_status_histories_job_request_id_foreign FOREIGN KEY (job_request_id) REFERENCES job_requests(id) ON DELETE CASCADE;

--
-- Name: job_request_status_histories job_request_status_histories_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_request_status_histories
    ADD CONSTRAINT job_request_status_histories_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: job_requests job_requests_decided_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_requests
    ADD CONSTRAINT job_requests_decided_by_foreign FOREIGN KEY (decided_by) REFERENCES users(id) ON DELETE SET NULL;

--
-- Name: job_requests job_requests_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_requests
    ADD CONSTRAINT job_requests_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: job_requests job_requests_requested_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_requests
    ADD CONSTRAINT job_requests_requested_by_foreign FOREIGN KEY (requested_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: job_requests job_requests_validated_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE job_requests
    ADD CONSTRAINT job_requests_validated_by_foreign FOREIGN KEY (validated_by) REFERENCES users(id) ON DELETE SET NULL;

--
-- Name: passkeys passkeys_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE passkeys
    ADD CONSTRAINT passkeys_user_id_foreign FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

--
-- Name: selection_decisions selection_decisions_decided_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_decided_by_foreign FOREIGN KEY (decided_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: selection_decisions selection_decisions_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: selection_decisions selection_decisions_selected_application_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_selected_application_id_foreign FOREIGN KEY (selected_application_id) REFERENCES applications(id) ON DELETE RESTRICT;

--
-- Name: selection_decisions selection_decisions_selection_registered_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_selection_registered_by_foreign FOREIGN KEY (selection_registered_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: selection_decisions selection_decisions_vacancy_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE selection_decisions
    ADD CONSTRAINT selection_decisions_vacancy_id_foreign FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE RESTRICT;

--
-- Name: users users_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE users
    ADD CONSTRAINT users_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: vacancies vacancies_closed_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_closed_by_foreign FOREIGN KEY (closed_by) REFERENCES users(id) ON DELETE SET NULL;

--
-- Name: vacancies vacancies_created_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_created_by_foreign FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;

--
-- Name: vacancies vacancies_job_request_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_job_request_id_foreign FOREIGN KEY (job_request_id) REFERENCES job_requests(id) ON DELETE RESTRICT;

--
-- Name: vacancies vacancies_organization_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_organization_id_foreign FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE RESTRICT;

--
-- Name: vacancies vacancies_published_by_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE vacancies
    ADD CONSTRAINT vacancies_published_by_foreign FOREIGN KEY (published_by) REFERENCES users(id) ON DELETE SET NULL;

--
-- PostgreSQL database dump complete
--
