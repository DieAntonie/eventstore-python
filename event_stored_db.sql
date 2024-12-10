--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2024-12-10 21:58:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16388)
-- Name: stored; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA stored;


ALTER SCHEMA stored OWNER TO postgres;

--
-- TOC entry 4909 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA stored; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA stored IS 'The `stored` schema serves as the designated namespace for maintaining the event-sourced data model. It organizes and encapsulates the tables related to event storage and management, ensuring a clear separation from other schemas in the database. This schema is specifically tailored to manage the persistence of immutable domain artifacts (events, commands, contexts) and their revisions, providing a foundation for versioning, auditability, and consistent state reconstruction in an event-driven architecture.';


--
-- TOC entry 241 (class 1255 OID 16535)
-- Name: auto_increment_command_version(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.auto_increment_command_version() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    latest_version integer;
BEGIN
    -- Fetch the latest command_version for this command_id
    SELECT COALESCE(MAX(command_version), -1) INTO latest_version
    FROM stored.command_revision
    WHERE command_id = NEW.command_id;

    -- Set the new command_version as the latest + 1
    NEW.command_version := latest_version + 1;

    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.auto_increment_command_version() OWNER TO postgres;

--
-- TOC entry 233 (class 1255 OID 16389)
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
-- TOC entry 243 (class 1255 OID 16549)
-- Name: auto_increment_event_version(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.auto_increment_event_version() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    latest_version integer;
BEGIN
    -- Fetch the latest event_version for this event_id
    SELECT COALESCE(MAX(event_version), -1) INTO latest_version
    FROM stored.event_revision
    WHERE event_id = NEW.event_id;

    -- Set the new event_version to the latest + 1
    NEW.event_version := latest_version + 1;

    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.auto_increment_event_version() OWNER TO postgres;

--
-- TOC entry 234 (class 1255 OID 16390)
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
-- TOC entry 240 (class 1255 OID 16533)
-- Name: create_initial_command_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.create_initial_command_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO stored.command_revision (command_id)
    VALUES (NEW.command_id); -- Default placeholder structure
    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.create_initial_command_revision() OWNER TO postgres;

--
-- TOC entry 242 (class 1255 OID 16547)
-- Name: create_initial_event_revision(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.create_initial_event_revision() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO stored.event_revision (event_id)
    VALUES (NEW.event_id);
    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.create_initial_event_revision() OWNER TO postgres;

--
-- TOC entry 235 (class 1255 OID 16391)
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
-- TOC entry 257 (class 1255 OID 16539)
-- Name: disallow_modifications(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.disallow_modifications() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'Updates and deletions are not allowed on this table.';
    RETURN NULL;
END;
$$;


ALTER FUNCTION stored.disallow_modifications() OWNER TO postgres;

--
-- TOC entry 236 (class 1255 OID 16392)
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
-- TOC entry 237 (class 1255 OID 16393)
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
-- TOC entry 238 (class 1255 OID 16394)
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
-- TOC entry 239 (class 1255 OID 16395)
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
-- TOC entry 256 (class 1255 OID 16537)
-- Name: validate_command_version(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.validate_command_version() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    is_valid_version boolean;
	latest_command_version integer;
BEGIN
    -- Get the latest command_version for the associated domain_command
    SELECT MAX(command_version) INTO latest_command_version
    FROM stored.command_revision
    WHERE command_id = NEW.command_id;

    -- Check if the provided command_version exists in the version history
    SELECT EXISTS (
        SELECT 1
        FROM stored.command_revision
        WHERE command_id = NEW.command_id
          AND NEW.command_version in (
              SELECT command_version
              FROM stored.command_revision
              WHERE command_id = NEW.command_id
          )
    ) INTO is_valid_version;

    -- Raise an error if the command_version is not valid
    IF NOT is_valid_version THEN
        RAISE EXCEPTION 'The provided command_version % is not within the version history of the domain command.',
            NEW.command_version;
    END IF;

    -- Raise a warning if the command_version is not the latest
    IF NEW.command_version <> latest_command_version THEN
        RAISE WARNING 'The provided command_version % is not the latest version (%).',
            NEW.command_version, latest_command_version;
    END IF;

RETURN NEW;
END;
$$;


ALTER FUNCTION stored.validate_command_version() OWNER TO postgres;

--
-- TOC entry 258 (class 1255 OID 16575)
-- Name: validate_event_stream(); Type: FUNCTION; Schema: stored; Owner: postgres
--

CREATE FUNCTION stored.validate_event_stream() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    latest_instance_version integer;
    earliest_instance_version integer;
    latest_event_version integer;
    earliest_event_version integer;
    max_sequence integer;
    error_messages text := ''; -- Variable to collect all error messages
BEGIN
    -- Get the latest instance_version for the associated aggregate_instance
    SELECT MAX(instance_version), MIN(instance_version)
	INTO latest_instance_version, earliest_instance_version
    FROM stored.instance_revision
    WHERE instance_id = NEW.instance_id;

    -- Validate instance_version
    IF latest_instance_version IS NULL THEN
        error_messages := error_messages || FORMAT(
            'The provided instance_id (%s) does not have an aggregate_instance version history. ', 
            NEW.instance_id
        );
    END IF;

    IF NEW.instance_version IS NULL THEN
        RAISE NOTICE 'No instance_version provided for instance_id (%), defaulting to latest_instance_version (%).',
            NEW.instance_id, latest_instance_version;
    ELSIF NEW.instance_version > latest_instance_version OR NEW.instance_version < earliest_instance_version THEN
        error_messages := error_messages || FORMAT(
            'Invalid instance_version (%s) for instance_id (%s). ', 
            NEW.instance_version, NEW.instance_id
        );
    ELSIF NEW.instance_version < latest_instance_version THEN
        RAISE WARNING 'The provided instance_version (%) is not the latest version (%).',
            NEW.instance_version, latest_instance_version;
    END IF;

    NEW.instance_version := COALESCE(NEW.instance_version, latest_instance_version);

    -- Get the latest event_version for the associated domain_event
    SELECT MAX(event_version), MIN(event_version)
	INTO latest_event_version, earliest_event_version
    FROM stored.event_revision
    WHERE event_id = NEW.event_id;

    -- Validate event_version
    IF latest_event_version IS NULL THEN
        error_messages := error_messages || FORMAT(
            'The provided event_id (%s) does not have a domain_event version history. ', 
            NEW.event_id
        );
    END IF;

    IF NEW.event_version IS NULL THEN
        RAISE NOTICE 'No event_version provided for event_id (%), defaulting to latest_event_version (%).',
            NEW.event_id, latest_event_version;
    ELSIF NEW.event_version > latest_event_version OR NEW.event_version < earliest_event_version THEN
        error_messages := error_messages || FORMAT(
            'Invalid event_version (%s) for event_id (%s). ', 
            NEW.event_version, NEW.event_id
        );
    ELSIF NEW.event_version < latest_event_version THEN
        RAISE WARNING 'The provided event_version (%) is not the latest version (%).',
            NEW.event_version, latest_event_version;
    END IF;

    NEW.event_version := COALESCE(NEW.event_version, latest_event_version);

    -- Get the current maximum stream_sequence for the given instance_id
    SELECT COALESCE(MAX(stream_sequence), -1) INTO max_sequence
    FROM stored.event_stream
    WHERE instance_id = NEW.instance_id
    AND instance_version = COALESCE(NEW.instance_version, latest_instance_version);

    -- Ensure the new stream_sequence is the next in the sequence
    NEW.stream_sequence := max_sequence + 1;

    -- If there are any errors, raise a single exception with all messages
    IF error_messages <> '' THEN
        RAISE EXCEPTION 'Validation errors: %', error_messages;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION stored.validate_event_stream() OWNER TO postgres;

--
-- TOC entry 255 (class 1255 OID 16396)
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
-- TOC entry 218 (class 1259 OID 16397)
-- Name: aggregate_instance; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.aggregate_instance (
    instance_id integer NOT NULL,
    context_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.aggregate_instance OWNER TO postgres;

--
-- TOC entry 4910 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE aggregate_instance; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.aggregate_instance IS 'Represents specific instances of aggregates within a bounded context, uniquely identifying domain entities.';


--
-- TOC entry 219 (class 1259 OID 16400)
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
-- TOC entry 220 (class 1259 OID 16401)
-- Name: bounded_context; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.bounded_context (
    context_id integer NOT NULL,
    context_name text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.bounded_context OWNER TO postgres;

--
-- TOC entry 4911 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE bounded_context; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.bounded_context IS 'Represents immutable definitions of bounded contexts within the system, ensuring clear separation and autonomy of domains.';


--
-- TOC entry 221 (class 1259 OID 16407)
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
-- TOC entry 222 (class 1259 OID 16408)
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
-- TOC entry 4912 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE command_log; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.command_log IS 'Logs instances of domain commands executed against a bounded context, providing an audit trail and history of operations.';


--
-- TOC entry 223 (class 1259 OID 16414)
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
-- TOC entry 224 (class 1259 OID 16415)
-- Name: command_revision; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.command_revision (
    command_id integer NOT NULL,
    command_version integer NOT NULL,
    command_structure jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.command_revision OWNER TO postgres;

--
-- TOC entry 4913 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE command_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.command_revision IS 'Tracks updates to the structure or definition of domain commands, accommodating system evolution.';


--
-- TOC entry 225 (class 1259 OID 16421)
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
-- TOC entry 4914 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE context_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.context_revision IS 'Tracks changes to the bounded context definitions over time, allowing for an evolving understanding of domain boundaries.';


--
-- TOC entry 226 (class 1259 OID 16428)
-- Name: domain_command; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.domain_command (
    command_id integer NOT NULL,
    command_name text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.domain_command OWNER TO postgres;

--
-- TOC entry 4915 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE domain_command; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.domain_command IS 'Represents distinct, immutable representations of domain commands that trigger domain logic and potential state changes.';


--
-- TOC entry 227 (class 1259 OID 16434)
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
-- TOC entry 228 (class 1259 OID 16435)
-- Name: domain_event; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.domain_event (
    event_id integer NOT NULL,
    event_name text NOT NULL,
    created_at time with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.domain_event OWNER TO postgres;

--
-- TOC entry 4916 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE domain_event; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.domain_event IS 'Stores distinct, immutable representations of domain events that signify meaningful changes within the domain.';


--
-- TOC entry 229 (class 1259 OID 16441)
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
-- TOC entry 230 (class 1259 OID 16442)
-- Name: event_revision; Type: TABLE; Schema: stored; Owner: postgres
--

CREATE TABLE stored.event_revision (
    event_id integer NOT NULL,
    event_version integer NOT NULL,
    event_structure jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE stored.event_revision OWNER TO postgres;

--
-- TOC entry 4917 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE event_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.event_revision IS 'Tracks revisions to the structure or definition of domain events over time, supporting schema evolution.';


--
-- TOC entry 231 (class 1259 OID 16448)
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
-- TOC entry 4918 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE event_stream; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.event_stream IS 'Captures the sequence of domain events emitted by aggregate instances in response to logged commands, forming the core of the event-sourced state reconstruction.';


--
-- TOC entry 232 (class 1259 OID 16454)
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
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE instance_revision; Type: COMMENT; Schema: stored; Owner: postgres
--

COMMENT ON TABLE stored.instance_revision IS 'Manages versioning for aggregate instances to align them with evolving bounded context definitions, ensuring consistency during changes.';


--
-- TOC entry 4711 (class 2606 OID 16459)
-- Name: aggregate_instance aggregate_instance_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.aggregate_instance
    ADD CONSTRAINT aggregate_instance_pkey PRIMARY KEY (instance_id);


--
-- TOC entry 4713 (class 2606 OID 16461)
-- Name: bounded_context bounded_context_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.bounded_context
    ADD CONSTRAINT bounded_context_pkey PRIMARY KEY (context_id);


--
-- TOC entry 4715 (class 2606 OID 16463)
-- Name: command_log command_log_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_log
    ADD CONSTRAINT command_log_pkey PRIMARY KEY (command_log_id);


--
-- TOC entry 4717 (class 2606 OID 16465)
-- Name: command_revision command_revision_command_id_command_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_revision
    ADD CONSTRAINT command_revision_command_id_command_version_key UNIQUE (command_id, command_version);


--
-- TOC entry 4719 (class 2606 OID 16467)
-- Name: context_revision context_revision_context_id_context_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.context_revision
    ADD CONSTRAINT context_revision_context_id_context_version_key UNIQUE (context_id, context_version);


--
-- TOC entry 4721 (class 2606 OID 16469)
-- Name: domain_command domain_command_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.domain_command
    ADD CONSTRAINT domain_command_pkey PRIMARY KEY (command_id);


--
-- TOC entry 4723 (class 2606 OID 16471)
-- Name: domain_event domain_event_pkey; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.domain_event
    ADD CONSTRAINT domain_event_pkey PRIMARY KEY (event_id);


--
-- TOC entry 4725 (class 2606 OID 16473)
-- Name: event_revision event_revision_event_id_event_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_revision
    ADD CONSTRAINT event_revision_event_id_event_version_key UNIQUE (event_id, event_version);


--
-- TOC entry 4727 (class 2606 OID 16475)
-- Name: event_stream event_stream_instance_id_instance_version_event_id_event_ve_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_instance_id_instance_version_event_id_event_ve_key UNIQUE (instance_id, instance_version, event_id, event_version, stream_sequence);


--
-- TOC entry 4729 (class 2606 OID 16477)
-- Name: instance_revision instance_version_instance_id_instance_version_key; Type: CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.instance_revision
    ADD CONSTRAINT instance_version_instance_id_instance_version_key UNIQUE (instance_id, instance_version);


--
-- TOC entry 4749 (class 2620 OID 16534)
-- Name: domain_command after_domain_command_insert; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER after_domain_command_insert AFTER INSERT ON stored.domain_command FOR EACH ROW EXECUTE FUNCTION stored.create_initial_command_revision();


--
-- TOC entry 4751 (class 2620 OID 16548)
-- Name: domain_event after_domain_event_insert; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER after_domain_event_insert AFTER INSERT ON stored.domain_event FOR EACH ROW EXECUTE FUNCTION stored.create_initial_event_revision();


--
-- TOC entry 4739 (class 2620 OID 16478)
-- Name: aggregate_instance after_insert_aggregate_instance; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER after_insert_aggregate_instance AFTER INSERT ON stored.aggregate_instance FOR EACH ROW EXECUTE FUNCTION stored.create_instance_revision();


--
-- TOC entry 4741 (class 2620 OID 16479)
-- Name: bounded_context after_insert_bounded_context; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER after_insert_bounded_context AFTER INSERT ON stored.bounded_context FOR EACH ROW EXECUTE FUNCTION stored.create_context_revision();


--
-- TOC entry 4743 (class 2620 OID 16538)
-- Name: command_log before_command_log_insert; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_command_log_insert BEFORE INSERT ON stored.command_log FOR EACH ROW EXECUTE FUNCTION stored.validate_command_version();


--
-- TOC entry 4745 (class 2620 OID 16536)
-- Name: command_revision before_command_revision_insert; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_command_revision_insert BEFORE INSERT ON stored.command_revision FOR EACH ROW EXECUTE FUNCTION stored.auto_increment_command_version();


--
-- TOC entry 4753 (class 2620 OID 16550)
-- Name: event_revision before_event_revision_insert; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_event_revision_insert BEFORE INSERT ON stored.event_revision FOR EACH ROW EXECUTE FUNCTION stored.auto_increment_event_version();


--
-- TOC entry 4747 (class 2620 OID 16480)
-- Name: context_revision before_insert_context_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_insert_context_revision BEFORE INSERT ON stored.context_revision FOR EACH ROW EXECUTE FUNCTION stored.auto_increment_context_version();


--
-- TOC entry 4755 (class 2620 OID 16576)
-- Name: event_stream before_insert_validate_event_stream; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_insert_validate_event_stream BEFORE INSERT ON stored.event_stream FOR EACH ROW EXECUTE FUNCTION stored.validate_event_stream();


--
-- TOC entry 4757 (class 2620 OID 16481)
-- Name: instance_revision before_insert_validate_instance_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER before_insert_validate_instance_revision BEFORE INSERT ON stored.instance_revision FOR EACH ROW EXECUTE FUNCTION stored.validate_instance_revision();


--
-- TOC entry 4740 (class 2620 OID 16482)
-- Name: aggregate_instance prevent_update_delete_aggregate_instance; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_aggregate_instance BEFORE DELETE OR UPDATE ON stored.aggregate_instance FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_aggregate_instance();


--
-- TOC entry 4742 (class 2620 OID 16483)
-- Name: bounded_context prevent_update_delete_bounded_context; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_bounded_context BEFORE DELETE OR UPDATE ON stored.bounded_context FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_domain_context();


--
-- TOC entry 4748 (class 2620 OID 16484)
-- Name: context_revision prevent_update_delete_context_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_context_revision BEFORE DELETE OR UPDATE ON stored.context_revision FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_context_revision();


--
-- TOC entry 4758 (class 2620 OID 16485)
-- Name: instance_revision prevent_update_delete_instance_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_update_delete_instance_revision BEFORE DELETE OR UPDATE ON stored.instance_revision FOR EACH ROW EXECUTE FUNCTION stored.disallow_update_delete_instance_revision();


--
-- TOC entry 4744 (class 2620 OID 16542)
-- Name: command_log prevent_updates_deletions_command_log; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_updates_deletions_command_log BEFORE DELETE OR UPDATE ON stored.command_log FOR EACH ROW EXECUTE FUNCTION stored.disallow_modifications();


--
-- TOC entry 4746 (class 2620 OID 16541)
-- Name: command_revision prevent_updates_deletions_command_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_updates_deletions_command_revision BEFORE DELETE OR UPDATE ON stored.command_revision FOR EACH ROW EXECUTE FUNCTION stored.disallow_modifications();


--
-- TOC entry 4750 (class 2620 OID 16540)
-- Name: domain_command prevent_updates_deletions_domain_command; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_updates_deletions_domain_command BEFORE DELETE OR UPDATE ON stored.domain_command FOR EACH ROW EXECUTE FUNCTION stored.disallow_modifications();


--
-- TOC entry 4752 (class 2620 OID 16551)
-- Name: domain_event prevent_updates_deletions_domain_event; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_updates_deletions_domain_event BEFORE DELETE OR UPDATE ON stored.domain_event FOR EACH ROW EXECUTE FUNCTION stored.disallow_modifications();


--
-- TOC entry 4754 (class 2620 OID 16552)
-- Name: event_revision prevent_updates_deletions_event_revision; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_updates_deletions_event_revision BEFORE DELETE OR UPDATE ON stored.event_revision FOR EACH ROW EXECUTE FUNCTION stored.disallow_modifications();


--
-- TOC entry 4756 (class 2620 OID 16577)
-- Name: event_stream prevent_updates_deletions_event_stream; Type: TRIGGER; Schema: stored; Owner: postgres
--

CREATE TRIGGER prevent_updates_deletions_event_stream BEFORE DELETE OR UPDATE ON stored.event_stream FOR EACH ROW EXECUTE FUNCTION stored.disallow_modifications();


--
-- TOC entry 4730 (class 2606 OID 16486)
-- Name: aggregate_instance aggregate_instance_context_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.aggregate_instance
    ADD CONSTRAINT aggregate_instance_context_id_fkey FOREIGN KEY (context_id) REFERENCES stored.bounded_context(context_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4731 (class 2606 OID 16491)
-- Name: command_log command_log_command_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_log
    ADD CONSTRAINT command_log_command_id_fkey FOREIGN KEY (command_id) REFERENCES stored.domain_command(command_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4732 (class 2606 OID 16496)
-- Name: command_revision command_revision_command_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.command_revision
    ADD CONSTRAINT command_revision_command_id_fkey FOREIGN KEY (command_id) REFERENCES stored.domain_command(command_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4733 (class 2606 OID 16501)
-- Name: context_revision context_revision_context_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.context_revision
    ADD CONSTRAINT context_revision_context_id_fkey FOREIGN KEY (context_id) REFERENCES stored.bounded_context(context_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4734 (class 2606 OID 16506)
-- Name: event_revision event_revision_event_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_revision
    ADD CONSTRAINT event_revision_event_id_fkey FOREIGN KEY (event_id) REFERENCES stored.domain_event(event_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4735 (class 2606 OID 16511)
-- Name: event_stream event_stream_command_log_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_command_log_id_fkey FOREIGN KEY (command_log_id) REFERENCES stored.command_log(command_log_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4736 (class 2606 OID 16516)
-- Name: event_stream event_stream_event_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_event_id_fkey FOREIGN KEY (event_id) REFERENCES stored.domain_event(event_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4737 (class 2606 OID 16521)
-- Name: event_stream event_stream_instance_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.event_stream
    ADD CONSTRAINT event_stream_instance_id_fkey FOREIGN KEY (instance_id) REFERENCES stored.aggregate_instance(instance_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4738 (class 2606 OID 16526)
-- Name: instance_revision instance_version_instance_id_fkey; Type: FK CONSTRAINT; Schema: stored; Owner: postgres
--

ALTER TABLE ONLY stored.instance_revision
    ADD CONSTRAINT instance_version_instance_id_fkey FOREIGN KEY (instance_id) REFERENCES stored.aggregate_instance(instance_id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2024-12-10 21:58:34

--
-- PostgreSQL database dump complete
--

