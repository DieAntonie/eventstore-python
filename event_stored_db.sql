--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-11-27 09:12:58

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4879 (class 1262 OID 5)
-- Name: postgres; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United Kingdom.1252';


ALTER DATABASE postgres OWNER TO postgres;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4880 (class 0 OID 0)
-- Dependencies: 4879
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- TOC entry 7 (class 2615 OID 16439)
-- Name: stored; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA stored;


ALTER SCHEMA stored OWNER TO postgres;

--
-- TOC entry 4881 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA stored; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA stored IS 'The `stored` schema serves as the designated namespace for maintaining the event-sourced data model. It organizes and encapsulates the tables related to event storage and management, ensuring a clear separation from other schemas in the database. This schema is specifically tailored to manage the persistence of immutable domain artifacts (events, commands, contexts) and their revisions, providing a foundation for versioning, auditability, and consistent state reconstruction in an event-driven architecture.';


--
-- TOC entry 233 (class 1255 OID 24714)
-- Name: auto_increment_context_version(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.auto_increment_context_version() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    max_version integer;
BEGIN
    -- Get the current maximum version for the context_id
    SELECT COALESCE(MAX(context_version), -1) INTO max_version
    FROM stored.context_revision
    WHERE context_id = NEW.context_id;

    -- Set the context_version to the next version
    NEW.context_version := max_version + 1;

    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.auto_increment_context_version() OWNER TO postgres;

--
-- TOC entry 232 (class 1255 OID 24712)
-- Name: create_context_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.create_context_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Insert a new context_revision entry for the new context
    INSERT INTO stored.context_revision (context_id)
    VALUES (NEW.context_id);
    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.create_context_revision() OWNER TO postgres;

--
-- TOC entry 236 (class 1255 OID 24720)
-- Name: create_instance_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.create_instance_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Insert a new instance_revision entry with version 1 and the latest context version
    INSERT INTO stored.instance_revision (instance_id, context_version)
    SELECT NEW.instance_id, MAX(context_version)
    FROM stored.context_revision
    WHERE context_id = NEW.context_id;

    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.create_instance_revision() OWNER TO postgres;

--
-- TOC entry 249 (class 1255 OID 24724)
-- Name: disallow_update_delete_aggregate_instance(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.disallow_update_delete_aggregate_instance() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'UPDATE or DELETE operations are not allowed on aggregate_instance';
END;
$$;


ALTER FUNCTION stored.disallow_update_delete_aggregate_instance() OWNER TO postgres;

--
-- TOC entry 235 (class 1255 OID 24718)
-- Name: disallow_update_delete_context_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.disallow_update_delete_context_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'UPDATE or DELETE operations are not allowed on context_revision';
END;
$$;


ALTER FUNCTION stored.disallow_update_delete_context_revision() OWNER TO postgres;

--
-- TOC entry 234 (class 1255 OID 24716)
-- Name: disallow_update_delete_domain_context(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.disallow_update_delete_domain_context() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'UPDATE or DELETE operations are not allowed on domain_context';
END;
$$;


ALTER FUNCTION stored.disallow_update_delete_domain_context() OWNER TO postgres;

--
-- TOC entry 250 (class 1255 OID 24726)
-- Name: disallow_update_delete_instance_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.disallow_update_delete_instance_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'UPDATE or DELETE operations are not allowed on instance_revision';
END;
$$;


ALTER FUNCTION stored.disallow_update_delete_instance_revision() OWNER TO postgres;

--
-- TOC entry 248 (class 1255 OID 24722)
-- Name: validate_instance_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.validate_instance_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    is_valid_version boolean;
    latest_context_version integer;
    max_version integer;
BEGIN
    -- Get the latest context_version for the associated bounded_context
    SELECT MAX(context_version) INTO latest_context_version
    FROM stored.context_revision
    WHERE context_id = (
        SELECT context_id
        FROM stored.aggregate_instance
        WHERE instance_id = NEW.instance_id
    );

    -- Check if the provided context_version exists in the version history
    SELECT EXISTS (
        SELECT 1
        FROM stored.context_revision
        WHERE context_version = NEW.context_version
          AND context_id = (
              SELECT context_id
              FROM stored.aggregate_instance
              WHERE instance_id = NEW.instance_id
          )
    ) INTO is_valid_version;

    -- Raise an error if the context_version is not valid
    IF NOT is_valid_version THEN
        RAISE EXCEPTION 'The provided context_version % is not within the version history of the domain context for this aggregate instance.',
            NEW.context_version;
    END IF;

    -- Raise a warning if the context_version is not the latest
    IF NEW.context_version <> latest_context_version THEN
        RAISE WARNING 'The provided context_version % is not the latest version (%).',
            NEW.context_version, latest_context_version;
    END IF;

    -- Get the current maximum version for the instance_id
    SELECT COALESCE(MAX(instance_version), 0) INTO max_version
    FROM stored.instance_revision
    WHERE instance_id = NEW.instance_id;

    -- Set the instance_version to the next version
    NEW.instance_version := max_version + 1;

    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.validate_instance_revision() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16464)
-- Name: aggregate_instance; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.aggregate_instance (
    instance_id integer NOT NULL,
    context_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE stored.aggregate_instance OWNER TO postgres;

--
-- TOC entry 4882 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE aggregate_instance; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.aggregate_instance IS 'Represents specific instances of aggregates within a bounded context, uniquely identifying domain entities.';


--
-- TOC entry 220 (class 1259 OID 16463)
-- Name: aggregate_instance_instance_id_seq; Type: SEQUENCE; Schema: stored; Owner: postgres
--

ALTER TABLE stored.aggregate_instance ALTER COLUMN instance_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME stored.aggregate_instance_instance_id_seq
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 218 (class 1259 OID 16441)
-- Name: bounded_context; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.bounded_context (
    context_id integer NOT NULL,
    context_name text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.bounded_context OWNER TO postgres;

--
-- TOC entry 4883 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE bounded_context; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.bounded_context IS 'Represents immutable definitions of bounded contexts within the system, ensuring clear separation and autonomy of domains.';


--
-- TOC entry 217 (class 1259 OID 16440)
-- Name: bounded_context_context_id_seq; Type: SEQUENCE; Schema: stored; Owner: postgres
--

ALTER TABLE stored.bounded_context ALTER COLUMN context_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME stored.bounded_context_context_id_seq
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 24652)
-- Name: command_log; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.command_log (
    command_log_id integer NOT NULL,
    command_id integer NOT NULL,
    command_version integer NOT NULL,
    command_data jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.command_log OWNER TO postgres;

--
-- TOC entry 4884 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE command_log; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.command_log IS 'Logs instances of domain commands executed against a bounded context, providing an audit trail and history of operations.';


--
-- TOC entry 226 (class 1259 OID 24651)
-- Name: command_log_command_log_id_seq; Type: SEQUENCE; Schema: stored; Owner: postgres
--

ALTER TABLE stored.command_log ALTER COLUMN command_log_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME stored.command_log_command_log_id_seq
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 24640)
-- Name: command_revision; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.command_revision (
    command_id integer NOT NULL,
    command_version integer NOT NULL,
    command_structure jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.command_revision OWNER TO postgres;

--
-- TOC entry 4885 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE command_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.command_revision IS 'Tracks updates to the structure or definition of domain commands, accommodating system evolution.';


--
-- TOC entry 219 (class 1259 OID 16449)
-- Name: context_revision; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.context_revision (
    context_id integer NOT NULL,
    context_version integer NOT NULL,
    context_structure jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.context_revision OWNER TO postgres;

--
-- TOC entry 4886 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE context_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.context_revision IS 'Tracks changes to the bounded context definitions over time, allowing for an evolving understanding of domain boundaries.';


--
-- TOC entry 224 (class 1259 OID 24632)
-- Name: domain_command; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.domain_command (
    command_id integer NOT NULL,
    command_name text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.domain_command OWNER TO postgres;

--
-- TOC entry 4887 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE domain_command; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.domain_command IS 'Represents distinct, immutable representations of domain commands that trigger domain logic and potential state changes.';


--
-- TOC entry 223 (class 1259 OID 24631)
-- Name: domain_command_command_id_seq; Type: SEQUENCE; Schema: stored; Owner: postgres
--

ALTER TABLE stored.domain_command ALTER COLUMN command_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME stored.domain_command_command_id_seq
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 229 (class 1259 OID 24666)
-- Name: domain_event; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.domain_event (
    event_id integer NOT NULL,
    event_name text NOT NULL,
    created_at time with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.domain_event OWNER TO postgres;

--
-- TOC entry 4888 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE domain_event; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.domain_event IS 'Stores distinct, immutable representations of domain events that signify meaningful changes within the domain.';


--
-- TOC entry 228 (class 1259 OID 24665)
-- Name: domain_event_event_id_seq; Type: SEQUENCE; Schema: stored; Owner: postgres
--

ALTER TABLE stored.domain_event ALTER COLUMN event_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME stored.domain_event_event_id_seq
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 24674)
-- Name: event_revision; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.event_revision (
    event_id integer NOT NULL,
    event_version integer NOT NULL,
    event_structure jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.event_revision OWNER TO postgres;

--
-- TOC entry 4889 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE event_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.event_revision IS 'Tracks revisions to the structure or definition of domain events over time, supporting schema evolution.';


--
-- TOC entry 231 (class 1259 OID 24685)
-- Name: event_stream; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.event_stream (
    instance_id integer NOT NULL,
    instance_version integer NOT NULL,
    event_id integer NOT NULL,
    event_version integer NOT NULL,
    stream_sequence integer NOT NULL,
    command_log_id integer NOT NULL,
    event_data jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.event_stream OWNER TO postgres;

--
-- TOC entry 4890 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE event_stream; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.event_stream IS 'Captures the sequence of domain events emitted by aggregate instances in response to logged commands, forming the core of the event-sourced state reconstruction.';


--
-- TOC entry 222 (class 1259 OID 16514)
-- Name: instance_revision; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.instance_revision (
    instance_id integer NOT NULL,
    instance_version integer NOT NULL,
    context_version integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.instance_revision OWNER TO postgres;

--
-- TOC entry 4891 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE instance_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.instance_revision IS 'Manages versioning for aggregate instances to align them with evolving bounded context definitions, ensuring consistency during changes.';


--
-- TOC entry 4699 (class 2606 OID 16511)
-- Name: aggregate_instance aggregate_instance_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.aggregate_instance
    ADD CONSTRAINT aggregate_instance_pkey PRIMARY KEY (instance_id);


--
-- TOC entry 4695 (class 2606 OID 16448)
-- Name: bounded_context bounded_context_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.bounded_context
    ADD CONSTRAINT bounded_context_pkey PRIMARY KEY (context_id);


--
-- TOC entry 4707 (class 2606 OID 24659)
-- Name: command_log command_log_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_log
    ADD CONSTRAINT command_log_pkey PRIMARY KEY (command_log_id);


--
-- TOC entry 4705 (class 2606 OID 24709)
-- Name: command_revision command_revision_command_id_command_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_revision
    ADD CONSTRAINT command_revision_command_id_command_version_key UNIQUE (command_id, command_version);


--
-- TOC entry 4697 (class 2606 OID 16526)
-- Name: context_revision context_revision_context_id_context_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.context_revision
    ADD CONSTRAINT context_revision_context_id_context_version_key UNIQUE (context_id, context_version);


--
-- TOC entry 4703 (class 2606 OID 24639)
-- Name: domain_command domain_command_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.domain_command
    ADD CONSTRAINT domain_command_pkey PRIMARY KEY (command_id);


--
-- TOC entry 4709 (class 2606 OID 24673)
-- Name: domain_event domain_event_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.domain_event
    ADD CONSTRAINT domain_event_pkey PRIMARY KEY (event_id);


--
-- TOC entry 4711 (class 2606 OID 24711)
-- Name: event_revision event_revision_event_id_event_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_revision
    ADD CONSTRAINT event_revision_event_id_event_version_key UNIQUE (event_id, event_version);


--
-- TOC entry 4713 (class 2606 OID 24692)
-- Name: event_stream event_stream_instance_id_instance_version_event_id_event_ve_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_instance_id_instance_version_event_id_event_ve_key UNIQUE (instance_id, instance_version, event_id, event_version, stream_sequence);


--
-- TOC entry 4701 (class 2606 OID 16519)
-- Name: instance_revision instance_version_instance_id_instance_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.instance_revision
    ADD CONSTRAINT instance_version_instance_id_instance_version_key UNIQUE (instance_id, instance_version);


--
-- TOC entry 4727 (class 2620 OID 24721)
-- Name: aggregate_instance after_insert_aggregate_instance; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER after_insert_aggregate_instance AFTER INSERT ON stored.aggregate_instance FOR EACH ROW EXECUTE FUNCTION stored.create_instance_revision();


--
-- TOC entry 4723 (class 2620 OID 24713)
-- Name: bounded_context after_insert_bounded_context; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER after_insert_bounded_context AFTER INSERT ON stored.bounded_context FOR EACH ROW EXECUTE FUNCTION stored.create_context_revision();


--
-- TOC entry 4725 (class 2620 OID 24715)
-- Name: context_revision before_insert_context_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_insert_context_revision BEFORE INSERT ON stored.context_revision FOR EACH ROW EXECUTE FUNCTION stored.auto_increment_context_version();


--
-- TOC entry 4729 (class 2620 OID 24723)
-- Name: instance_revision before_insert_validate_instance_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_insert_validate_instance_revision BEFORE INSERT ON stored.instance_revision FOR EACH ROW EXECUTE FUNCTION stored.validate_instance_revision();


--
-- TOC entry 4728 (class 2620 OID 24725)
-- Name: aggregate_instance prevent_update_delete_aggregate_instance; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_aggregate_instance BEFORE DELETE OR UPDATE ON stored.aggregate_instance FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_aggregate_instance();


--
-- TOC entry 4724 (class 2620 OID 24717)
-- Name: bounded_context prevent_update_delete_bounded_context; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_bounded_context BEFORE DELETE OR UPDATE ON stored.bounded_context FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_domain_context();


--
-- TOC entry 4726 (class 2620 OID 24719)
-- Name: context_revision prevent_update_delete_context_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_context_revision BEFORE DELETE OR UPDATE ON stored.context_revision FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_context_revision();


--
-- TOC entry 4730 (class 2620 OID 24727)
-- Name: instance_revision prevent_update_delete_instance_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_instance_revision BEFORE DELETE OR UPDATE ON stored.instance_revision FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_instance_revision();


--
-- TOC entry 4715 (class 2606 OID 16469)
-- Name: aggregate_instance aggregate_instance_context_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.aggregate_instance
    ADD CONSTRAINT aggregate_instance_context_id_fkey FOREIGN KEY (context_id) REFERENCES stored.bounded_context(context_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4718 (class 2606 OID 24660)
-- Name: command_log command_log_command_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_log
    ADD CONSTRAINT command_log_command_id_fkey FOREIGN KEY (command_id) REFERENCES stored.domain_command(command_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4717 (class 2606 OID 24646)
-- Name: command_revision command_revision_command_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_revision
    ADD CONSTRAINT command_revision_command_id_fkey FOREIGN KEY (command_id) REFERENCES stored.domain_command(command_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4714 (class 2606 OID 16458)
-- Name: context_revision context_revision_context_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.context_revision
    ADD CONSTRAINT context_revision_context_id_fkey FOREIGN KEY (context_id) REFERENCES stored.bounded_context(context_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4719 (class 2606 OID 24680)
-- Name: event_revision event_revision_event_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_revision
    ADD CONSTRAINT event_revision_event_id_fkey FOREIGN KEY (event_id) REFERENCES stored.domain_event(event_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4720 (class 2606 OID 24703)
-- Name: event_stream event_stream_command_log_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_command_log_id_fkey FOREIGN KEY (command_log_id) REFERENCES stored.command_log(command_log_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4721 (class 2606 OID 24698)
-- Name: event_stream event_stream_event_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_event_id_fkey FOREIGN KEY (event_id) REFERENCES stored.domain_event(event_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4722 (class 2606 OID 24693)
-- Name: event_stream event_stream_instance_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_instance_id_fkey FOREIGN KEY (instance_id) REFERENCES stored.aggregate_instance(instance_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4716 (class 2606 OID 16520)
-- Name: instance_revision instance_version_instance_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.instance_revision
    ADD CONSTRAINT instance_version_instance_id_fkey FOREIGN KEY (instance_id) REFERENCES stored.aggregate_instance(instance_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2024-11-27 09:12:59

--
-- PostgreSQL database dump complete
--

