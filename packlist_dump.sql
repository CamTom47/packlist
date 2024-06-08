--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Postgres.app)
-- Dumped by pg_dump version 16.2 (Postgres.app)

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
-- Name: items; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.items (
    id integer NOT NULL,
    name text NOT NULL,
    category text NOT NULL,
    essential boolean NOT NULL,
    rain_precautionary boolean,
    cold_precautionary boolean,
    heat_precautionary boolean,
    emergency_precautionary boolean,
    created_by integer,
    removable boolean
);


ALTER TABLE public.items OWNER TO camth;

--
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.items_id_seq OWNER TO camth;

--
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- Name: packs; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.packs (
    id integer NOT NULL,
    owner integer NOT NULL,
    name text NOT NULL,
    notes text
);


ALTER TABLE public.packs OWNER TO camth;

--
-- Name: packs_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.packs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.packs_id_seq OWNER TO camth;

--
-- Name: packs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.packs_id_seq OWNED BY public.packs.id;


--
-- Name: packs_items; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.packs_items (
    id integer NOT NULL,
    pack_id integer NOT NULL,
    item_id integer NOT NULL
);


ALTER TABLE public.packs_items OWNER TO camth;

--
-- Name: packs_items_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.packs_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.packs_items_id_seq OWNER TO camth;

--
-- Name: packs_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.packs_items_id_seq OWNED BY public.packs_items.id;


--
-- Name: trip_status; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.trip_status (
    id integer NOT NULL,
    status text NOT NULL
);


ALTER TABLE public.trip_status OWNER TO camth;

--
-- Name: trip_status_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.trip_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trip_status_id_seq OWNER TO camth;

--
-- Name: trip_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.trip_status_id_seq OWNED BY public.trip_status.id;


--
-- Name: trips; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.trips (
    id integer NOT NULL,
    name text NOT NULL,
    location text NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    mileage integer,
    notes text,
    lat double precision,
    lng double precision,
    status integer NOT NULL
);


ALTER TABLE public.trips OWNER TO camth;

--
-- Name: trips_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.trips_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trips_id_seq OWNER TO camth;

--
-- Name: trips_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.trips_id_seq OWNED BY public.trips.id;


--
-- Name: trips_packs; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.trips_packs (
    id integer NOT NULL,
    trip_id integer NOT NULL,
    pack_id integer NOT NULL
);


ALTER TABLE public.trips_packs OWNER TO camth;

--
-- Name: trips_packs_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.trips_packs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trips_packs_id_seq OWNER TO camth;

--
-- Name: trips_packs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.trips_packs_id_seq OWNED BY public.trips_packs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.users OWNER TO camth;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO camth;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_trips; Type: TABLE; Schema: public; Owner: camth
--

CREATE TABLE public.users_trips (
    id integer NOT NULL,
    user_id integer NOT NULL,
    trip_id integer NOT NULL
);


ALTER TABLE public.users_trips OWNER TO camth;

--
-- Name: users_trips_id_seq; Type: SEQUENCE; Schema: public; Owner: camth
--

CREATE SEQUENCE public.users_trips_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_trips_id_seq OWNER TO camth;

--
-- Name: users_trips_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camth
--

ALTER SEQUENCE public.users_trips_id_seq OWNED BY public.users_trips.id;


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Name: packs id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs ALTER COLUMN id SET DEFAULT nextval('public.packs_id_seq'::regclass);


--
-- Name: packs_items id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs_items ALTER COLUMN id SET DEFAULT nextval('public.packs_items_id_seq'::regclass);


--
-- Name: trip_status id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trip_status ALTER COLUMN id SET DEFAULT nextval('public.trip_status_id_seq'::regclass);


--
-- Name: trips id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips ALTER COLUMN id SET DEFAULT nextval('public.trips_id_seq'::regclass);


--
-- Name: trips_packs id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips_packs ALTER COLUMN id SET DEFAULT nextval('public.trips_packs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: users_trips id; Type: DEFAULT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users_trips ALTER COLUMN id SET DEFAULT nextval('public.users_trips_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.items (id, name, category, essential, rain_precautionary, cold_precautionary, heat_precautionary, emergency_precautionary, created_by, removable) FROM stdin;
1	Maps	Navigation	t	f	f	f	t	1	f
2	Permits	Navigation	t	f	f	f	f	1	f
3	Compass	Navigation	t	f	f	f	t	1	f
4	Backpack	Gear	t	f	f	f	f	1	f
5	Rain Cover	Gear	t	t	f	f	f	1	f
6	Tent	Gear	t	f	f	f	f	1	f
7	Tarp	Gear	t	f	f	f	f	1	f
8	Rain Fly	Gear	t	t	f	f	f	1	f
9	Sleeping Bag	Sleeping	t	f	f	f	f	1	f
10	Sleeping Pad	Sleeping	t	f	f	f	f	1	f
11	Trekking Poles	Gear	t	f	f	f	f	1	f
12	Bear Canister	Safety	t	f	f	f	f	1	f
13	Water Filter/Purifier	Safety	t	f	f	t	t	1	f
14	Aquatabs	Safety	t	f	f	f	t	1	f
15	Head Lamp	Safety	t	f	f	f	t	1	f
16	Extra Batteries	Miscellaneous	t	f	f	f	f	1	f
17	Bear Spray	Safety	t	f	f	f	f	1	f
18	Bug Spray	Miscellaneous	t	f	f	f	f	1	f
19	Knife	Miscellaneous	f	f	f	f	t	1	f
20	Multi-Tool	Miscellaneous	f	f	f	f	t	1	f
21	Nalgene	Gear	t	f	f	f	f	1	f
22	Hand Sanitizer	Hygiene	f	f	f	f	f	1	f
23	Toilet Paper 	Hygiene	t	f	f	f	f	1	f
24	Sealable Bags	Hygiene	t	f	f	f	f	1	f
25	Toothbrush	Hygiene	f	f	f	f	f	1	f
26	Toolpaste	Hygiene	f	f	f	f	f	1	f
27	Soap	Hygiene	f	f	f	f	f	1	f
28	Contact Solution	Hygiene	f	f	f	f	f	1	f
29	Deodorant	Hygiene	f	f	f	f	f	1	f
30	Bathroom Hand Shovel	Hygiene	f	f	f	f	f	1	f
31	Food	Cooking	t	f	f	f	f	1	f
32	Energy Chews	Cooking	f	f	f	f	f	1	f
33	Fuel	Cooking	t	f	f	f	f	1	f
34	Matches	Cooking	f	f	t	f	f	1	f
35	Fire Starter	Cooking	f	t	f	f	f	1	f
36	Flint and Steel	Cooking	f	f	f	f	t	1	f
37	Lint	Cooking	f	t	f	f	f	1	f
38	Lighter	Cooking	f	f	f	f	f	1	f
39	Stove	Cooking	t	f	f	f	f	1	f
40	Cookset	Cooking	t	f	f	f	f	1	f
41	Pot Grabber	Cooking	f	f	f	f	f	1	f
42	Bowls	Cooking	f	f	f	f	f	1	f
43	Plates	Cooking	f	f	f	f	f	1	f
44	Silverware	Cooking	f	f	f	f	f	1	f
45	Mugs	Cooking	f	f	f	f	f	1	f
46	Dish Soap	Cooking	f	f	f	f	f	1	f
47	First-Aid Kit	Safety	t	f	f	f	t	1	f
48	Garmin	Safety	f	f	f	f	t	1	f
49	Walkie Talkies	Safety	f	f	f	f	t	1	f
50	Gauze	Safety	f	f	f	f	t	1	f
51	Wraps	Safety	f	f	f	f	t	1	f
52	Flashlight	Safety	f	f	f	f	t	1	f
53	String	Miscellaneous	f	f	f	f	f	1	f
54	Rope	Miscellaneous	f	f	f	f	f	1	f
55	Reading Material	Miscellaneous	f	f	f	f	f	1	f
56	Portable Phone Charger	Miscellaneous	f	f	f	f	f	1	f
57	Hatchet	Miscellaneous	f	f	f	f	f	1	f
58	Small Trash Bags	Miscellaneous	f	f	f	f	f	1	f
59	Tent Patch Kit	Miscellaneous	f	f	f	f	f	1	f
60	Duct Tape	Miscellaneous	f	f	f	f	f	1	f
61	Sleeping Bag Liner	Sleeping	f	f	t	f	f	1	f
62	Inflatable Pillow	Sleeping	f	f	f	f	f	1	f
63	Bug Net	Miscellaneous	f	f	f	f	f	1	f
64	Playing Cards	Miscellaneous	f	f	f	f	f	1	f
65	Pet Pack	Pet	f	f	f	f	f	1	f
66	Pet Food	Pet	f	f	f	f	f	1	f
67	Treats	Pet	f	f	f	f	f	1	f
68	Long Leash	Pet	f	f	f	f	f	1	f
69	Short Leash	Pet	f	f	f	f	f	1	f
70	Harness	Pet	f	f	f	f	f	1	f
71	Comb	Pet	f	f	f	f	f	1	f
72	Abrasion Spray	Pet	f	f	f	f	f	1	f
73	Collapsible Bowl	Pet	f	f	f	f	f	1	f
74	Light Collar	Pet	f	f	f	f	f	1	f
75	Towel	Pet	f	f	f	f	f	1	f
76	Pet Sleeping Pad	Pet	f	f	f	f	f	1	f
77	Poop Bags	Pet	f	f	f	f	f	1	f
78	Hand Warmers	Miscellaneous	f	f	t	f	t	1	f
79	Feet Warmers	Miscellaneous	f	f	t	f	t	1	f
80	Metal Nalgene	Gear	f	f	t	f	f	1	f
81	Gloves	Clothing	f	f	t	f	f	1	f
82	Hat	Clothing	f	f	t	f	f	1	f
83	Long Sleeve Shirt	Clothing	f	f	t	f	f	1	f
84	Quick Drying Pants	Clothing	t	t	f	f	f	1	f
85	Rain Proof Pants	Clothing	t	t	f	f	f	1	f
86	Shorts	Clothing	f	f	f	t	f	1	f
87	Leggings	Clothing	f	f	f	t	f	1	f
88	Lightweight Fleece	Clothing	f	f	f	f	f	1	f
89	Lightweight Jacket	Clothing	f	f	f	t	f	1	f
90	Wool Socks	Clothing	t	f	t	f	f	1	f
91	Hiking Boots	Clothing	t	f	f	f	f	1	f
92	Camp Sandals	Clothing	f	f	f	f	f	1	f
93	Moisture Wicking Shirt	Clothing	t	t	f	f	f	1	f
94	Underwear	Clothing	t	f	f	f	f	1	f
95	Rain Coat	Clothing	f	t	f	f	f	1	f
96	Thermal Layer	Clothing	f	f	t	f	f	1	f
\.


--
-- Data for Name: packs; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.packs (id, owner, name, notes) FROM stdin;
1	3	testTEST	
\.


--
-- Data for Name: packs_items; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.packs_items (id, pack_id, item_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	1	5
6	1	6
7	1	7
8	1	8
9	1	11
10	1	80
11	1	9
12	1	10
13	1	61
\.


--
-- Data for Name: trip_status; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.trip_status (id, status) FROM stdin;
1	Upcoming
2	Completed
3	Archived
\.


--
-- Data for Name: trips; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.trips (id, name, location, start_date, end_date, mileage, notes, lat, lng, status) FROM stdin;
1	test	Mailbox Peak Summit, Mailbox Peak Trail, North Bend, WA, USA	2024-05-12	2024-05-19	7		47.4623879	-121.6392051	1
\.


--
-- Data for Name: trips_packs; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.trips_packs (id, trip_id, pack_id) FROM stdin;
1	1	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.users (id, first_name, last_name, username, password) FROM stdin;
1	system_user	system_user	system_user	$2b$12$O/BV8WlmGpcj2FZlI8WBMObLZyq96pv7tM57kmSbJW0v98ZKwEdXq
2	test	test	test	$2b$12$OS6vqNUPLBA4yTd.U6EONOYnlkhFKsRn5GL./jJq4c0aq8Z.qIA3C
3	cameron	thomas	camtom47	$2b$12$y/fGVJWcw1kqj5W.EE5DweK.S0FecxlvudH86YpqcsUcgw5rQLcMi
\.


--
-- Data for Name: users_trips; Type: TABLE DATA; Schema: public; Owner: camth
--

COPY public.users_trips (id, user_id, trip_id) FROM stdin;
1	3	1
\.


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.items_id_seq', 96, true);


--
-- Name: packs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.packs_id_seq', 1, true);


--
-- Name: packs_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.packs_items_id_seq', 13, true);


--
-- Name: trip_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.trip_status_id_seq', 3, true);


--
-- Name: trips_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.trips_id_seq', 1, true);


--
-- Name: trips_packs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.trips_packs_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: users_trips_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camth
--

SELECT pg_catalog.setval('public.users_trips_id_seq', 1, true);


--
-- Name: items items_name_key; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_name_key UNIQUE (name);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- Name: packs_items packs_items_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs_items
    ADD CONSTRAINT packs_items_pkey PRIMARY KEY (id);


--
-- Name: packs packs_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs
    ADD CONSTRAINT packs_pkey PRIMARY KEY (id);


--
-- Name: trip_status trip_status_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trip_status
    ADD CONSTRAINT trip_status_pkey PRIMARY KEY (id);


--
-- Name: trips_packs trips_packs_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips_packs
    ADD CONSTRAINT trips_packs_pkey PRIMARY KEY (id);


--
-- Name: trips trips_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_pkey PRIMARY KEY (id);


--
-- Name: users users_password_key; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_password_key UNIQUE (password);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_trips users_trips_pkey; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users_trips
    ADD CONSTRAINT users_trips_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: items items_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: packs_items packs_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs_items
    ADD CONSTRAINT packs_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: packs_items packs_items_pack_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs_items
    ADD CONSTRAINT packs_items_pack_id_fkey FOREIGN KEY (pack_id) REFERENCES public.packs(id);


--
-- Name: packs packs_owner_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.packs
    ADD CONSTRAINT packs_owner_fkey FOREIGN KEY (owner) REFERENCES public.users(id);


--
-- Name: trips_packs trips_packs_pack_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips_packs
    ADD CONSTRAINT trips_packs_pack_id_fkey FOREIGN KEY (pack_id) REFERENCES public.packs(id);


--
-- Name: trips_packs trips_packs_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips_packs
    ADD CONSTRAINT trips_packs_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(id);


--
-- Name: trips trips_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_status_fkey FOREIGN KEY (status) REFERENCES public.trip_status(id);


--
-- Name: users_trips users_trips_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users_trips
    ADD CONSTRAINT users_trips_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(id);


--
-- Name: users_trips users_trips_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camth
--

ALTER TABLE ONLY public.users_trips
    ADD CONSTRAINT users_trips_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

