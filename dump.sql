create table auth_group
(
    id   integer      not null
        primary key autoincrement,
    name varchar(150) not null
        unique
);

create table django_content_type
(
    id        integer      not null
        primary key autoincrement,
    app_label varchar(100) not null,
    model     varchar(100) not null
);

create table auth_permission
(
    id              integer      not null
        primary key autoincrement,
    content_type_id integer      not null
        references django_content_type
            deferrable initially deferred,
    codename        varchar(100) not null,
    name            varchar(255) not null
);

create table auth_group_permissions
(
    id            integer not null
        primary key autoincrement,
    group_id      integer not null
        references auth_group
            deferrable initially deferred,
    permission_id integer not null
        references auth_permission
            deferrable initially deferred
);

create index auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create unique index auth_group_permissions_group_id_permission_id_0cd325b0_uniq
    on auth_group_permissions (group_id, permission_id);

create index auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create index auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create unique index auth_permission_content_type_id_codename_01ab375a_uniq
    on auth_permission (content_type_id, codename);

create unique index django_content_type_app_label_model_76bd3d3b_uniq
    on django_content_type (app_label, model);

create table django_migrations
(
    id      integer      not null
        primary key autoincrement,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime     not null
);

create table django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data text        not null,
    expire_date  datetime    not null
);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

create table musictour_luogo
(
    id        integer      not null
        primary key autoincrement,
    nome      varchar(100) not null,
    indirizzo varchar(200) not null,
    capienza  integer      not null
);

create table musictour_evento
(
    id          integer      not null
        primary key autoincrement,
    nome        varchar(100) not null,
    data        datetime     not null,
    descrizione text         not null,
    capienza    integer      not null,
    luogo_id    bigint
        references musictour_luogo
            deferrable initially deferred
);

create index musictour_evento_luogo_id_8180312e
    on musictour_evento (luogo_id);

create table musictour_ubicazione
(
    id          integer not null
        primary key autoincrement,
    orario_fine time,
    evento_id   bigint  not null
        references musictour_evento
            deferrable initially deferred,
    luogo_id    bigint  not null
        references musictour_luogo
            deferrable initially deferred
);

create index musictour_ubicazione_evento_id_e7bd58ea
    on musictour_ubicazione (evento_id);

create index musictour_ubicazione_luogo_id_320b5b33
    on musictour_ubicazione (luogo_id);

create table musictour_utente
(
    id               integer      not null
        primary key autoincrement,
    password         varchar(128) not null,
    last_login       datetime,
    is_superuser     bool         not null,
    username         varchar(150) not null
        unique,
    first_name       varchar(150) not null,
    last_name        varchar(150) not null,
    email            varchar(254) not null,
    is_staff         bool         not null,
    is_active        bool         not null,
    date_joined      datetime     not null,
    is_partecipante  bool         not null,
    is_organizzatore bool         not null
);

create table django_admin_log
(
    id              integer           not null
        primary key autoincrement,
    object_id       text,
    object_repr     varchar(200)      not null,
    action_flag     smallint unsigned not null,
    change_message  text              not null,
    content_type_id integer
        references django_content_type
            deferrable initially deferred,
    user_id         bigint            not null
        references musictour_utente
            deferrable initially deferred,
    action_time     datetime          not null,
    check ("action_flag" >= 0)
);

create index django_admin_log_content_type_id_c4bce8eb
    on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
    on django_admin_log (user_id);

create table musictour_organizzatore
(
    id_organizzatore integer      not null
        primary key autoincrement,
    nome             varchar(100) not null,
    cognome          varchar(100) not null,
    utente_id        bigint       not null
        unique
        references musictour_utente
            deferrable initially deferred
);

create table musictour_organizza
(
    id                  integer not null
        primary key autoincrement,
    data_organizzazione date,
    evento_id           bigint  not null
        references musictour_evento
            deferrable initially deferred,
    organizzatore_id    integer not null
        references musictour_organizzatore
            deferrable initially deferred
);

create index musictour_organizza_evento_id_097ab6b1
    on musictour_organizza (evento_id);

create index musictour_organizza_organizzatore_id_4b2f1011
    on musictour_organizza (organizzatore_id);

create table musictour_partecipante
(
    id        integer      not null
        primary key autoincrement,
    nome      varchar(100) not null,
    cognome   varchar(100) not null,
    email     varchar(254) not null
        unique,
    password  varchar(128) not null,
    utente_id bigint       not null
        unique
        references musictour_utente
            deferrable initially deferred
);

create table musictour_prenotazione
(
    id                integer     not null
        primary key autoincrement,
    data_prenotazione date        not null,
    codice_conferma   varchar(20) not null,
    evento_id         bigint      not null
        references musictour_evento
            deferrable initially deferred,
    partecipante_id   bigint      not null
        references musictour_partecipante
            deferrable initially deferred
);

create index musictour_prenotazione_evento_id_607d95a8
    on musictour_prenotazione (evento_id);

create index musictour_prenotazione_partecipante_id_0faa28ca
    on musictour_prenotazione (partecipante_id);

create table musictour_recensione
(
    id_recensione   integer not null
        primary key autoincrement,
    punteggio       integer not null,
    data            date    not null,
    testo           text,
    evento_id       bigint  not null
        references musictour_evento
            deferrable initially deferred,
    partecipante_id bigint  not null
        references musictour_partecipante
            deferrable initially deferred
);

create index musictour_recensione_evento_id_6573857e
    on musictour_recensione (evento_id);

create index musictour_recensione_partecipante_id_5f39099e
    on musictour_recensione (partecipante_id);

create table musictour_scrive
(
    id            integer not null
        primary key autoincrement,
    data          date    not null,
    recensione_id integer not null
        unique
        references musictour_recensione
            deferrable initially deferred,
    utente_id     bigint  not null
        references musictour_utente
            deferrable initially deferred
);

create index musictour_scrive_utente_id_b24a62e9
    on musictour_scrive (utente_id);

create table musictour_utente_groups
(
    id        integer not null
        primary key autoincrement,
    utente_id bigint  not null
        references musictour_utente
            deferrable initially deferred,
    group_id  integer not null
        references auth_group
            deferrable initially deferred
);

create index musictour_utente_groups_group_id_1701ada1
    on musictour_utente_groups (group_id);

create index musictour_utente_groups_utente_id_a8bd5ca7
    on musictour_utente_groups (utente_id);

create unique index musictour_utente_groups_utente_id_group_id_b3635e6f_uniq
    on musictour_utente_groups (utente_id, group_id);

create table musictour_utente_user_permissions
(
    id            integer not null
        primary key autoincrement,
    utente_id     bigint  not null
        references musictour_utente
            deferrable initially deferred,
    permission_id integer not null
        references auth_permission
            deferrable initially deferred
);

create index musictour_utente_user_permissions_permission_id_d95884a2
    on musictour_utente_user_permissions (permission_id);

create index musictour_utente_user_permissions_utente_id_731fe978
    on musictour_utente_user_permissions (utente_id);

create unique index musictour_utente_user_permissions_utente_id_permission_id_fb07dc06_uniq
    on musictour_utente_user_permissions (utente_id, permission_id);


