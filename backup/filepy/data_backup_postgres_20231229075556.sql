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
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart (
    id integer NOT NULL,
    user_id integer,
    item_id integer,
    quantity integer
);


ALTER TABLE public.cart OWNER TO postgres;

--
-- Name: cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_id_seq OWNER TO postgres;

--
-- Name: cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_id_seq OWNED BY public.cart.id;


--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.category_id_seq OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- Name: delivery_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.delivery_address (
    id integer NOT NULL,
    user_id integer,
    country character varying(100),
    city character varying(100),
    street character varying(100),
    phone character varying(20)
);


ALTER TABLE public.delivery_address OWNER TO postgres;

--
-- Name: delivery_address_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.delivery_address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.delivery_address_id_seq OWNER TO postgres;

--
-- Name: delivery_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.delivery_address_id_seq OWNED BY public.delivery_address.id;


--
-- Name: item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    price integer NOT NULL,
    "isActive" boolean,
    text text NOT NULL,
    image_url character varying(255),
    category_id integer
);


ALTER TABLE public.item OWNER TO postgres;

--
-- Name: item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_id_seq OWNER TO postgres;

--
-- Name: item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_id_seq OWNED BY public.item.id;


--
-- Name: news; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    intro character varying(300) NOT NULL,
    text text NOT NULL,
    date timestamp without time zone
);


ALTER TABLE public.news OWNER TO postgres;

--
-- Name: news_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.news_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.news_id_seq OWNER TO postgres;

--
-- Name: news_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_id_seq OWNED BY public.news.id;


--
-- Name: order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order" (
    id integer NOT NULL,
    user_id integer,
    total_price double precision,
    status character varying(100),
    order_date timestamp without time zone,
    delivery_address_id integer
);


ALTER TABLE public."order" OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_id_seq OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_id_seq OWNED BY public."order".id;


--
-- Name: order_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_item (
    order_id integer NOT NULL,
    item_id integer NOT NULL,
    quantity integer
);


ALTER TABLE public.order_item OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(512),
    role character varying(50) DEFAULT 'Пользователь'::character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: cart id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart ALTER COLUMN id SET DEFAULT nextval('public.cart_id_seq'::regclass);


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- Name: delivery_address id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_address ALTER COLUMN id SET DEFAULT nextval('public.delivery_address_id_seq'::regclass);


--
-- Name: item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item ALTER COLUMN id SET DEFAULT nextval('public.item_id_seq'::regclass);


--
-- Name: news id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news ALTER COLUMN id SET DEFAULT nextval('public.news_id_seq'::regclass);


--
-- Name: order id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order" ALTER COLUMN id SET DEFAULT nextval('public.order_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart (id, user_id, item_id, quantity) FROM stdin;
15	6	8	5
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, name) FROM stdin;
1	Конфеты
2	Шоколадки
3	Тортики
4	Мармеладки
5	Пироженные
6	Леденцы
7	Сахарная вата
8	Жевачки
9	Пирожные
10	Сладкие напитки
11	Мороженое
\.


--
-- Data for Name: delivery_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.delivery_address (id, user_id, country, city, street, phone) FROM stdin;
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item (id, title, price, "isActive", text, image_url, category_id) FROM stdin;
8	Батончик шоколадный SNICKERS Лесной орех, 81г, Россия, 81 г	49	t	Шоколадный батончик SNICKERS Лесной орех с начинкой из цельного жареного арахиса, фундука, нуги и карамели, покрытый слоем молочного шоколада. Тающий во рту десерт быстро утоляет голод и заряжает энергией на целый день. Отличный вариант для быстрого перекуса и чаепития в кругу друзей.	https://lenta.servicecdn.ru/globalassets/1/-/11/35/56/271672.png?preset=fulllossywhite	1
9	Батончик шоколадный MARS Max с нугой и карамелью, 81г, Россия, 81 г	49	t	Большой шоколадный батончик MARS Max – это уникальное сочетание нуги, карамели и ароматного молочного шоколада, который буквально тает во рту. Вкус Марса знаком каждому с детства и дарит отличное настроение каждому. Питательный и вкусный десерт идеально дополнит чашечку горячего чая или кофе.	https://lenta.servicecdn.ru/globalassets/1/-/26/66/05/271670.png?preset=fulllossywhite	1
10	Батончик шоколадный SNICKERS White, 81г, Россия, 81 г	49	t	Шоколадный батончик SNICKERS Белый с начинкой из жареного арахиса, карамели и нуги покрыт нежным белым шоколадом, буквально тающим во рту. Он идеально подходит для людей, ведущих активный образ жизни, нередко перекусывающих на ходу.	https://lenta.servicecdn.ru/globalassets/1/-/44/30/74/405881_1.png?preset=fulllossywhite	1
11	Конфеты KONTI Золотая лилия, весовые, Россия	350	t	Конфеты KONTI Золотая лилия – глазированные конфеты на основе нежной ирисной массы с добавлением сгущенного молока. Содержат 17% сгущенного молока.	https://lenta.servicecdn.ru/globalassets/1/-/32/60/92/261224_2.png?preset=fulllossywhite	1
12	Конфеты СЛАВЯНКА Маленькое чудо сливочное, весовые, Россия	539	t	Конфеты СЛАВЯНКА Маленькое чудо оригинальной формы с нежной сливочной начинкой и целым орехом. Для производства используются натуральные ингредиенты высшего качества. Без искусственных красителей и ароматизаторов!	https://lenta.servicecdn.ru/globalassets/1/-/36/06/29/282442_4.png?preset=fulllossywhite	1
13	Конфеты KDV Крокант, весовые, Россия	349	t	Конфеты KDV Крокант – это глазированный молочный грильяж с добавлением тертого жареного арахиса и дробленого миндаля.	https://lenta.servicecdn.ru/globalassets/1/-/27/31/83/445589.png?preset=fulllossywhite	1
14	Конфеты РАЙСКИЕ ОБЛАКА Ассорти суфле, весовые, Россия	359	t	Конфеты РАЙСКИЕ ОБЛАКА Ассорти – суфле в шоколадной глазури с разными вкусами. Для производства используются натуральные ингредиенты высшего качества. Без искусственных красителей и ароматизаторов!	https://lenta.servicecdn.ru/globalassets/1/-/38/15/14/241121_5.png?preset=fulllossywhite	1
15	Конфеты BORA-BORA Кокос, весовые, Россия	429	t	Конфеты BORA-BORA Кокос – нежный сливочный крем, кокосовая мякоть и молочно-шоколадная глазурь.	https://lenta.servicecdn.ru/globalassets/1/-/56/47/82/359175_1.png?preset=fulllossywhite	1
16	Конфеты СЛАВЯНКА Медунок с орехом, весовые, Россия	349	t	Конфеты СЛАВЯНКА Медунок с орехом – глазированная конфета из хрустящих шариков, ореха и мягкой карамели. Для производства используются натуральные ингредиенты высшего качества. 	https://lenta.servicecdn.ru/globalassets/1/-/22/09/94/370004.png?preset=fulllossywhite	1
18	Шоколад молочный MILKA, 85г, Болгария, 85 г	68	t	Классический молочный шоколад MILKA приготовлен с добавлением свежего альпийского молока, благодаря чему обладает настолько нежным мягким вкусом со сливочными нотками и шелковистой текстурой.	https://lenta.servicecdn.ru/globalassets/1/-/56/74/00/326631_9.png?preset=fulllossywhite	2
19	Шоколад молочный ALPEN GOLD с фундуком и изюмом, 85г, Россия, 85 г	48	t	Выпускаемый брендом ALPEN GOLD молочный шоколад, изготовленный по традиционному рецепту из высококачественных ингредиентов, обладает классическим нежным вкусом, дополненным изюмом и обжаренным дробленым фундуком.	https://lenta.servicecdn.ru/globalassets/1/-/54/61/90/532494_2.png?preset=fulllossywhite	2
\.


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news (id, title, intro, text, date) FROM stdin;
4	Прекрасное веселье в каждой жвачке: Hubba Bubba - история вкуса и радости	Hubba Bubba - вкус и радость	Сладкая жвачка Hubba Bubba - это не просто конфета для жевания, это настоящий символ веселья и незабываемых моментов. Среди множества сладостей этот великолепный продукт выделяется своим уникальным вкусом и внушительной историей. Однако не только вкус делает Hubba Bubba такой особенной. Давайте углубимся в детали и узнаем больше о неповторимых формах этой замечательной жвачки\r\n\r\n\r\n\r\n\r\n\r\n\r\nУникальность Hubba Bubba проявляется также в ее разнообразии форм. Одной из наиболее узнаваемых форм являются маленькие палочки, каждая из которых хранит в себе секретный вкус внутри. Это позволяет наслаждаться не только прекрасным ароматом, но и ощущением открытия новой сладкой тайны с каждой жевательной пластинкой.\r\n\r\n\r\n\r\nКроме того, Hubba Bubba славится своими огромными пузырями, которые можно создавать, раздувая жвачку. Эти великолепные шедевры пузырной магии поразят вас своей размерами и удивительной прочностью. Развлекайтесь, создавая целые пузырные волшебства с Hubba Bubba!\r\n\r\n\r\n\r\nВзрыв вкуса и веселья с Hubba Bubba: история долгоживущей сладкой легенды\r\n\r\n\r\n\r\n\r\n\r\n\r\nСозданная в 1979 году компанией Wm. Wrigley Jr. Company, жвачка Hubba Bubba сразу стала звездой среди молодежи и детей. Она поразила мир своей невероятной растяжимостью и неповторимыми вкусами. Первоначально представленная в Америке, Hubba Bubba вскоре завоевала сердца людей по всему миру.\r\n\r\n\r\n\r\nЧто делает Hubba Bubba настолько неповторимой? Это просто! Ее яркие и сочные ароматы, позволяющие окунуться в настоящий фестиваль вкусов, и удивительная способность растягиваться до невероятных размеров, что стало настоящей фишкой. Первоначально запускаясь с несколькими классическими вкусами, Hubba Bubba с течением времени разнообразила свой ассортимент, предлагая десятки оригинальных и экзотических вариантов.\r\n\r\n\r\n\r\n Вкус детства, который никогда не уходит\r\n\r\n\r\n\r\n\r\nДолгие годы прошли, но Hubba Bubba остается популярной, как никогда. Эта жвачка привлекает не только детей, но и взрослых, которые ценят вкус ностальгии и ярких впечатлений. Взяв Hubba Bubba в руки, вы словно возвращаетесь в дни радостных игр и беззаботных моментов детства.\r\n\r\n\r\n\r\nСчастье и радость, упакованные в каждую жвачку Hubba Bubba, остаются с нами на протяжении долгих лет. Станьте частью этой сладкой легенды, исследуйте ее богатый мир вкусов и вспомните яркие моменты вашей жизни. И помните, что вы всегда можете заказать свои любимые вкусы Hubba Bubba в нашем интернет-магазине. Добавьте кусочек радости и веселья в свою жизнь с Hubba Bubba прямо сейчас!\r\n	2023-12-27 07:08:18.555112
5	В чём секрет успеха шоколада Milka	В чём секрет успеха шоколада Milka	Milka - бренд, который не только завоевал весь мир своим изысканным шоколадом, но и проник в самые глубины сердец любителей сладостей. В чем же заключается секрет успеха этого непревзойденного альпийского шедевра?\r\n\r\n\r\n\r\nКаждый кусочек Milka - это истинное чудо для ваших вкусовых рецепторов. Сочетание нежного шоколада и аромата альпийского молока делает его вкус неповторимым. Но важный элемент, который делает Milka таким особенным, - это высокое качество ингредиентов. Каждый ингредиент, используемый в производстве Milka, проходит строгий отбор, чтобы обеспечить истинное наслаждение и удовольствие в каждой упаковке.\r\n\r\n\r\n\r\nБренд персонажа - фиолетовая корова	2023-12-27 07:09:11.920949
6	Японские палочки Pocky	Праздник Pocky Day	Национальный праздник Pocky Day впервые начал праздноваться в 1994 году в южнокорейском городе Пусан. Уже в 1997 году он стал широко известным. День Поки довольно быстро набрал популярность у молодёжи и стал азиатским аналогом Дня Святого Валентина. День приходится на 11 ноября и уже стал национальным праздником. В отличие от Дня святого Валентина, в этот день люди дарят палочки Поки не только в знак любви, но для того, чтобы показать уважение и симпатию для близкого им человека. 	2023-12-29 04:19:58.624165
\.


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."order" (id, user_id, total_price, status, order_date, delivery_address_id) FROM stdin;
\.


--
-- Data for Name: order_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_item (order_id, item_id, quantity) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, email, password_hash, role) FROM stdin;
6	Маша	masha@mail.ru	scrypt:32768:8:1$h0SjCKixn6nF7qrp$2fb27c3ba24aba072143941006b0698fb498541252cbb6f76072ef1235606015b291eff54783b87f65d3801009fa9c2c6719b37d1883a40b5a9fe34d8034fa31	Пользователь
7	Дарья	dasha.sidorenko1111@mail.ru	scrypt:32768:8:1$JdokWa3JUV3FIfO0$e88f85c036f989ec4ac33c7bd138c73ddaaab789aa78c666b9a24ceb0fa9cb00135cac6c36af06e6a15654d4eed9faa274e135ffbea1c9faf7adeadd6a595433	Администратор
\.


--
-- Name: cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_id_seq', 15, true);


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 11, true);


--
-- Name: delivery_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.delivery_address_id_seq', 16, true);


--
-- Name: item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_id_seq', 20, true);


--
-- Name: news_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.news_id_seq', 6, true);


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_id_seq', 16, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 7, true);


--
-- Name: cart cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_pkey PRIMARY KEY (id);


--
-- Name: category category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_name_key UNIQUE (name);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: delivery_address delivery_address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_address
    ADD CONSTRAINT delivery_address_pkey PRIMARY KEY (id);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (id);


--
-- Name: order_item order_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT order_item_pkey PRIMARY KEY (order_id, item_id);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: cart cart_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id);


--
-- Name: cart cart_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: delivery_address delivery_address_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_address
    ADD CONSTRAINT delivery_address_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: item fk_category; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: order fk_delivery_address; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT fk_delivery_address FOREIGN KEY (delivery_address_id) REFERENCES public.delivery_address(id);


--
-- Name: order_item order_item_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT order_item_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id);


--
-- Name: order_item order_item_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT order_item_order_id_fkey FOREIGN KEY (order_id) REFERENCES public."order"(id);


--
-- Name: order order_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

