DROP TABLE IF EXISTS cluster;
CREATE TABLE `cluster` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS sensor_event;
CREATE TABLE `sensor_event` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `clustered` tinyint(1) DEFAULT '0',
  `cluster_id` int(10) unsigned DEFAULT NULL,
  `cluster_label` int(11) DEFAULT NULL,
  `device_id` int(10) unsigned NOT NULL,
  `device_fw` int(11) NOT NULL,
  `device_evt` int(11) NOT NULL,
  `alarms` varchar(45) NOT NULL,
  `power_active` float NOT NULL,
  `power_reactive` float NOT NULL,
  `power_appearent` float NOT NULL,
  `line_current` float NOT NULL,
  `line_voltage` float NOT NULL,
  `line_phase` float NOT NULL,
  `utc_time` datetime(6) NOT NULL,
  `hz` float NOT NULL,
  `wifi_strength` int(11) NOT NULL,
  `dummy` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_cluster_idx` (`cluster_id`),
  KEY `ix_power_active` (`power_active`) USING BTREE,
  CONSTRAINT `fk_cluster` FOREIGN KEY (`cluster_id`) REFERENCES `cluster` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS sensor_event_fft_img;
CREATE TABLE `sensor_event_fft_img` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` float NOT NULL,
  `sensor_event_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_sensor_event_fft_img_idx` (`sensor_event_id`),
  CONSTRAINT `fk_sensor_event_fft_img` FOREIGN KEY (`sensor_event_id`) REFERENCES `sensor_event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS sensor_event_fft_re;
CREATE TABLE `sensor_event_fft_re` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` float NOT NULL,
  `sensor_event_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_sensor_event_fft_re_idx` (`sensor_event_id`),
  CONSTRAINT `fk_sensor_event_fft_re` FOREIGN KEY (`sensor_event_id`) REFERENCES `sensor_event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS sensor_event_peaks;
CREATE TABLE `sensor_event_peaks` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` float NOT NULL,
  `sensor_event_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_sensor_event_peaks_idx` (`sensor_event_id`),
  CONSTRAINT `fk_sensor_event_peaks` FOREIGN KEY (`sensor_event_id`) REFERENCES `sensor_event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



