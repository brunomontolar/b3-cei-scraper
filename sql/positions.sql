-- Table: public.positions

-- DROP TABLE IF EXISTS public.positions;

CREATE TABLE IF NOT EXISTS public.positions
(
    account_id character varying(10) COLLATE pg_catalog."default" NOT NULL,
    position_date date NOT NULL,
    stock_id character varying(10) COLLATE pg_catalog."default" NOT NULL,
    quantity numeric(65,4) NOT NULL,
    price numeric(65,4) NOT NULL,
    stock_type character varying(10) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_position PRIMARY KEY (account_id, position_date, stock_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.positions
    OWNER to postgres;

REVOKE ALL ON TABLE public.positions FROM finance_updater;

GRANT INSERT ON TABLE public.positions TO finance_updater;

GRANT ALL ON TABLE public.positions TO postgres;