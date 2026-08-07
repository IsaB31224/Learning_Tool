CREATE TABLE Reflections (
    Reflection_id           INTEGER     PRIMARY KEY AUTOINCREMENT,
    Given_prompt            TEXT        NOT NULL,
    Reflection_Writing      TEXT        NOT NULL,
    Date                    TEXT        NOT NULL,
    Source_Author               TEXT,
    Media                   TEXT        NOT NULL,
    Topic_of_discussion     TEXT,
    Abstract_topic          TEXT,
    Character_referenced    TEXT
);