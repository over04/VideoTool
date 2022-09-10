CREATE TABLE if not exists SynPath
(
    id INTEGER UNIQUE NOT NULL ,
    source_path TEXT UNIQUE NOT NULL ,
    target_tv_path TEXT UNIQUE NOT NULL ,
    target_movie_path TEXT UNIQUE NOT NULL
);
CREATE TABLE if not exists Parse
(
    syn_id TEXT NOT NULL ,
    file_path TEXT UNIQUE NOT NULL , --必须是完整的地址
    id TEXT UNIQUE NOT NULL ,
    tmdb_id TEXT,
    name TEXT NOT NULL ,
    season INTEGER ,
    episode INTEGER ,
    media_type TEXT
);
--CREATE TABLE if not exists ParseTvTemp AS
--SELECT *
--FROM ParseTv
--WHERE 1 = 0;

CREATE TABLE if not exists TmdbTvTemp
(
    tv_id TEXT UNIQUE NOT NULL ,
    name TEXT , --英文名
    origin_name TEXT ,
    show_name TEXT , --最后获取的名称
    overview TEXT ,
    first_air_date INTEGER ,
    number_of_episodes INTEGER
);
CREATE TABLE if not exists TmdbEpisodeTemp
(
    tv_id TEXT NOT NULL ,
    id TEXT ,
    name TEXT , --最后获取的名称
    overview TEXT ,
    season INTEGER NOT NULL ,
    episode INTEGER NOT NULL ,
    air_date INTEGER
)