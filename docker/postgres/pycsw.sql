--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET search_path = public, pg_catalog;

--
-- Name: records_update_geometry(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION records_update_geometry() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.wkt_geometry IS NULL THEN
        RETURN NEW;
    END IF;
    NEW.wkb_geometry := ST_GeomFromText(NEW.wkt_geometry,4326);
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.records_update_geometry() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE records (
    identifier text NOT NULL,
    typename text NOT NULL,
    schema text NOT NULL,
    mdsource text NOT NULL,
    insert_date text NOT NULL,
    xml text NOT NULL,
    anytext text NOT NULL,
    language text,
    type text,
    title text,
    title_alternate text,
    abstract text,
    keywords text,
    keywordstype text,
    parentidentifier text,
    relation text,
    time_begin text,
    time_end text,
    topicategory text,
    resourcelanguage text,
    creator text,
    publisher text,
    contributor text,
    organization text,
    securityconstraints text,
    accessconstraints text,
    otherconstraints text,
    date text,
    date_revision text,
    date_creation text,
    date_publication text,
    date_modified text,
    format text,
    source text,
    crs text,
    geodescode text,
    denominator text,
    distancevalue text,
    distanceuom text,
    wkt_geometry text,
    servicetype text,
    servicetypeversion text,
    operation text,
    couplingtype text,
    operateson text,
    operatesonidentifier text,
    operatesoname text,
    degree text,
    classification text,
    conditionapplyingtoaccessanduse text,
    lineage text,
    responsiblepartyrole text,
    specificationtitle text,
    specificationdate text,
    specificationdatetype text,
    links text,
    anytext_tsvector tsvector,
    wkb_geometry geometry(Geometry,4326)
);


ALTER TABLE records OWNER TO postgres;

--
-- Data for Name: records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY records (identifier, typename, schema, mdsource, insert_date, xml, anytext, language, type, title, title_alternate, abstract, keywords, keywordstype, parentidentifier, relation, time_begin, time_end, topicategory, resourcelanguage, creator, publisher, contributor, organization, securityconstraints, accessconstraints, otherconstraints, date, date_revision, date_creation, date_publication, date_modified, format, source, crs, geodescode, denominator, distancevalue, distanceuom, wkt_geometry, servicetype, servicetypeversion, operation, couplingtype, operateson, operatesonidentifier, operatesoname, degree, classification, conditionapplyingtoaccessanduse, lineage, responsiblepartyrole, specificationtitle, specificationdate, specificationdatetype, links, anytext_tsvector, wkb_geometry) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY spatial_ref_sys  FROM stdin;
\.


SET search_path = topology, pg_catalog;

--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology  FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY layer  FROM stdin;
\.


SET search_path = public, pg_catalog;

--
-- Name: records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY records
    ADD CONSTRAINT records_pkey PRIMARY KEY (identifier);


--
-- Name: fts_gin_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fts_gin_idx ON records USING gin (anytext_tsvector);


--
-- Name: ix_records_abstract; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_abstract ON records USING btree (abstract);


--
-- Name: ix_records_accessconstraints; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_accessconstraints ON records USING btree (accessconstraints);


--
-- Name: ix_records_classification; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_classification ON records USING btree (classification);


--
-- Name: ix_records_conditionapplyingtoaccessanduse; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_conditionapplyingtoaccessanduse ON records USING btree (conditionapplyingtoaccessanduse);


--
-- Name: ix_records_contributor; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_contributor ON records USING btree (contributor);


--
-- Name: ix_records_couplingtype; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_couplingtype ON records USING btree (couplingtype);


--
-- Name: ix_records_creator; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_creator ON records USING btree (creator);


--
-- Name: ix_records_crs; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_crs ON records USING btree (crs);


--
-- Name: ix_records_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_date ON records USING btree (date);


--
-- Name: ix_records_date_creation; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_date_creation ON records USING btree (date_creation);


--
-- Name: ix_records_date_modified; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_date_modified ON records USING btree (date_modified);


--
-- Name: ix_records_date_publication; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_date_publication ON records USING btree (date_publication);


--
-- Name: ix_records_date_revision; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_date_revision ON records USING btree (date_revision);


--
-- Name: ix_records_degree; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_degree ON records USING btree (degree);


--
-- Name: ix_records_denominator; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_denominator ON records USING btree (denominator);


--
-- Name: ix_records_distanceuom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_distanceuom ON records USING btree (distanceuom);


--
-- Name: ix_records_distancevalue; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_distancevalue ON records USING btree (distancevalue);


--
-- Name: ix_records_format; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_format ON records USING btree (format);


--
-- Name: ix_records_geodescode; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_geodescode ON records USING btree (geodescode);


--
-- Name: ix_records_insert_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_insert_date ON records USING btree (insert_date);


--
-- Name: ix_records_keywords; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_keywords ON records USING btree (keywords);


--
-- Name: ix_records_keywordstype; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_keywordstype ON records USING btree (keywordstype);


--
-- Name: ix_records_language; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_language ON records USING btree (language);


--
-- Name: ix_records_lineage; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_lineage ON records USING btree (lineage);


--
-- Name: ix_records_links; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_links ON records USING btree (links);


--
-- Name: ix_records_mdsource; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_mdsource ON records USING btree (mdsource);


--
-- Name: ix_records_operateson; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_operateson ON records USING btree (operateson);


--
-- Name: ix_records_operatesoname; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_operatesoname ON records USING btree (operatesoname);


--
-- Name: ix_records_operatesonidentifier; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_operatesonidentifier ON records USING btree (operatesonidentifier);


--
-- Name: ix_records_operation; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_operation ON records USING btree (operation);


--
-- Name: ix_records_organization; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_organization ON records USING btree (organization);


--
-- Name: ix_records_otherconstraints; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_otherconstraints ON records USING btree (otherconstraints);


--
-- Name: ix_records_parentidentifier; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_parentidentifier ON records USING btree (parentidentifier);


--
-- Name: ix_records_publisher; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_publisher ON records USING btree (publisher);


--
-- Name: ix_records_relation; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_relation ON records USING btree (relation);


--
-- Name: ix_records_resourcelanguage; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_resourcelanguage ON records USING btree (resourcelanguage);


--
-- Name: ix_records_responsiblepartyrole; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_responsiblepartyrole ON records USING btree (responsiblepartyrole);


--
-- Name: ix_records_schema; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_schema ON records USING btree (schema);


--
-- Name: ix_records_securityconstraints; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_securityconstraints ON records USING btree (securityconstraints);


--
-- Name: ix_records_servicetype; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_servicetype ON records USING btree (servicetype);


--
-- Name: ix_records_servicetypeversion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_servicetypeversion ON records USING btree (servicetypeversion);


--
-- Name: ix_records_source; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_source ON records USING btree (source);


--
-- Name: ix_records_specificationdate; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_specificationdate ON records USING btree (specificationdate);


--
-- Name: ix_records_specificationdatetype; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_specificationdatetype ON records USING btree (specificationdatetype);


--
-- Name: ix_records_specificationtitle; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_specificationtitle ON records USING btree (specificationtitle);


--
-- Name: ix_records_time_begin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_time_begin ON records USING btree (time_begin);


--
-- Name: ix_records_time_end; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_time_end ON records USING btree (time_end);


--
-- Name: ix_records_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_title ON records USING btree (title);


--
-- Name: ix_records_title_alternate; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_title_alternate ON records USING btree (title_alternate);


--
-- Name: ix_records_topicategory; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_topicategory ON records USING btree (topicategory);


--
-- Name: ix_records_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_type ON records USING btree (type);


--
-- Name: ix_records_typename; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_records_typename ON records USING btree (typename);


--
-- Name: wkb_geometry_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX wkb_geometry_idx ON records USING gist (wkb_geometry);


--
-- Name: ftsupdate; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ftsupdate BEFORE INSERT OR UPDATE ON records FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger('anytext_tsvector', 'pg_catalog.english', 'anytext');


--
-- Name: records_update_geometry; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER records_update_geometry BEFORE INSERT OR UPDATE ON records FOR EACH ROW EXECUTE PROCEDURE records_update_geometry();


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

