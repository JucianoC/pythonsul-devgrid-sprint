
-- Table: cluster
DROP TABLE IF EXISTS cluster;
CREATE TABLE cluster (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL);

-- Table: sensor_event
DROP TABLE IF EXISTS sensor_event;
CREATE TABLE sensor_event (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, clustered BOOLEAN DEFAULT FALSE, cluster_id INTEGER REFERENCES cluster (id) ON DELETE RESTRICT ON UPDATE RESTRICT DEFAULT NULL, cluster_label INTEGER DEFAULT NULL, device_id INTEGER NOT NULL, device_fw INTEGER NOT NULL, device_evt INTEGER NOT NULL, alarms TEXT DEFAULT NULL, power_active DECIMAL NOT NULL, power_reactive DECIMAL NOT NULL, power_appearent DECIMAL NOT NULL, line_current DECIMAL NOT NULL, line_voltage DECIMAL NOT NULL, line_phase DECIMAL NOT NULL, utc_time DATETIME NOT NULL, hz DECIMAL NOT NULL, wifi_strength INTEGER NOT NULL, dummy INTEGER NOT NULL);

-- Table: sensor_event_fft_img
DROP TABLE IF EXISTS sensor_event_fft_img;
CREATE TABLE sensor_event_fft_img (
    id              INTEGER PRIMARY KEY AUTOINCREMENT
                            NOT NULL
                            UNIQUE,
    value           DECIMAL NOT NULL,
    sensor_event_id INTEGER REFERENCES sensor_event (id) ON DELETE RESTRICT
                                                         ON UPDATE RESTRICT
                            NOT NULL
);

-- Table: sensor_event_fft_re
DROP TABLE IF EXISTS sensor_event_fft_re;
CREATE TABLE sensor_event_fft_re (
    id              INTEGER PRIMARY KEY AUTOINCREMENT
                            NOT NULL
                            UNIQUE,
    value           DECIMAL NOT NULL,
    sensor_event_id INTEGER REFERENCES sensor_event (id) ON DELETE RESTRICT
                                                         ON UPDATE RESTRICT
                            NOT NULL
);

-- Table: sensor_event_peaks
DROP TABLE IF EXISTS sensor_event_peaks;
CREATE TABLE sensor_event_peaks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, value DECIMAL NOT NULL, sensor_event_id INTEGER REFERENCES sensor_event (id) ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL);
