--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: FHIRType_Local; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "FHIRType_Local" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LC_COLLATE = 'C' LC_CTYPE = 'en';


ALTER DATABASE "FHIRType_Local" OWNER TO postgres;

\connect "FHIRType_Local"

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: table_name; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.table_name (
);


ALTER TABLE public.table_name OWNER TO postgres;

--
-- Name: test; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public.test OWNER TO postgres;

--
-- Data for Name: table_name; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.table_name  FROM stdin;
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test (id, name) FROM stdin;
\.


--
-- Name: test test_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_pk PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

