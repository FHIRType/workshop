-- we don't know how to generate root <with-no-name> (class Root) :(

-- comment on database postgres is 'default administrative connection database';

create table test
(
    id   integer not null
        constraint test_pk
            primary key,
    name varchar
);

--   alter table test
--       owner to postgres;

