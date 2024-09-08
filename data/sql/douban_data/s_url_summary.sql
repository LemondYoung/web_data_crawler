CREATE TABLE `s_url_summary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'url类型',
  `url_status` int DEFAULT NULL COMMENT 'url状态',
  `count` int DEFAULT NULL COMMENT '数量',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `url_type` (`url_type`,`url_status`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='url统计表'